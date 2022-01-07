

# -*- coding: utf-8 -*-
"""
Created on Thu May 27 17:21:37 2021

@author: duhem.aristide
"""

import sqlite3  as sql
import os
import tarfile
import numpy as np 
from math import sqrt
conn=sql.connect('sismic1.db')

cursor = conn.cursor()
# cursor.execute("""
# DROP TABLE IF EXISTS seismes
# """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS seismes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    lat float  NOT NULL,
    long float NOT NULL,
    depth float NOT NULL,
    mag float NOT NULL) 
    """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS station(
    code TEXT PRIMARY KEY NOT NULL,
    lat float  NOT NULL,
    long float NOT NULL,
    heigt float NOT NULL,
    network TEXT NOT NULL)
    """)
    
cursor.execute("""
CREATE TABLE IF NOT EXISTS infos(
    station_code TEXT NOT NULL,
    earthquake_id  int,
    PGA float NOT NULL,
    PGA_EW float NOT NULL,
    PGA_UD float NOT NULL,
    PGA_NS float NOT NULL,
    PGV float,
    UNIQUE (station_code,earthquake_id))
    """)

def add_intel(date,station,network):
    
    conn=sql.connect('sismic1.db')
    cursor = conn.cursor()
    data = selec_more_opti2(date,station,network)
    idseisme = cursor.execute("""
            SELECT id FROM seismes WHERE date = ? and lat = ?                 
            """,(data['date'],data['lat'])).fetchone()
            
    if idseisme == None :
        cursor.execute("""
                   
    INSERT INTO seismes (date,lat,long,depth,mag) VALUES (?,?,?,?,?)

    """,(data['date'],float(data['lat']),
    float(data['long']),float(data['depth']),float(data['mag'])))
        
        idseisme = cursor.execute("""
            SELECT id FROM seismes WHERE date = ? and lat = ?                 
            """,(data['date'],data['lat'])).fetchone()
            
    idseisme=idseisme[0]
    
    if cursor.execute("""
            SELECT count(*) FROM station WHERE code=?                 
            """,(data['_code'],)).fetchone()[0]==0 :
        cursor.execute("""

    INSERT INTO station (code,lat,long,heigt,network) VALUES (?,?,?,?,?)

""",(data['_code'],data['_lat'],
data['_long'],data['_heigt'],data['network']))
    
    if cursor.execute("""
            SELECT count(*) FROM infos WHERE station_code = ? and earthquake_id = ?                 
            """,(data['_code'],idseisme)).fetchone()[0]==0:
                cursor.execute("""
                   
    INSERT INTO infos (station_code,earthquake_id,PGA,PGA_EW,PGA_UD,PGA_NS,PGV) VALUES (?,?,?,?,?,?,?)

    """,(data['_code'],idseisme,float(data['PGA']),float(data['.EW']),float(data['.UD'])\
        ,float(data['.NS']),float(data['PGV'])))
    conn.commit()
    

def addseisme(path=None,data=None):
    """ Add a seisme in the table seismes."""
    conn=sql.connect('sismic1.db')
    cursor = conn.cursor()
    if data==None:
        data=recup_station_one_tab(path)
    if cursor.execute("""
            SELECT count(*) FROM seismes WHERE date = ? and lat = ?                 
            """,(data['date'],data['lat'])).fetchone()[0]==0 :
                cursor.execute("""
                   
    INSERT INTO seismes (date,lat,long,depth,mag) VALUES (?,?,?,?,?)

    """,(data['date'],float(data['lat']),
    float(data['long']),float(data['depth']),float(data['mag'])))
    conn.commit()




def addstation(path=None,data=None):
    """ Add a station in the table station. """
    conn=sql.connect('sismic1.db')
    cursor = conn.cursor()
    if data==None:
        data=recup_station_one_tab(path)
    if cursor.execute("""
            SELECT count(*) FROM station WHERE code=?                 
            """,(data['_code'],)).fetchone()[0]==0 :
        cursor.execute("""

INSERT INTO station (code,lat,long,heigt,network) VALUES (?,?,?,?,?)

""",(data['_code'],data['_lat'],
data['_long'],data['_heigt'],data['network']))
    conn.commit()
seismes=cursor.execute ("""
                Select * from seismes 
                """).fetchall()
values=cursor.execute ("""
                Select * from infos where earthquake_id=3
                """).fetchall()
