# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:52:36 2021

@author: Xtrem
"""
import sqlite3 as sql
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from shapely.geometry import Point,Polygon
from scipy.interpolate import griddata
import numpy as np 
from scipy import ndimage
# import geoplot

japan_map=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/map bondarie japan/gm-jpn-bnd_u_2_1/polbnda_jpn.shp")
# japan1_map=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/\
#     map bondarie japan/gm-jpn-bnd_u_2_1/coastl_jpn.shp")


s_pos=pd.read_sql("""SELECT long,lat,network,PGA FROM station as s join infos as i 
                  on s.code=i.station_code
                  where i.earthquake_id=3""",sql.connect('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/sismic1.db'))
# read sql database for station and create panda dataframe
crs={'init': 'epsg:4326'}
# système de coordonnées


geometry = [Point(s_pos["long"][i],s_pos["lat"][i]) for i in range (len(s_pos["long"]))]

geo_s_pos = gpd.GeoDataFrame(s_pos,crs=crs,geometry=geometry)
    
s_pos_s=pd.read_sql('SELECT lat,long FROM seismes where id=3',\
            sql.connect('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/sismic1.db'))

geometry_s = [Point(s_pos_s["long"][i],s_pos_s["lat"][i]) for i in range (len(s_pos_s["long"]))]
geo_s_pos_s = gpd.GeoDataFrame(s_pos_s,crs=crs,geometry=geometry_s)


def map_plot (map_back=False, cmap=None, colors_name=None, iterpolate=False, n=10000):
    """

    Parameters
    ----------
    map_back : Bool, optional
        Si True affiche la carte en fond sinon uniquement les points.
        The default is False.
    cmap : Colormap, optional
        To force a colormap. The default is None.
    colors_name : List, optional
        [string,arg*] arg are hexcolor. The default is None.
    If both cmap and colors_name are None: we select 'jet' colormap
    Returns
    -------
    None.

    """
    fig,ax = plt.subplots(figsize=(40,40))
    
    if map_back:
        japan_map.plot(ax=ax,color='k')   
        # affiche la carte du japon en fond 

    if cmap==None and colors_name!=None:
        try:
            create_cmap1(colors_name[1:],colors_name[0])
            cmap=colors_name[0]
        except:
            cmap=colors_name[0]

    #création de la colormap si elle n'est pas déjà créée
    cmap1=plt.get_cmap(cmap,10)
    
    bounds=np.array([0.0, 0.2, 1.0, 4.0, 15.0, 50.0, 100.0, 200.0, 400.0, 750.0, 2000.0])
    norm=colors.BoundaryNorm(boundaries=bounds, ncolors=10)
    scalar=plt.cm.ScalarMappable(norm=norm,cmap=cmap1)
    bar = plt.colorbar(scalar,fraction=0.03,drawedges=True,label='PGA (gal)', spacing='uniform', ticks=[0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0,100.0,200.0,500.0,1000.0,2000.0])
    bar.ax.set_yticklabels(['0.2','0.5','1.0','2.0','5.0','10.0','20.0','50.0','100.0','200.0','500.0','1000.0','2000.0'])
# met la barre à l'échelle et créer la norme
        
    geo_s_pos[geo_s_pos['network'] == 'kik'].plot(column="PGA", ax = ax, marker = '.',\
                markersize = 25,vmax=2000.0 ,norm=norm,label = 'kik station',cmap=cmap1)
    
    geo_s_pos[geo_s_pos['network'] == 'knt'].plot(column="PGA", ax = ax, marker = '^',\
            markersize = 20, norm=norm, vmax=2000.0, label = 'knt station', cmap=cmap1)
    
    geo_s_pos_s.plot(ax=ax,marker='*',color='red',markersize=90,label='sismic event')
    plt.legend(loc=4,fontsize=40,markerscale=6)
    # plt.plot(np.linspace(125,155,500),(10*np.cos(np.linspace(125,155,500))+30))
    
    
    ###interpolation à partir d'ici à finir  
    if interpolate:
        n=n**0.5
        point = np.array([(s_pos['long'][i],s_pos['lat'][i]) for i in range (len(s_pos['long']))])
        xgrid,ygrid=np.mgrid[min(s_pos['long']):max(s_pos['long']):n*1j , min(s_pos['lat']):max(s_pos['lat']):n*1j]
        interpolated_values=griddata(point,np.array(s_pos['PGA']),(xgrid,ygrid),method='cubic',fill_value=0.0)
        dataframe={'values' : [],'geometry':[]}
        for i in range (int(n)):
            for j in range (int(n)):
                dataframe['values'].append(interpolated_values[i,j])
                dataframe['geometry'].append(Point((xgrid[i,j],ygrid[i,j])))
        dataframe['geometry']=gpd.GeoSeries(dataframe['geometry'])
        geo_values = gpd.GeoDataFrame(dataframe,crs=crs,geometry=dataframe['geometry'])
        geo_values1 = gpd.overlay(geo_values,japan_map,how='intersection')
        # print(geo_values.head())
        geo_values1.plot(column="values", ax = ax, marker = ',',alpha=0.5,\
                        markersize = 5, norm=norm, vmax=2000.0, label = 'knt station', cmap=cmap1)
    
    pass


accel_colors=['accel','#fefefe','#99a7da','#4096df','#33ccad','#99ff60','#ffff00','#ff9a34','#ff6275','#990000']

def create_cmap1(color_list,name='test'):
    
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
            dataframe['geometry'].append(Point((xgrid[i,j],ygrid[i,j])))
    geo_values=gpd.GeoDataFrame(dataframe,crs=crs,geometry=dataframe['geometry'])
    geo_values.plot(column='values',cmap='accel')
    
    
def heat_map( bins=(100,100), smoothing=1.3, cmap='jet',colors=None):
    fig,ax = plt.subplots(figsize=(40,40))
    x=[s_pos["long"][i] for i in range (len(s_pos["long"]))]
    y=[s_pos["lat"][i] for i in range (len(s_pos["long"]))]
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    if colors!=None:
        cmap=create_cmap1(colors)

    logheatmap = heatmap#np.log(heatmap)
    print(logheatmap)
    # logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='constant')
    
    plt.imshow(logheatmap, cmap=cmap, extent=extent)
    geo_s_pos[geo_s_pos['network'] == 'kik'].plot(ax = ax, marker = '+',\
                color = '#ADD8E6', markersize = 50, label = 'kik station')
    geo_s_pos[geo_s_pos['network'] == 'knt'].plot(ax = ax, marker = '^',\
                color = '#A020F0', markersize = 50, label = 'knt station')
    plt.colorbar(plt.cm.ScalarMappable(cmap=cmap))
    plt.gca().invert_yaxis()
    plt.show()
    
