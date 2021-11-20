# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 17:51:32 2021

@author: Xtrem
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np 

df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
df.plot("pop_est",cmap="Blues" )
scalar=plt.cm.ScalarMappable(cmap="Blues")
scalar.set_array(np.array(df["pop_est"]))
scalar.autoscale()
plt.colorbar(scalar) 
