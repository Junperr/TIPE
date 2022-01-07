# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:52:36 2021

@author: Junper
"""
import sqlite3 as sql
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import shapely.geometry as geo
from scipy.interpolate import griddata
import numpy as np 
from scipy import ndimage
# import geoplot

japan_f=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/map bondarie japan/gm-jpn-bnd_u_2_1/polbnda_jpn.shp")
japan_c=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/map bondarie japan/gm-jpn-bnd_u_2_1/coastl_jpn.shp")



s_pos=pd.read_sql("""SELECT long,lat,network,PGA FROM station as s join infos as i 
                  on s.code=i.station_code
                  where i.earthquake_id=3""",sql.connect('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/sismic1.db'))
# read sql database for station and create panda dataframe
crs={'init': 'epsg:4326'}
# système de coordonnées


geometry = [geo.Point(s_pos["long"][i],s_pos["lat"][i]) for i in range (len(s_pos["long"]))]

geo_s_pos = gpd.GeoDataFrame(s_pos,crs=crs,geometry=geometry)
    
s_pos_s=pd.read_sql('SELECT lat,long FROM seismes where id=3',\
            sql.connect('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/sismic1.db'))

geometry_s = [geo.Point(s_pos_s["long"][i],s_pos_s["lat"][i]) for i in range (len(s_pos_s["long"]))]
geo_s_pos_s = gpd.GeoDataFrame(s_pos_s,crs=crs,geometry=geometry_s)

accel_colors=['accel','#ffffff','#99b3e6','#4073d9','#33ccad','#06d039','#99ff60','#ffff00','#ff9a34','#ff6275','#990000']


def map_plot (map_back=True, cmap=None, colors_name = accel_colors, interpolate=False, n=100,msize=50):
    """

    Parameters:
        map_back : Bool, optional
            Si True affiche la carte en fond sinon uniquement les points.
            The default is True.
        cmap : Colormap, optional
            To force a colormap. The default is None.
        colors_name : List, optional
            [string,arg*] arg are colors. The default is accel_colors.
        interpolate: Bool, optional
            Si True affiche le rendu avec une interpollation réaliser avec n
                points par axes 
    
    USE:
        Rendu de l'accéleration maximal d'un séisme sur le japon
    Returns
    -------
    None.

    """
    fig,ax = plt.subplots(figsize=(25,25))
    ax.set_facecolor('#d3ffff')
    ax.set_ylim([min(s_pos['lat'])-1,max(s_pos['lat'])+1])
    ax.set_xlim([min(s_pos['long'])-1,max(s_pos['long'])+1])
    if map_back:
        japan_f.plot(ax=ax,color="w",edgecolor="w",zorder=1)
        japan_c.plot(ax=ax,color="k",edgecolor="none",linewidth=0.5,zorder=3)
        # affiche la carte du japon en fond 

    if cmap==None and colors_name!=None:
        try:
            create_cmap1(colors_name[1:],colors_name[0])
            cmap=colors_name[0]
        except:
            cmap=colors_name[0]

    # création de la colormap si elle n'est pas déjà créée
    cmap1=plt.get_cmap(cmap,10)
    #on récupère uniquement 10 couleurs en réalité celles de la liste accel_colors
    #il y a une meilleure faocn de faire la colormap mais ce que j'ai fais est 
    #suffisant
    bounds=np.array([0.0, 0.2, 1.0, 4.0, 15.0, 50.0, 100.0, 200.0, 400.0, 750.0, 2000.0])
    norm=colors.BoundaryNorm(boundaries=bounds, ncolors=10)
    scalar=plt.cm.ScalarMappable(norm=norm,cmap=cmap1)
    bar = plt.colorbar(scalar,fraction=0.03,drawedges=True,label='PGA (gal)',spacing='uniform', ticks=[0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0,100.0,200.0,500.0,1000.0,2000.0])
    bar.ax.set_yticklabels(['0.2','0.5','1.0','2.0','5.0','10.0','20.0','50.0','100.0','200.0','500.0','1000.0','2000.0'])
# met la barre à l'échelle et créer la norme et ajoute des graduations
        
    geo_s_pos[geo_s_pos['network'] == 'kik'].plot(column="PGA", ax = ax, marker = ',',\
                markersize = 85,edgecolor="black",linewidth=0.5,vmax=2000.0 ,norm=norm,label = 'kik station',cmap=cmap1,zorder=4)

    geo_s_pos[geo_s_pos['network'] == 'knt'].plot(column="PGA", ax = ax, marker = '^',\
             markersize=100 ,edgecolor="black",linewidth=0.5,norm=norm, vmax=2000.0, label = 'knt station', cmap=cmap1,zorder=6)
    # on affiche les sismogrpahes du réseaux kik et knt qui ont percu le seisme 
    geo_s_pos_s.plot(ax=ax,marker='*',color='red',markersize=125,label='sismic event',zorder=5)
    plt.legend(loc=4,fontsize=40,markerscale=6)
    # ajout d el'épicentre et de la legende
    # plt.plot(np.linspace(125,155,500),(10*np.cos(np.linspace(125,155,500))+30))
    
    
    ###interpolation à partir d'ici à finir  
    if interpolate:
        ratio=(max(s_pos['lat'])-min(s_pos['lat']))/(max(s_pos['long'])-min(s_pos['long']))
        if ratio<=1:
            xgrid,ygrid=np.mgrid[min(s_pos['long']):max(s_pos['long']):n*1j , min(s_pos['lat']):max(s_pos['lat']):ratio*n*1j]
        else:
            xgrid,ygrid=np.mgrid[min(s_pos['long']):max(s_pos['long']):n*1j/ratio , min(s_pos['lat']):max(s_pos['lat']):n*1j]
        #meshgrid prend en argument le nombre de point selon un axe et non le nombre total
        #on ajuste donc le nombre de point pour qu'ils soient répartit uniformément 
        #avec comme nombre maximum de point selon un axe n
        point = np.array([(s_pos['long'][i],s_pos['lat'][i]) for i in range (len(s_pos['long']))])
        #on reucupere les coordonnées de tout les sismographes pour les utiliser
        #en tant que valeurs de références pour l'interpolation
        
        interpolated_values=griddata(point,np.array(s_pos['PGA']),(xgrid,ygrid),method='linear',fill_value=0.0)
        #on créer une grille de n points sur le plus petit rectangle contenant tout les sismographes
        # print(len(xgrid),len(xgrid[0]),len(ygrid),len(ygrid[0]),sep='\n')
        dataframe={'values' : [],'geometry':[]}
        for i in range (len(xgrid)):
            for j in range (len(xgrid[0])):
                dataframe['values'].append(interpolated_values[i,j])
                dataframe['geometry'].append(geo.Point((xgrid[i,j],ygrid[i,j])))
        dataframe['geometry']=gpd.GeoSeries(dataframe['geometry'])
        geo_values = gpd.GeoDataFrame(dataframe,crs=crs,geometry=dataframe['geometry'])
        geo_values1 = geo_values.overlay(japan_f,how='intersection')
        # # print(geo_values.head())
        geo_values1.plot(column="values", ax = ax, marker = '.',\
                        markersize = msize, norm=norm, vmax=2000.0, label = 'knt station', cmap=cmap1,zorder=2)
        # inprogress(ax,geo_values,map_back)

    pass

def inprogress(ax,geo_values,map_back):
    list_p = geo.MultiPoint(np.array(geo_values[geo_values['values']>5]['geometry']))
    points =gpd.GeoDataFrame(geometry = [list_p])
    convex = gpd.GeoDataFrame(geometry = [list_p.convex_hull])
    if map_back:
        inter= gpd.overlay(convex,japan_f)
    inter.plot(ax = ax, color = 'yellow')
    print(inter)
    return inter
    points.plot(marker = ',', markersize = 5, ax = ax, color = 'red')
    points_inter= gpd.overlay(inter,points)
    points_inter.plot(marker = '*', markersize = 5, ax = ax, color = 'green')
    

def create_cmap1(color_list,name='test'):
    """
    PARAMETER:
        color_list : list
            list of colors.
        name : str, optional
            the name of your futur colormap. The default is 'test'.
    USE:
        Create a color map from a list of color in the order given in color_list        
    Return:
        None
    """
    cmap = colors.LinearSegmentedColormap.from_list(name, color_list)
    plt.register_cmap(name, cmap)
    
    
def interpolate(n):
    n=n**0.5
    point = np.array([(s_pos['long'][i],s_pos['lat'][i]) for i in range (len(s_pos['long']))])
    xgrid,ygrid=np.mgrid[min(s_pos['long']):max(s_pos['long']):n*1j , min(s_pos['lat']):max(s_pos['lat']):n*1j]
    interpolated_values=griddata(point,np.array(s_pos['PGA']),(xgrid,ygrid),method='linear',fill_value=0.0)
    dataframe={'values' : [],'geometry':[]}
    for i in range (int(n)):
        for j in range (int(n)):
            dataframe['values'].append(interpolated_values[i,j])
            dataframe['geometry'].append(geo.Point((xgrid[i,j],ygrid[i,j])))
    geo_values=gpd.GeoDataFrame(dataframe,crs=crs,geometry=dataframe['geometry'])
    geo_values.plot(column='values',cmap='accel')
