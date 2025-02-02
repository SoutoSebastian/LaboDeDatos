# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:23:03 2024

@author: Sebastián
"""
from inline_sql import sql, sql_val
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import tree
import pandas as pd


ruta = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\claseModelo\\"

archivo = "arboles.csv"

df = pd.read_csv(ruta+archivo)

#%%
#HISTOGRAMAS:
    
nbins = 20

f, s = plt.subplots()

plt.suptitle('altura', size = 'large')
sns.histplot(data = df, x = 'altura_tot', hue = 'nombre_com', bins = nbins, stat = 'probability',  palette = 'viridis')


f2,s2 = plt.subplots()

plt.suptitle('diametro', size = 'large')
sns.histplot(data = df, x = 'diametro', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis')


f3, s3 = plt.subplots()

plt.suptitle('inclinacion', size = 'large')
sns.histplot(data = df, x = 'inclinacio', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis')

#%%

#SCATTER:

fig, ax = plt.subplots() 

plt.rcParams['font.family'] = 'sans-serif'           
ax.scatter(data = df,  
           x='altura_tot', 
           y='diametro',
           c=df['nombre_com'].astype('category').cat.codes,
           s=8,                       
           cmap = 'viridis')           

ax.set_title('Diametro en funcion de Altura') 
ax.set_xlabel('altura', fontsize='medium')          
ax.set_ylabel('diametro', 
              fontsize='medium')                    

#%%

fig, ax = plt.subplots() 

plt.rcParams['font.family'] = 'sans-serif'           
scatter = ax.scatter(data=df,  
                     x='altura_tot', 
                     y='diametro',
                     c=df['nombre_com'].astype('category').cat.codes,
                     s=8,                       
                     cmap='viridis')           

ax.set_title('Diámetro en función de Altura') 
ax.set_xlabel('Altura', fontsize='medium')          
ax.set_ylabel('Diámetro', fontsize='medium')          


# Crear la leyenda automáticamente
handles, labels = scatter.legend_elements()
ax.legend(handles, df['nombre_com'].unique(), title="Especies")


#%%

#ARBOLES DE DECICSION:
    
#%%

#1)
X = df[['altura_tot', 'diametro', 'inclinacio']]
Y = df['nombre_com']

fnames = X.columns.tolist()

#%%

clf_info = tree.DecisionTreeClassifier(criterion = "entropy", max_depth= 4)
clf_info = clf_info.fit(X, Y)

cnames = clf_info.classes_.tolist()

plt.figure(figsize= [35,15])
tree.plot_tree(clf_info, feature_names = fnames, class_names = cnames,filled = True, rounded = True, fontsize = 10)

#%%

nuevoDato = {'altura_tot' : [22], 'diametro' : [56], 'inclinacio' : [8]}
datonuevo= pd.DataFrame(nuevoDato)

clf_info.predict(datonuevo)








