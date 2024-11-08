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
from sklearn.metrics import recall_score

#bruno
#prefijo = 'C:/Users/Bruno Goldfarb/Downloads/'

#seba
#prefijo = 'C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\TP2\\'

#labo
ruta ="/home/Estudiante/Escritorio/LaboDeDatos/TP2/"


data = pd.read_csv(ruta + 'TMNIST_Data.csv')


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


#%%

########Pruebo con conjuntos de 3 atributos


#1

#tome 3 atributos al azar 


X_train3 = X_train[[ '186','381', '661']]
X_test3 = X_test[[ '186','381', '661']]


#%%

#ahora realizamos el modelo

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train3, Y_train) 
Y_pred = model.predict(X_test3) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)



recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  # 'macro' es el promedio no ponderado
print(f"Recall : {recall_multiclass:.4f}")

metrics.confusion_matrix(Y_test, Y_pred)


#%%

#2

#tome 3 que se que pocas imagenes tienen valorees distintos de 0 
X_train3 = X_train[[ '200','201', '202']]
X_test3 = X_test[[ '200','201', '202']]

#%%

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train3, Y_train) 
Y_pred = model.predict(X_test3) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)



recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  # 'macro' es el promedio no ponderado
print(f"Recall : {recall_multiclass:.4f}")

metrics.confusion_matrix(Y_test, Y_pred)

#muy baja se debe a que estas posiciones corresponden al borde

#%%

#3

#tomo 3 atributos a proposito que se que tienen valores en la mayoria de los numeros

X_train3 = X_train[[ '294','322', '550']]
X_test3 = X_test[[ '294','322', '550']]

#%%

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train3, Y_train) 
Y_pred = model.predict(X_test3) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)



recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  # 'macro' es el promedio no ponderado
print(f"Recall : {recall_multiclass:.4f}")

metrics.confusion_matrix(Y_test, Y_pred)

#exactitud y recall parecida a la del primer caso.


#%%
#Tomo los del 3) y modifico el numero de los vecinos a ver que pasa:
    
model = KNeighborsClassifier(n_neighbors = 12)
model.fit(X_train3, Y_train) 
Y_pred = model.predict(X_test3) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
metrics.confusion_matrix(Y_test, Y_pred)



recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  # 'macro' es el promedio no ponderado
print(f"Recall : {recall_multiclass:.4f}")

metrics.confusion_matrix(Y_test, Y_pred)

#aumenta un poco la exactitud, pero no obtendremos un buen modelo en terminos de exactitud.
#Ya que 3 atributos no son representativos.

#%%

#########Me fijo que pasa con todos los atributos.

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))
#aumneta a 0.96

recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  # 'macro' es el promedio no ponderado
print(f"Recall : {recall_multiclass:.4f}")
metrics.confusion_matrix(Y_test, Y_pred)

#%%

#########Quiero ver que pasa si saco los bordes. 

X = data.iloc[:,92:696]

#%%
#Separamos en datos de train y test y tomo 3 atributos.

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3) # 70% para train y 30% para test

#%%

model = KNeighborsClassifier(n_neighbors = 5)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))


recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  
print(f"Recall : {recall_multiclass:.4f}")
metrics.confusion_matrix(Y_test, Y_pred)


##descartando 184 atributos tenemos una precision parecida.

#%%
#y si aumento el numero de vecinos?

model = KNeighborsClassifier(n_neighbors = 100)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))


recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  
print(f"Recall : {recall_multiclass:.4f}")
metrics.confusion_matrix(Y_test, Y_pred)

#Exactitud del modelo: 0.9460423634336678

#%%

model = KNeighborsClassifier(n_neighbors = 1000)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))


recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  
print(f"Recall : {recall_multiclass:.4f}")
metrics.confusion_matrix(Y_test, Y_pred)

#vemos como al aumentar el numero de vecinos esta provocando que baje la exactitud y el recall

#%% 
#y si pongo solo 1 vecino?


model = KNeighborsClassifier(n_neighbors = 1)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))


recall_multiclass = recall_score(Y_test, Y_pred, average='macro')  
print(f"Recall : {recall_multiclass:.4f}")
metrics.confusion_matrix(Y_test, Y_pred)

#bastante bueno con 1. 