conn.commit()#end of sql
#os.getcwd() renvois le répertoire de travail actuel
#os.listdir(path) renvois les éléments du dossier path

def inttxt(txt):
    """ Return an int number from txt,
    exemple '34534jn22' return int 3453422 """
    t=""
    for i in txt:
        if 47<ord(i)<58:
            t+=i
    return int(t)


kik_ext=['.EW2','.UD2','.NS2','.UD1','.NS1','.EW1']
knt_ext=['.UD','.EW','.NS']
equivalence={0:'date',1:'lat',2:'long',3:'depth',4:'mag',5:'_code',6:'_lat',\
             7:'_long',8:'_heigt',9:'_date',10:'_freq',11:'duration',\
             12:'axe',13:'_scale',14:'max_acc',15:'last_correc'}

def integrate123(l):#euler
    l1=np.zeros(len(l))
    l1[0]=l[0]
    for i in range (1,len(l)):
        l1[i]=(l1[i-1]+(l[i]+l[i-1])/200)
    return l1

    
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

ex='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/20200912114400/kik/ABSH062009121144.NS1'
ex1='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/20200912114400/kik'
ex2 = 'C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/Test_kik'
ex3='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/HKD0911006181123.EW'
ex4='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/20200912114400/kik/MYGH032009121144.NS1'# point de secousse importantes
ex5=('C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/earthquake/20200912114400/kik/MYGH032009121144.EW2',
 'C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/earthquake/20200912114400/kik/MYGH032009121144.UD2',
 'C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/earthquake/20200912114400/kik/MYGH032009121144.NS2')
ex6='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/earthquake/20110311144600/knt/IWT0211103111446.NS'
ex7='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE/data_gestion/earthquake/20110311144600/kik/IBUH031103111446.NS1'

def peak_value(path,right_ext=None):
    """ Recup PGV, PGA, PGA on the 3 axes for all station of one kik/knt folder
    created by all_in_one. """
    L=os.listdir(path)
    stock={}
    
    if right_ext==None:
        right_ext=path[-3:]
        if right_ext == 'kik':
            right_ext = kik_ext
        elif right_ext == 'knt':
            right_ext = knt_ext
        else:
            raise 'wrong folder'
            #verification that the path is a kik or knt folder if it's the case
            #we save it to recup extention later right_ext[nb] give an extention
            
    for file in L:
        station = extensions(file)[0]
        if station not in stock : #there is multiple time the same
        #name due to different axes, in order to not calculate the same value 
        #multiple time there is a verification if it's already done
            all_val={'sum' : 0}
            axes,integration=None,None
            offset=[0,0,0]
            for nb in range (3):
                info , axe = recup_station_one_tab(path +  "/" + station + right_ext[nb] , accel=True)
                if type(axes) != np.ndarray:
                    axes = np.zeros([3,len(axe)])
                if type(integration) != np.ndarray:
                    integration = np.zeros([3,len(axe)])
                axes[nb] = axe
                offset[nb]=round(np.mean(axes[nb]),3)
                integration[nb] = axe-offset[nb]
                #calcule de la valeur moyenne d'un axe et recupère l'accélération
                axes[nb] = abs(axes[nb] - offset[nb])
                #on retire la composante continue du signal

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
        stock[extensions(file)[0]]= all_val
    return stock


test=('20210516122400','ABSH022105161224','kik')
test1=('20200912114400', 'MYGH032009121144', 'kik')

def selec_more_opti2 (date,station,network):
    
    path='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/' + date + "/" + network
    
    if network == 'kik':
        right_ext = kik_ext
    elif network == 'knt':
        right_ext = knt_ext
    else:
        raise 'wrong network'
            #associe les bonnes extentions de fichier en fonction du réseaux
    
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
    scale = recup_scaling(info['_scale'])
    right_ext=knt_ext #on s'arrange pour avoir uniquement EW,UD et NS
    # peut importe le réseaux
    
    for nb in range (3):
        info[right_ext[nb]] = round(np.max(axes[nb])*scale,3)
                    #add PGA of one axis 
        integration[nb] = integrate123(integration[nb])
    velocity = np.prod([integration,integration],axis=0)
    velocity = np.sum(velocity,axis=0)
    somme = np.prod([axes,axes],axis=0)
    somme = np.sum(somme,axis=0)
    info['PGA']=round(sqrt(np.max(somme))*scale,3)
    info['PGV']=round(sqrt(np.max(velocity))*scale,3)
    #add PGA and PGV (norm)
    
    return info



