# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:37:17 2021

@author: Xtrem
"""
import numpy as np 
import matplotlib.pyplot as plt
from conversion_data import *
from math import sqrt
import scipy.integrate as scii

def recup_name (path):
    t=""
    i=len(path)-1
    while i>=0 and path[i]!='.' :
        i+=-1
    i+=-1
    while i>=0 and path[i]!='/'  :
        t=path[i]+t
        i+=-1
    return t

def accel_values(path,folder=None):
    
    """ Recup PGV, PGA, PGA on the 3 axes for all station of one kik/knt folder
    created by all_in_one. """
    
    if 'kik' in path:
        ext=kik_ext
        path=path[:-4]
    elif 'knt':
        ext=knt_ext
        path=path[:-3]
    l=[]
    offset=[0,0,0]
    for nb in range (3):
        info , axe = recup_station_one_tab(path+ext[nb],accel=True)
        l.append(axe)
        offset[nb]=round(np.mean(l[nb]),3)
                #calculate offset of the different axes and recup acceleration

    for nb in range (3):
        for i in range (len(l[0])):
            l[nb][i]+=-offset[nb]
            l[nb][i]*=recup_scaling(info['_scale'])
    #remove offset off the signal
    return l,recup_name(path)

l,title=accel_values(ex7)
fig, axs = plt.subplots(2, 3,figsize=(30,15))

def offset (l,n):
    s=0 
    for i in range (len(l[n])):
        s+=int(l[n][i])
    return s/len(l[n])

def integrate(l):
    l1=[l[0]]
    for i in range (1,len(l)):
        l1.append(l1[i-1]+(l[i]+l[i-1])/200)
    return l1


vEW=integrate(l[0])
vUD=integrate(l[1])
vNS=integrate(l[2])
X=[0.01*x for  x in range(len(l[2]))]

plt.subplot(2,3,1)
plt.plot(X,l[0],lw=1.2)
plt.xlabel("Temps (s)",fontsize=20)
plt.ylabel("Accelération (gal)",fontsize=20)
plt.title('E-W acceleration',fontsize=25)

plt.subplot(2,3,2)
plt.plot(X,l[1],lw=1.2)
plt.xlabel("Temps (s)",fontsize=20)
plt.ylabel("Accelération (gal)",fontsize=20)
plt.title('N-S acceleration',fontsize=25)

plt.subplot(2,3,3)
plt.plot(X,l[2],lw=1.2)
plt.xlabel("Temps (s)",fontsize=20)
plt.ylabel("Accelération (gal)",fontsize=20)
plt.title('U-D acceleration',fontsize=25)

plt.subplot(2,3,4)
plt.plot(X,[sqrt(vEW[x]**2+vUD[x]**2+vNS[x]**2)for x in range(len(l[0]))],lw=1.2)
plt.xlabel("Temps (s)",fontsize=20)
plt.ylabel("Speed (cm/s)",fontsize=20)
plt.title('Velocity',fontsize=25)

plt.subplot(2,3,5)
plt.plot(X,[sqrt(l[0][x]**2+l[1][x]**2+l[2][x]**2)for x in range(len(l[0]))],lw=1.2)
plt.xlabel("Temps (s)",fontsize=20)
plt.ylabel("Accelération (gal)",fontsize=20)
plt.title('Acceleration Norm',fontsize=25)
