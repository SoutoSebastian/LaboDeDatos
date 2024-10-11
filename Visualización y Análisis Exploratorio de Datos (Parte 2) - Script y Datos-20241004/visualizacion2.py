#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase Visualizacion 2. Script clase.
Autor  : Ailen Altamirano
Fecha  : 2024-01-04
"""
#%%
# Importamos bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from   matplotlib import ticker  
from matplotlib import rcParams
import seaborn as sns           

# Carpeta donde se encuentran los archivos a utilizar
#carpeta = "~/Downloads/clase-12/scriptClase/"
#carpeta = "C:/Users/ailen/Desktop/Visualizacion2/"
#carpeta = "~/Escritorio/LaboDeDatos/Visualización y Análisis Exploratorio de Datos (Parte 2) - Script y Datos-20241004/"
carpeta = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\Visualización y Análisis Exploratorio de Datos (Parte 2) - Script y Datos-20241004\\"

#%%##########################################################################
#                                                                           #
#                                TIPS                                       #
#                                                                           #
#############################################################################

# VISUALIZACION - ANALISIS ESTADISTICO - MEDIDAS DE TENDENCIA

# Para aprender a calcular medidad de tendencia usaremos nuevamente el 
# dataset tips
tips = pd.read_csv(carpeta+"tips.csv")  # Cargamos el dataset

# Mostramos las primeras observaciones
tips.head()
    
# Vamos a trabajar con la columna 'tip'

# Calculamos la media
tips['tip'].mean()

# Calculamos la mediana
tips['tip'].median()

# Calculamos la moda
tips['tip'].mode()

#%%#################### MEDIDAS DE DISPERSIÓN ################################

# Calculamos el rango de la columan tip como la diferencia
# entre el valor máximo y el mínimo
rango_tips = max(tips['tip']) - min(tips['tip'])
print(rango_tips) 

# Calculamos el desviación estándar para la columna tip
tips['tip'].std()

# Utilizamos el metodo describe para obtener los valores de
# los percentiles 25, 50 y 75

tips['tip'].describe()


#%% # # # # # # # # # # # # # # # # # # # # # # # 
# #   ventaCasas
# # # # # # # # # # # # # # # # # # # # # # # # 

# Cargamos dataset ventaCasas
ventaCasas= pd.read_csv(carpeta+"ventaCasas.csv")

# Mostramos las primeras observaciones
ventaCasas.head()

# Estadistica Descritiva
ventaCasas.describe()

# Genera el grafico de boxplot (grafico por defecto)
fig, ax = plt.subplots()

ax.boxplot(ventaCasas['PrecioDeVenta'])

# Genera el grafico de boxplot (mejorando la informacion mostrada)    

rcParams['font.family'] = 'sans-serif'           # Modifica el tipo de letra
rcParams['axes.spines.right']  = False            # Elimina linea derecha   del recuadro
rcParams['axes.spines.left']   = True             # Agrega  linea izquierda del recuadro
rcParams['axes.spines.top']    = False            # Elimina linea superior  del recuadro
rcParams['axes.spines.bottom'] = False            # Elimina linea inferior  del recuadro

fig, ax = plt.subplots()

ax.boxplot(ventaCasas['PrecioDeVenta'], showmeans=True)

# Agrega titulo, etiquetas a los ejes 
#y limita el rango de valores de los ejes
ax.set_title('Precio de venta de casas')
ax.set_xticks([])
ax.set_ylabel('Precio de venta ($)')
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("$ {x:,.2f}")); # Agrega separador de decimales y signo $
ax.set_ylim(0,500)


#%%################ VOLVAMOS AL DATASET DE PROPINAS (TIPS) ###################################

# # # # # # # # 
# Genera el grafico de boxplot por sexo
# # # # # # # # 

rcParams['font.family'] = 'sans-serif'           # Modifica el tipo de letra
rcParams['axes.spines.right']  = False            # Elimina linea derecha   del recuadro
rcParams['axes.spines.left']   = True             # Agrega  linea izquierda del recuadro
rcParams['axes.spines.top']    = False            # Elimina linea superior  del recuadro
rcParams['axes.spines.bottom'] = False            # Elimina linea inferior  del recuadro

fig, ax = plt.subplots()

tips.boxplot(by=['sex'], column=['tip'], 
             ax=ax, grid=False, showmeans=True)

# Agrega titulo, etiquetas a los ejes  
fig.suptitle('')
ax.set_title('Propinas')
ax.set_xlabel('Sexo')
ax.set_ylabel('Valor de Propina ($)')

ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("$ {x:,.2f}")); # Agrega separador de decimales y signo $
ax.set_ylim(0,12) #limita el rango de valores de los ejes



#%% # # # # # # # 
# Genera el grafico de boxplot por dia (y agrupado por sexo)
# # # # # # # # 
ax = sns.boxplot(x="day", 
                 y="tip", 
                 hue="sex", 
                 data=tips, 
                 order=['Thur', 'Fri', 'Sat', 'Sun'], 
                 palette={"Female": "orange", "Male": "skyblue" })


ax.set_title('Propinas')
ax.set_xlabel('Día de la Semana')
ax.set_ylabel('Valor de Propina ($)')
ax.set_ylim(0,12)
ax.legend(title="Sexo")
ax.set_xticklabels(['Jueves','Viernes','Sábado','Domingo'])    

#%%########################## EJERCICIO ######################################

# Utilizando el dataset de propinas (tips):
   
    # Generar un gráfico de boxplot de la proporcion 
    # de propina recibida (tip/total_bill)
        # Ayuda: para este punto es necesario que generen una nueva
        # columna en el dataframe (columna con los datos de tip/total_bill)
        
    # Analizar los resultados obtenidos
    
    # Estudiar si hay diferencias en función del sexo y el sexo+día
    
    # Discutir con el resto de la clase los resultados obtenidos

#%% # # # # # # # 
# Genera el grafico de violinplot 
# # # # # # # # 

ax = sns.violinplot(x ="sex", y ="tip", data = tips,
                     palette={"Female": "orange", "Male": "skyblue" })

ax.set_title('Propinas')
ax.set_xlabel('sexo')
ax.set_ylabel('Valor de Propina ($)')
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("$ {x:,.2f}")); # Agrega separador de decimales y signo $
ax.set_ylim(0,12)
ax.set_xticklabels(['Femenino','Masculino'])    