# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:23:08 2021

@author: Xtrem
"""

from shapely.geometry import Polygon,Point
import geopandas as gpd

polys1 = gpd.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]),
                              Polygon([(2,2), (4,2), (4,4), (2,4)])])


polys2 = gpd.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]),
                              Polygon([(3,3), (5,3), (5,5), (3,5)])])


df1 = gpd.GeoDataFrame({'geometry': polys1, 'df1':[1,2]})

df2 = gpd.GeoDataFrame({'geometry': polys2, 'df2':[1,2]})

ax = df1.plot(color='red');

df2.plot(ax=ax, color='green', alpha=0.5);

res_inter = gpd.overlay(df1,df2, how='intersection')

res_inter.plot(ax=ax, facecolor=("k"))

other = gpd.GeoDataFrame({'geometry':[Point(1.5,1.5),Point(3,1),Point(3,5)],'df3':[1,2,3]})

other.plot(ax=ax)

o_inter = gpd.overlay(other, df1)

o_inter.plot(ax=ax, marker='o')
