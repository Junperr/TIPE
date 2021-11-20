# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 11:20:58 2021

@author: Xtrem
"""
'''pour remplir penser à l'interpolation ou bien à gauss-seidel'''
import sqlite3 as sql
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

japan_map=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/map bondarie japan/gm-jpn-bnd_u_2_1/polbnda_jpn.shp")
# japan1_map=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/\
#     map bondarie japan/gm-jpn-bnd_u_2_1/coastl_jpn.shp")


df=pd.read_sql('SELECT * FROM station',sql.connect('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/sismic1.db'))
# read sql database for station and create panda dataframe
crs={'init': 'epsg:4326'}
# format des coordonnées


geometry = [Point(df["long"][i],df["lat"][i]) for i in range (len(df["long"]))]


geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
fig,ax = plt.subplots(figsize=(40,40))
japan_map.plot(ax=ax,color='k')
# japan1_map.plot(ax=ax,color='r',markersize=1)
geo_df[geo_df['network'] == 'kik'].plot(ax = ax, marker = '+',\
                color = '#ADD8E6', markersize = 50, label = 'kik station')
geo_df[geo_df['network'] == 'knt'].plot(ax = ax, marker = '^',\
                color = '#A020F0', markersize = 50, label = 'knt station')


df_s=pd.read_sql('SELECT * FROM seismes',\
            sql.connect('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/sismic1.db'))
geometry_s = [Point(df_s["long"][i],df_s["lat"][i]) for i in range (len(df_s["long"]))]
geo_df_s = gpd.GeoDataFrame(df_s,crs=crs,geometry=geometry_s)
geo_df_s.plot(ax=ax,marker='*',color='red',markersize=90,label='sismic event')

plt.legend(loc=4,fontsize=40,markerscale=6)
