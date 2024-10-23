#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:12:33 2024

@author: Estudiante
"""

import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns           # Para graficar histograma


ruta ="/home/Estudiante/Escritorio/LaboDeDatos/clasee1810/"

archivo = "tiempoReaccion.csv"

archivo2 = "reaccion2.csv"
df = pd.read_csv(ruta+archivo)

df2 = pd.read_csv(ruta+archivo2)
#%%

consulta_sql = """
                SELECT DISTINCT "Nro Estudiante", Tiempo, 
                                CASE 
                                    WHEN Mano LIKE '%zq%' then 'izquierda'
                                    ELSE 'derecha'
                                END AS Mano
                FROM df;
               """

tiempo_reaccion = sql^consulta_sql

#%%

#Histograma:
    
plt.rcParams['font.family'] = 'sans-serif'           # Modifica el tipo de letra
plt.rcParams['axes.spines.right'] = False            # Elimina linea derecha  del recuadro
plt.rcParams['axes.spines.left']  = False            # Elimina linea izquierda  del recuadro
plt.rcParams['axes.spines.top']   = False            # Elimina linea superior del recuadro

fig, ax = plt.subplots()

sns.histplot(data = tiempo_reaccion,
             x = 'Tiempo', 
             bins = 7, 
             hue= 'Mano',                # Coloreamos segun los valores de la columna 'Sex'
             palette = 'colorblind',
             stat='probability')  


# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
ax.set_title('Tiempo Reaccion')
ax.set_xlabel('Tiempo(segundos)')
ax.set_ylabel('Cantidad de repeticiones')



#%%

# Configuración de la visualización
plt.rcParams['font.family'] = 'sans-serif'           
plt.rcParams['axes.spines.right'] = False            
plt.rcParams['axes.spines.left']  = False            
plt.rcParams['axes.spines.top']   = False            

# Crear la figura y los ejes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))


sns.histplot(data=df2,
             x='mano_habil', 
             bins=7, 
             stat='probability', 
             ax=ax1)  
ax1.set_title('Tiempo Reacción Mano Hábil')
ax1.set_xlabel('Tiempo (segundos)')
ax1.set_ylabel('Cantidad de Repeticiones')


sns.histplot(data=df2,
             x='mano_no_habil', 
             bins=8, 
             color = "red",
             stat='probability', 
             ax=ax2)  
ax2.set_title('Tiempo Reacción Mano Inhabil')
ax2.set_xlabel('Tiempo (segundos)')
ax2.set_ylabel('Cantidad de Repeticiones')

xlim_min = min(df2['mano_habil'].min(), df2['mano_no_habil'].min())
xlim_max = max(df2['mano_habil'].max(), df2['mano_no_habil'].max())
ax1.set_xlim(xlim_min, xlim_max)
ax2.set_xlim(xlim_min, xlim_max)




