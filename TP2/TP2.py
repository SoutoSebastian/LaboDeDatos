# Grupo: Pescado rabioso
# Participantes:
#               -Souto, Sebastian Manuel
#               -Sanza, Gian Lucca
#               -Goldfarb, Bruno

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


#bruno
#prefijo = 'C:/Users/Bruno Goldfarb/Downloads/'

#seba
prefijo = 'C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\TP2\\'

data = pd.read_csv(prefijo + 'TMNIST_Data.csv')

#%%

#con esta función imprimimos las primeras 10 imagenes del dataframe

def imprimir_img (data):
    imagenes = data.iloc[:, 2:] #saco las 2 primeras columnas
    for i in range(10):
        img = np.array(imagenes.iloc[i]).reshape((28,28))
        plt.imshow(img, cmap='gray')
        plt.show()
    

imprimir_img(data)
#%%

#1c
consulta_sql = """
                SELECT DISTINCT * 
                FROM data
                WHERE labels == '0';
               """

img0 = sql^consulta_sql

imprimir_img(img0)

#Se puede observar que la mayoría de las imagenes que corresponden al 0 cumplen que en 
#centro tienen como valor 0. Sin embargo en algunos casos no se cumple, por ejemplo para 
#la fuente Mitr-Bold.

#%%

#EJ 2

#a
#Armo df con digitos 0 y 1

consulta_sql = """
                SELECT DISTINCT * 
                FROM data
                WHERE labels == '0' OR  labels == '1';               
               """
               
img01 = sql^consulta_sql

#Queremos ver si esta balanceado.

consulta_sql = """
                SELECT labels, COUNT(*) AS cantXdigito
                FROM img01
                GROUP BY labels;
               """

cantidadXdigito = sql^consulta_sql

#mismo numero de 0s y 1s, esta balanceado.

#%%
#b

#Primero separamos la data de los labels.

X = data.iloc[:,2:]
Y = data['labels']

#%%
#Separamos en datos de train y test y tomo 3 atributos.

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3) # 70% para train y 30% para test

X_train3 = X_train[[ '186','381', '661']]
X_test3 = X_test[[ '186','381', '661']]


#%%

#ahora realizamos el modelo

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train3, Y_train) 
Y_pred = model.predict(X_test3) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)

#no tiene buena exactitud, pruebo con todos los atributos.

#%%

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)

#aumneta a 0.96

#hay que seguir probando con distintos atributos, ver las metricas y eso.