#kik 6 axes knt 3 axes 
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

######## mettre add_intel a la place de staiton et seisme
def all_in_one(path='C:/Users/Xtrem/OneDrive/Documents/°Prepa/Info/TIPE\
/data_gestion/earthquake/'):
    
    """ A function using most of the previous function in order to extract all
    usefull data from a directory containing all the earthquake just after download """
    folder = os.listdir(path) # liste des éléments dans path 
    for file_name in folder :
        
        if extensions(file_name)[1]=='.tar':
            #traite uniquement les fichiers compressé en .tar
            
            new_folder=path+extensions(file_name)[0]
            extracted=[]
            try : os.mkdir(new_folder)
            except:
                extracted=os.listdir(new_folder)
            #si le dossier n'existe pas on le créé sinon on récupere le nom
            #des fichiers à l'intérieur (inutile maintenant que je supprime
            #les fichier une fois que je n'en ais plus le besoin)
            
            compress = tarfile.open(new_folder+".tar",'r')
            inside_members = compress.getmembers()
            #on ouvre le fichier et récupère les infos des fichier à l'intérieur
            for member in inside_members :
                if 'knt' not in extracted and extensions(member.name)[1]=='.knt.tar.gz' : 
            #première condition inutile depuis la suppression des fichiers une fois utilisé
                    #vérifie si le dossier knt n'a pas déjà était extrait
                    #et on selectionne uniquement le fichier contenant 
                    #les informations sur les stations du réseau knt
                    compress.extract(member,new_folder)#on extrait le fichier tar
                    os.mkdir(new_folder+"/knt")# créer le dossier knt
                    knt = tarfile.open(new_folder+"/"+member.name,'r')
                    #ouvre le fichier tar contenant les informations des stations knt
                    for member1 in knt.getmembers() :
                        if extensions(member1.name[1:])[1] in knt_ext[:3]:
                            knt.extract(member1,new_folder+"/knt")
                            info=recup_station_one_tab(new_folder+"/knt/"+member1.name[1:])
                            #on récupère les fichiers qui nous interesse
                            # addstation(data=info)
                            if extensions(member1.name[1:])[1] =='.UD' :
                                date=str(inttxt(info['date']))
                                add_intel(date, info['_code'] + date[2:-2], 'knt')
                                #ajoute les informations nécessaire dans la base de donnée
                                for ext in knt_ext :
                                    os.remove(new_folder+"/knt/"+extensions(member1.name[1:])[0]+ext)
                                #supprime les fichier une fois que l'on a récupéré ce qui nous interessait
                                
                    knt.close()

                    os.remove(new_folder+"/"+member.name)
                    #on supprime le fichier tar car ils prennent beaucoup de place
                    
                elif 'kik' not in extracted and extensions(member.name)[1]=='.kik.tar.gz':
            #première condition inutile depuis la suppression des fichiers une fois utilisé
                    compress.extract(member,new_folder)
                    os.mkdir(new_folder+"/kik")
                    kik = tarfile.open(new_folder+"/"+member.name,'r')
                    for member2 in kik.getmembers() :
                        if extensions(member2.name[1:])[1] in kik_ext:
                            kik.extract(member2,new_folder+"/kik")
                            info=recup_station_one_tab(new_folder+"/kik/"+member2.name[1:])
                            # addstation(data=info)
                            if extensions(member2.name[1:])[1] =='.UD2' :
                                date=str(inttxt(info['date']))
                                add_intel(date, info['_code'] + date[2:-2], 'kik')
                                for ext in kik_ext :
                                    os.remove(new_folder+"/kik/"+extensions(member2.name[1:])[0]+ext)
                    
                    kik.close()

                    os.remove(new_folder+"/"+member.name)
                #Pour cette partie c'est exactement la même chose que pour knt
                #mais pour le réseau kik
                
            os.rmdir(new_folder+"/knt")
            os.rmdir(new_folder+"/kik")
            os.rmdir(new_folder)
            #on supprime les dossiers créer
            
            compress.close()
            #on ferme le fichier ouvert
            os.remove(new_folder+".tar")
            #et on le supprime pour les même raisons

