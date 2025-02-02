#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 22:04:07 2023

@author: mcerdeiro
"""
#%% modulos

from inline_sql import sql, sql_val
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import tree
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

#%%######################

        ####            Cargo dataset

#########################
#%%        


iris = load_iris(as_frame = True)

data = iris.frame
X = iris.data
Y = iris.target

iris.target_names
diccionario = dict(zip( [0,1,2], iris.target_names))
#%%######################

        ####            Un primer modelo

#########################
#%%  
model = KNeighborsClassifier(n_neighbors = 5) # modelo en abstracto
model.fit(X, Y) # entreno el modelo con los datos X e Y
Y_pred = model.predict(X) # me fijo qué clases les asigna el modelo a mis datos
metrics.accuracy_score(Y, Y_pred)
metrics.confusion_matrix(Y, Y_pred)

#%%        
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3) # 70% para train y 30% para test

model = KNeighborsClassifier(n_neighbors = 5) # modelo en abstracto
model.fit(X_train, Y_train) # entreno el modelo con los datos X_train e Y_train
Y_pred = model.predict(X_test) # me fijo qué clases les asigna el modelo a mis datos X_test
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)
#%%

# ¿QUÉ PASA SI REPETIMOS CON OTRO SPLIT?

#%%

Nrep = 5
valores_n = range(1, 20)

resultados_test = np.zeros((Nrep, len(valores_n)))
resultados_train = np.zeros((Nrep, len(valores_n)))


for i in range(Nrep):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
    for k in valores_n:
        model = KNeighborsClassifier(n_neighbors = k)
        model.fit(X_train, Y_train) 
        Y_pred = model.predict(X_test)
        Y_pred_train = model.predict(X_train)
        acc_test = metrics.accuracy_score(Y_test, Y_pred)
        acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
        resultados_test[i, k-1] = acc_test
        resultados_train[i, k-1] = acc_train

#%%

promedios_train = np.mean(resultados_train, axis = 0) 
promedios_test = np.mean(resultados_test, axis = 0) 
#%%

plt.plot(valores_n, promedios_train, label = 'Train')
plt.plot(valores_n, promedios_test, label = 'Test')
plt.legend()
plt.title('Exactitud del modelo de knn')
plt.xlabel('Cantidad de vecinos')
plt.ylabel('Exactitud (accuracy)')
#%%

#%%

# ¿QUÉ PASA SI REPETIMOS MÁS VECES?

#%%


#ejercicio.

ruta ="/home/Estudiante/Escritorio/LaboDeDatos/Clase 17 - archivos-20241101/"
archivo = "alturas.csv"

df = pd.read_csv(ruta+archivo)


#%%


consulta_sql = """
                SELECT id, altura, CASE 
                                        WHEN genero == 'M' then '1'
                                        ELSE '0'
                                    END AS genero , contextura_madre, altura_madre
                FROM df;
               """

nuevodf = sql^consulta_sql

#%%

consulta_sql = """
                SELECT *
                FROM df
                WHERE genero == 'M';
               """
               
nuevodf = sql^consulta_sql           
#%%

Y = df['altura']
X = df.altura_madre
X = X.values.reshape(-1,1)

#%%
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3) # 70% para train y 30% para test

model = KNeighborsRegressor(n_neighbors = 5) # modelo en abstracto
model.fit(X, Y)

        
        
        
        
        
        
        
        
        
        
        
        
        
        