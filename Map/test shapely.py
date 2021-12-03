# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:23:08 2021

@author: Xtrem
"""

from shapely.geometry import Polygon,Point
import geopandas as gpd

import sqlite3 as sql
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import shapely.geometry as geo
from scipy.interpolate import griddata
import numpy as np 
from scipy import ndimage

# polys1 = gpd.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]),
#                               Polygon([(2,2), (4,2), (4,4), (2,4)])])


# polys2 = gpd.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]),
#                               Polygon([(3,3), (5,3), (5,5), (3,5)])])


# df1 = gpd.GeoDataFrame({'geometry': polys1, 'df1':[1,2]})

# df2 = gpd.GeoDataFrame({'geometry': polys2, 'df2':[1,2]})

# ax = df1.plot(color='red');

# df2.plot(ax=ax, color='green', alpha=0.5);

# res_inter = gpd.overlay(df1,df2, how='intersection')

# res_inter.plot(ax=ax, facecolor=("k"))

# other = gpd.GeoDataFrame({'geometry':[Point(1.5,1.5),Point(3,1),Point(3,5)],'df3':[1,2,3]})

# other.plot(ax=ax,edgecolor="black")

# o_inter = gpd.overlay(other, df1)

# o_inter.plot(ax=ax, marker='o')

# ['f_code', 'coc', 'nam', 'laa', 'pop', 'ypc', 'adm_code', 'salb', 'soc',
       # 'geometry'],
       
jf=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/map bondarie japan/gm-jpn-bnd_u_2_1/polbnda_jpn.shp")
jc=gpd.read_file("C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/map bondarie japan/gm-jpn-bnd_u_2_1/coastl_jpn.shp")

fig,ax=plt.subplots(2,figsize=(5,5))

ax[0].set_facecolor('#99ff60')
ax[1].set_facecolor('#06d039')

# jf.plot(ax=ax,color="w",edgecolor="w",zorder=1)
# jc.plot(ax=ax,color="k",edgecolor="none",linewidth=0.5,zorder=2)

# print(japan_map.columns)
