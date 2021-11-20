# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 21:04:44 2021

@author: Xtrem
"""

import sqlite3  as sql
import os
import tarfile
import numpy as np 
from math import sqrt
from scipy.integrate import odeint

kik_ext=['.EW2','.UD2','.NS2','.UD1','.NS1','.EW1']
knt_ext=['.UD','.EW','.NS']
equivalence={0:'date',1:'lat',2:'long',3:'depth',4:'mag',5:'_code',6:'_lat',\
             7:'_long',8:'_heigt',9:'_date',10:'_freq',11:'duration',\
             12:'axe',13:'_scale',14:'max_acc',15:'last_correc'}

def inttxt(txt):
    """ Return an int number from txt,
    exemple '34534jn22' return int 3453422 """
    t=""
    for i in txt:
        if 47<ord(i)<58:
            t+=i
    return int(t)


def extensions(name):#pas de point dans le nom du fichier
    """ Return "core" containing the name off the file and ext the extension
    but the file name should not contain any."""
    n=len(name)
    core=""
    ext=""
    ind=0
    while ind<n and name[ind]!="." :
        core+=name[ind]
        ind+=1
    while ind <n:
        ext+=name[ind]
        ind+=1
    return core,ext

def recup_scaling(txt):
    """
    txt : the txt scale factor at format number(gal)/number
    Returns : numeric value of the scale factor
    """
    ind=0
    while 47<ord(txt[ind])<58 :
        ind+=1
    num1=txt[:ind]
    while 48>ord(txt[ind]) or ord(txt[ind])>57 :
        ind +=1
    num2=txt[ind:]
    return int(num1)/int(num2)

def consecutive_split(text,l=[]):
    """ Function used in order to recup acceleration value from ascii format. """
    current=""
    for i in range (len(text)):
         if text[i]==' ':
             if current!=' ' and current !="":
                 l.append(int(current))
                 current=""
         else :
            current+=str(text[i])
    return l

ex5=('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/\
data_gestion/earthquake/20200912114400/kik/MYGH032009121144.EW2'\
     ,'C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/\
data_gestion/earthquake/20200912114400/kik/MYGH032009121144.UD2'\
     ,'C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/\
data_gestion/earthquake/20200912114400/kik/MYGH032009121144.NS2')

def recup_station_one_tab (path,accel=False):
    """ Recup station/earthquake info (in info) and acceleration value in l. """
    file=open(path,'r')
    info={}
    j=0
    l=[]
    for ligne in file  :
        if j>16 and accel==True:
            l=consecutive_split(ligne,l)
        elif j<16:
            info[equivalence[j]]=ligne[18:len(ligne)-1]
        j+=1
    if extensions(file.name)[1] in knt_ext :
        info['network']='knt'
    elif extensions(file.name)[1] in kik_ext :
            info['network']='kik'
    file.close()
    if accel :
        return info,np.array(l)
    else:
        return info
    
def integrate123(l):#euler
    l1=np.zeros(len(l))
    l1[0]=l[0]
    for i in range (1,len(l)):
        l1[i]=(l1[i-1]+(l[i]+l[i-1])/200)
    return l1



kik_ext=['.EW2','.UD2','.NS2','.UD1','.NS1','.EW1']
knt_ext=['.EW','.UD','.NS']
equivalence={0:'date',1:'lat',2:'long',3:'depth',4:'mag',5:'_code',6:'_lat',\
             7:'_long',8:'_heigt',9:'_date',10:'_freq',11:'duration',\
             12:'axe',13:'_scale',14:'max_acc',15:'last_correc'}
test=('20210516122400','ABSH022105161224','kik')

    
def selec_more_opti2 (date,station,network):
    
    path='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/' + str(inttxt(date)) + "/" + network
    
    if network == 'kik':
        right_ext = kik_ext
    elif network == 'knt':
        right_ext = knt_ext
    else:
        raise 'wrong network'
            #associe les bonnes extentions de fichier ne fonction du réseaux
    all_val={'sum' : 0}
    axes,integration=None,None
    offset=[0,0,0]
    for nb in range (3):
                info , axe = recup_station_one_tab(path +  "/" + station + right_ext[nb] , accel=True)
                if type(axes) != np.ndarray:
                    axes = np.zeros([3,len(axe)])
                if type(integration) != np.ndarray:
                    integration = np.zeros([3,len(axe)])
                #initialisation de axes et integration aux bonnes dimentions
                axes[nb] = axe
                #intitialisation des valeurs
                offset[nb]=round(np.mean(axes[nb]),3)
                #calcule de la valeur moyenne 
                integration[nb] = axe-offset[nb]
                axes[nb] = abs(axes[nb] - offset[nb])
                #on retire la composante continue du signal

    right_ext=knt_ext
    for nb in range (3):
        all_val[right_ext[nb]] = round(np.max(axes[nb])*recup_scaling(info['_scale']),3)
                    #add PGA of one axis 
        integration[nb] = integrate123(integration[nb])
    velocity = np.prod([integration,integration],axis=0)
    velocity = np.sum(velocity,axis=0)
    somme = np.prod([axes,axes],axis=0)
    somme = np.sum(somme,axis=0)
    all_val['sum']=round(sqrt(np.max(somme))*recup_scaling(info['_scale']),3)
    all_val['PGV']=round(sqrt(np.max(velocity))*recup_scaling(info['_scale']),3)
    #add PGA and PGV (norm)
    
    return all_val









