#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:23:11 2024

@author: mcerdeiro
"""

import pandas as pd
import numpy as np


#%% armo un dataframe a partir de un diccionario
d = {'nombre':['Antonio', 'Brenda', 'Camila', 'David', 'Esteban', 'Felicitas'], 'apellido': ['Restrepo', 'Saenz', 'Torres', 'Urondo', 'Valdes', 'Wainstein'], 'lu': ['78/23', '449/22', '111/24', '1/21', '201/06', '47/20'], 'nota1': [9, 7, 7, 4, 3, np.nan], 'nota2': [10, 6, 7, 8, 5, np.nan], 'aprueba': [True, True, True, False, False, np.nan]}

df = pd.DataFrame(data = d) # creamos un df a partir de un diccionario
df.set_index('lu', inplace = True) # seteamos una columna como index
#%%
df.head()   
df.tail()
df.info() 
df.dtypes
df.columns  
df.index
df.describe() 
df[['nombre', 'nota1']]
df['nombre']
df.iloc[2]
df.iloc[2:6]
df.loc['78/23']
df.loc['78/23', 'nombre']
df.sample()
df.sample(n = 3)

#%% manejo de valores NaN

df.isna()  ##te da el dataFrame con True o False si es nan o no.

df.notna()  ##te da el dataFrame con True o False si no es nan o si es.

df.dropna()  ##te saca toda la fila que tiene valores nan.

df.dropna(axis='columns') ##te saca toda la columna que tiene algun valor nan.

df.dropna(how='all') # solo si TODA la fila es nula

df.dropna(thresh=2) # solo si tiene muy pocos campos (trhesh) no-nan <2

df.dropna(subset=['nombre', 'apellido'])
                                                ## te saca la fila que tenga nan en esas columnas
df.dropna(subset=['nota1', 'apellido'])

df.fillna(0) #te cambia los nan por 0

values = {"nota1": 0, "nota2": 0, "aprueba": False}     #te llena los valores nan en las columnas con esos valores.
df.fillna(value=values)


#%% ordenar por alguna columna 
df.sort_values(by= 'nombre', ascending = False)


#%% modificar una o varias entradas

df.loc['1/21', 'nombre'] = 'Daniel' # modifico la entrada accediendo a la ubicación por fila (index) y columna (nombre de la columna) y defino el nuevo valor con '='

df 

df.replace({'nombre': {'David': 'Daniel'}}) # modifico todas las apariciones de David
df

### OJO - un caso es inplace, el otro no.

df.replace(7, 8)

df.replace({7: 8, 3: 2})

df.replace({'nota2': {7: 9, 5: 6}})

df.astype({'nota2': 'float'})  # cambio de tipo

#%% modificar nombres de las columnas
df.rename(columns={"nota1": "Parcial1", "nota2": "Parcial2"})


#%% calcular promedio y otras cosas

df.agg('min')
df.agg(['sum', 'min', 'max', 'mean'])

df['promedio'] = (df['nota1'] + df['nota2'])/2


#%%
df.all() # solo para variables booleanas (OJO --> si no es bool es todo es True salvo el caso vacío)
df.any()

df.isna().all()
df.isna().any()

df['aprueba'].all()
df['aprueba'].any()

#%% otros "drop" - eliminar partes del df

df.drop(['78/23'], axis = 0) # tiro la fila con index = 78/23

df.drop(['apellido', 'nombre'], axis = 1) # tiro las columnas apellido y nombre

df.duplicated() # dice True en las filas que están duplicadas (luego de la primera aparición)

df.duplicated(keep=False) # dice True en las filas que están duplicadas (incluyendo la primera aparición)

df.duplicated(subset=['nota1'])

df.duplicated(subset=['nota1'], keep = False)

df.drop_duplicates()

df.drop_duplicates(subset=['nota1'])

df.drop_duplicates(subset=['nota1'], keep = 'last')

#%% chequear condiciones

df == 7

df.eq(7)

df!= 7

df.isin([6, 7])

~df.isin([6, 7])

df.isin({'nota1': [6,7]})

#%% otras funciones aplicables al df

df.eval('nota_final = nota1 + 1')

df.eval('promedio = 0.5*nota1 + 0.5*nota2') ##le agrega una columna al dataframe.


df.applymap(lambda x: len(str(x))) # defino la funcion acá mismo

df[['nombre']].applymap(lambda x: x.upper())

df[['nota1']].applymap(lambda x: x*10)

# puedo armar la función aparte o dentro del applymap con lambda
def f(x):
    res = x+1
    return res

df[['nota1']].applymap(f)

df[['nota1']].applymap(lambda x: x + 1)


df[['nota1', 'nota2']].transform(lambda x: x*10)
#%% iterar sobre las filas
df.iterrows()

for e in df.iterrows():
    print(e)

for i, e in df.iterrows():
    print(i, e['nombre'])


df.itertuples()

for e in df.itertuples():
    print(e)
    
for e in df.itertuples():
    print(e.nombre)

for e in df.itertuples():
    print(e.Index)
    
lista_ingresantes_pandemia = []
for e in df.itertuples():
    ingreso = int(e.Index.split('/')[1])
    if ingreso in [20, 21]:
        lista_ingresantes_pandemia.append((e.apellido, e.nombre))


#%% concatenar con otro dataframe
d2 = {'nombre':['Gregoria', 'Horacio'], 'apellido': ['Pérez', 'Quirno'], 'lu': ['09/23', '657/21'], 'nota1': [2,10], 'nota2': [7, 8], 'aprueba': [False, True]}

df_nuevo = pd.DataFrame(data = d2)
df_nuevo.set_index('lu', inplace = True) 

pd.concat([df, df_nuevo])

#%% armar una copia

df_copia = df.copy()
#%% guardar el dataframe como archivo csv

df.to_csv('planilla')



#%% FILTROS

df['nota1']>=7 # nos da una serie booleana, que indica donde se cumple la condición
# el index de esta serie es el del df

(df['nota1']>=7).sum()

df[df['nota1']>=7] # nos da el sub-dataframe donde se cumple la condición

df[ (df['nota1']>=7) & (df['nota2']>=7)]

df[ df['nota1']== 7]


df[ df['nota1'].isin([7,4])]

df[(df['nota2'] <=7) & df['aprueba']]

df[(df['nota2'] <=7) | df['aprueba']]

#%% otras cosas
a = df.to_numpy() # con tipos mixtos no

d = df[['nota1', 'nota2']].dropna().to_numpy()

df['nota1'].unique() ##todos los valores que hay sacando repetidos

df['nota1'].value_counts(dropna = False) ##cuantas veces hay cada valor

df.where(df['nota1'] > 6, 0) # donde no es mayor a 6 pongo 0

#Algunas cosas de la clase
#Abriendo archivos
# con '../Descargas/datame.txt' voy armando el path para llegar al archivo

nombre_archivo = 'datame.txt'

f = open(nombre_archivo, 'rt')

data = f.read()

print(data)
f.read()
f.close()

promedio = (df['nota1']+df['nota2'])/2
df['promedio'] = promedio

alu_nue = {'lu':['125/45'], 'nombre':['Juan'], 'apellido':['Perez'], 'nota1':[2], 'nota2':[10]}

df_alu_nue = pd.DataFrame(data = alu_nue)
df_alu_nue.set_index('lu', inplace = True)

df_nuevo = pd.concat([df, df_alu_nue])

df_nuevo.loc['125/45', 'promedio'] = 1

df_nuevo.loc['125/45', 'promedio'] = (df_nuevo.loc['125/45','nota1'] + df_nuevo.loc['125/45', 'nota2'])/2

df_nuevo['aprueba'] = (df_nuevo['nota1'] >= 5) & (df_nuevo['nota2'] >= 5)

df_nuevo['promociona'] = (df_nuevo['nota1'] >= 8) & (df_nuevo['nota2'] >= 8)

df_aprobados = df_nuevo[df_nuevo['nota1']>=5]
