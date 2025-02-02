# Grupo: Pescado rabioso
# Participantes:
#               -Souto, Sebastian Manuel
#               -Sanza, Gian Lucca
#               -Goldfarb, Bruno
import os
from inline_sql import sql, sql_val
from pathlib import Path
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import tree
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import random as rd
import copy 
from sklearn.metrics import  precision_score, recall_score

ruta_base = Path(__file__).parent

os.chdir(ruta_base)

prefijo="TablasLimpias/"

data = pd.read_csv('TMNIST_Data.csv')


#%%

#################ANALISIS EXPLORATORIO##########

#con esta función imprimimos las primeras 10 imagenes del dataframe

def imprimir_img (data):
    imagenes = data.iloc[:, 2:] #saco las 2 primeras columnas
    for i in range(10):
        img = np.array(imagenes.iloc[i]).reshape((28,28))
        plt.imshow(img, cmap='gray')
        plt.show()
    
#%%

X = data.iloc[:,2:]
Y = data['labels']


#%%
#ia)
n = 200
indices = []
for i in range(n):
    indice = rd.randint(0,29899)
    indices.append(indice)        
muestreo = X.iloc[indices]    
promedios = muestreo.mean(axis=0).tolist()
muestreo.loc[len(muestreo)] = promedios

#%%

# muestreo, prom = sacarPromedioAleatorio(X, n)    
def dibujarPromedio(muestreo):
    n = 200
    img = np.array(muestreo.iloc[n]).reshape((28,28))
    plt.imshow(img, cmap='gray')
    plt.show()
dibujarPromedio(muestreo)
#%%
#1a figura 1
consulta_sql = """
                SELECT DISTINCT * 
                FROM data
                WHERE labels == '2' or labels == '5';               
               """             
img1 = sql^consulta_sql
n = 500
indices = []
data1 = img1.iloc[:,2:]
for i in range(n):
    indice = rd.randint(0, data1.shape[0])
    indices.append(indice)
muestreo = data1.iloc[indices]
promedios = muestreo.mean(axis=0).tolist()
img2 = np.array(promedios).reshape((28,28))
plt.imshow(img2, cmap='gray')
plt.show()
#%%
#1b figura 2
consulta_sql = """
                SELECT DISTINCT * 
                FROM data
                WHERE labels == '6' or labels == '8';               
               """             
img1 = sql^consulta_sql
n = 500
indices = []
data1 = img1.iloc[:,2:]
for i in range(n):
    indice = rd.randint(0, data1.shape[0])
    indices.append(indice)
muestreo = data1.iloc[indices]
promedios = muestreo.mean(axis=0).tolist()
img2 = np.array(promedios).reshape((28,28))
plt.imshow(img2, cmap='gray')
plt.show()
#%%
#1c figura 3
consulta_sql = """
                SELECT DISTINCT * 
                FROM data
                WHERE labels == '0';               
               """             
img1 = sql^consulta_sql
n = 100
indices = []
data1 = img1.iloc[:,2:]
for i in range(n):
    indice = rd.randint(0, data1.shape[0])
    indices.append(indice)
muestreo = data1.iloc[indices]
promedios = muestreo.mean(axis=0).tolist()
img2 = np.array(promedios).reshape((28,28))
plt.imshow(img2, cmap='gray')
plt.show()
#%% 
#1C, figura 4
consulta_sql = """
                SELECT DISTINCT * 
                FROM data
                WHERE labels == '0';               
               """             
img1 = sql^consulta_sql
n = 3
indices = []
data1 = img1.iloc[:,2:]
for i in range(n):
    indice = rd.randint(0, data1.shape[0])
    indices.append(indice)
muestreo = data1.iloc[indices]
promedios = muestreo.mean(axis=0).tolist()
img2 = np.array(promedios).reshape((28,28))
plt.imshow(img2, cmap='gray')
plt.show()

#%%

######PUNTO 2: KNN###############


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

X = img01.iloc[:,2:]
Y = img01['labels']


#%%
#Separamos en datos de train y test.

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 42) # 70% para train y 30% para test






#%%

#defino una funcion que me arme el modelo de knn:
    
def modelo_knn(X_train, X_test, Y_test, Y_train,k):
    
    model = KNeighborsClassifier(n_neighbors = k)
    model.fit(X_train, Y_train) 
    Y_pred = model.predict(X_test) 

    print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))

    recall = recall_score(Y_test, Y_pred, pos_label=1) 
    print("Recall:", recall)

    precision = precision_score(Y_test, Y_pred, pos_label=1)  
    print("Precisión:", precision)

    print(metrics.confusion_matrix(Y_test, Y_pred))

#%%

#########Me fijo que pasa con todos los atributos.

modelo_knn(X_train, X_test, Y_test, Y_train, 5)

#Muy buenas metricas pero se que hay muchos atributos que se podrian descartar.


#%%

#########Quiero ver que pasa si saco los bordes. 

X_trainsb = X_train.iloc[:,92:696]
X_testsb = X_test.iloc[:,92:696]


#%%

modelo_knn(X_trainsb, X_testsb, Y_test, Y_train, 5)

#sacamos 180 atributos y las metricas siguen siendo muy buenas. Quiero disminuir la
#cantidad de atributos.

#%%

########Pruebo con conjuntos de 3 atributos


#1

#tome 3 atributos al azar 


X_train3 = X_train[[ '170','381', '661']]

X_test3 = X_test[[ '170','381', '661']]


#%%

modelo_knn(X_train3, X_test3, Y_test, Y_train, 5)


#no son malas las metricas, quiero ver si tomando a proposito otros valores tenemos mejores 
#o peores.
#%%
#2

#tome 3 que se que pocas imagenes tienen valorees distintos de 0 
X_train3 = X_train[[ '165','174', '782']]
X_test3 = X_test[[ '165','174', '782']]

#%%

modelo_knn(X_train3, X_test3, Y_test, Y_train, 5)
#manda a todos los datos al 0 o al 1. 


#%%
#3

#tomo 3 atributos a proposito que se que tienen valores en la mayoria de los numeros

X_train3 = X_train[[ '294','322', '550']]
X_test3 = X_test[[ '294','322', '550']]


#%%

modelo_knn(X_train3, X_test3, Y_test, Y_train, 5)
#Metricas parecidas a las del primer caso pero pueden mejorar

#%%
# figura 5
#Con esta imagen observamos donde estan las diferencias entre los 0s y los 1s.

n = 500
indices = []
data1 = img01.iloc[:,2:]
for i in range(n):
    indice = rd.randint(0, data1.shape[0])
    indices.append(indice)
muestreo = data1.iloc[indices]
promedios = muestreo.mean(axis=0).tolist()
img2 = np.array(promedios).reshape((28,28))


plt.imshow(img2, cmap='gray')
plt.show()
#%%
#Voy a probar con un solo atributo, que seria el del medio:

X_train1 = X_train[[ '406']]
X_test1 = X_test[[ '406']]

#%%

modelo_knn(X_train1, X_test1, Y_test, Y_train, 5)

#para ser un solo atributo esta bastante bien, voy a probar de agarrar 3 del medio.

#%%
#Voy a tomar 3 atributos del medio.

X_train3 = X_train[[ '406', '520', '462']]
X_test3 = X_test[[ '406', '520', '462']]

modelo_knn(X_train3, X_test3, Y_test, Y_train, 5)

#Logramos hacer que las metrcias suban eligiendo atributos que sabemos que pueden
#diferenciar a los 1s de los 0s.
#%%
#Finalmente tomo 7 atributos que peretencen a pixeles del centro

X_train7 = X_train[[ '406', '377', '378', '399','422','520','462']]
X_test7 = X_test[[ '406', '377', '378', '399','422','520','462']]

modelo_knn(X_train7, X_test7, Y_test, Y_train, 5)


#%%
#Con los 7 atributos dados anteriormente, voy a ir variando la cantidad de vecinos y comparar

exactitudes = []
recalls = []
precisiones = []
indices = []

for k in range (5,800,30):
    
    model = KNeighborsClassifier(n_neighbors = k)
    model.fit(X_train7, Y_train) 
    Y_pred = model.predict(X_test7) 

    exactitud = metrics.accuracy_score(Y_test, Y_pred)
    recall = recall_score(Y_test, Y_pred, pos_label=1) 
    precision = precision_score(Y_test, Y_pred, pos_label=1)  
    
    indices.append(k)
    exactitudes.append(exactitud)
    recalls.append(recall)
    precisiones.append(precision)
    
#%%
#figura 6
#Ahora quiero graficar los resultados:

fig, ax = plt.subplots(figsize=(10,10))
    
plt.scatter(indices,exactitudes, c='blue',label='Exactitud', alpha=0.6, edgecolors='w', s=20)
plt.scatter(indices,recalls, c='red',label='Recall', alpha=0.6, edgecolors='w', s=20)
plt.scatter(indices,precisiones, c='green',label='Precisión', alpha=0.6, edgecolors='w', s=20)


plt.plot(indices, exactitudes, c='blue', alpha=0.6)  # Línea azul para Exactitud
plt.plot(indices, recalls, c='red', alpha=0.6)      # Línea roja para Recall
plt.plot(indices, precisiones, c='green', alpha=0.6) # Línea verde para Precisión

plt.title('Métricas en función de vecinos', fontsize=16)
plt.xlabel('Cantidad de vecinos', fontsize=14)
plt.ylabel('Valor métrica', fontsize=14)

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Métrica')
plt.show()    

 

#%%

###########PUNTO 3: ARBOLES DE DECISION################
#3. (Clasificación multiclase) 
X = data.iloc[:,2:]
Y = data['labels']
#separo el modelo en train, testing y validation:
    
X_D, X_validation, Y_D, Y_validation = train_test_split(X, Y, test_size = 0.2) # 80% para train y 20% para validation



X_train, X_test, Y_train, Y_test = train_test_split(X_D, Y_D, test_size = 0.3) #70% para train y 30% para testing


def metricas(pred,obtenido):

    acc_test = metrics.accuracy_score(obtenido, pred)
    prec_test = metrics.precision_score(obtenido,pred,average="weighted")
    recall_test=metrics.recall_score(obtenido, pred,average="weighted")

    return acc_test, prec_test, recall_test





#%%        

cnombres = ['0', '1', '2', '3', '4', '5', '6', '7','8','9']

#PROBAMOS CON DISTINTAS PROFUNDIDAES:
    
#depth= 1

arbol = tree.DecisionTreeClassifier(criterion = "entropy", max_depth= 1)
arbol = arbol.fit(X_train, Y_train)

Y_pred = arbol.predict(X_test)

acc, prec, recall=metricas(Y_pred,Y_test)




plt.figure(figsize= [15,10])
tree.plot_tree(arbol,filled = True, rounded = True, fontsize = 10,class_names=cnombres)

#%%
#depth =5
arbol = tree.DecisionTreeClassifier(criterion = "entropy", max_depth= 5)
arbol = arbol.fit(X_train, Y_train)

Y_pred = arbol.predict(X_test)
Y_pred_train = arbol.predict(X_train)

acc, prec, recall=metricas(Y_pred,Y_test)

plt.figure(figsize= [15,10])
tree.plot_tree(arbol,filled = True, rounded = True, fontsize = 10,class_names=cnombres)


#%%
#depth =10
arbol = tree.DecisionTreeClassifier(criterion = "entropy", max_depth= 10)
arbol = arbol.fit(X_train, Y_train)

Y_pred = arbol.predict(X_test)
Y_pred_train = arbol.predict(X_train)

acc, prec, recall=metricas(Y_pred,Y_test)


plt.figure(figsize= [15,10])
tree.plot_tree(arbol,filled = True, rounded = True, fontsize = 10,class_names=cnombres)


#%%
#PELIGRO AL CORRER ESTO TARDA MUCHISIMO!!!!!!!!!!!

Nrep = 5
valores_n = range(1, 11)

resultados_test_gini_acc = np.zeros((Nrep, len(valores_n)))
resultados_train_gini_acc = np.zeros((Nrep, len(valores_n)))
resultados_test_gini_prec = np.zeros((Nrep, len(valores_n)))
resultados_train_gini_prec = np.zeros((Nrep, len(valores_n)))
resultados_test_gini_recall= np.zeros((Nrep, len(valores_n)))
resultados_train_gini_recall= np.zeros((Nrep, len(valores_n)))

criterion= ["entropy","gini"]

for i in range(Nrep):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
    for k in valores_n:
        model = tree.DecisionTreeClassifier(criterion = 'gini', max_depth= k)
        model.fit(X_train, Y_train) 
        Y_pred = model.predict(X_test)
        Y_pred_train = model.predict(X_train)
        acc, prec, recall=metricas(Y_pred,Y_test)
        
        resultados_test_gini_acc[i, k-1] = acc
#        resultados_train_gini_acc[i, k-1] = acc_train
        resultados_test_gini_prec[i, k-1] = prec
#        resultados_train_gini_prec[i, k-1] = prec_train
        resultados_test_gini_recall[i, k-1] = recall
#        resultados_train_gini_recall[i, k-1] = recall_train 
        
resultados_test_entropy_acc = np.zeros((Nrep, len(valores_n)))
#resultados_train_entropy_acc = np.zeros((Nrep, len(valores_n)))
resultados_test_entropy_prec = np.zeros((Nrep, len(valores_n)))
#resultados_train_entropy_prec = np.zeros((Nrep, len(valores_n)))
resultados_test_entropy_recall= np.zeros((Nrep, len(valores_n)))
#resultados_train_entropy_recall= np.zeros((Nrep, len(valores_n)))
      
for i in range(Nrep):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
    for k in valores_n:
        model = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= k)
        model.fit(X_train, Y_train) 
        Y_pred = model.predict(X_test)
        Y_pred_train = model.predict(X_train)
        acc, prec, recall=metricas(Y_pred,Y_test)

        resultados_test_entropy_acc[i, k-1] = acc
#        resultados_train_entropy_acc[i, k-1] = acc_train
        resultados_test_entropy_prec[i, k-1] = prec
#        resultados_train_entropy_prec[i, k-1] = prec_train
        resultados_test_entropy_recall[i, k-1] = recall
#        resultados_train_entropy_recall[i, k-1] = recall_train

#%%




promedios_test_gini_acc= np.mean(resultados_test_gini_acc,axis=0)


promedios_test_entropy_acc= np.mean(resultados_test_entropy_acc,axis=0)


promedios_test_gini_prec= np.mean(resultados_test_gini_prec,axis=0)


promedios_test_entropy_prec= np.mean(resultados_test_entropy_prec,axis=0)


prom_recalls_v_gini = np.mean(resultados_test_gini_recall,axis=0)


prom_recalls_v_entropy = np.mean(resultados_test_entropy_recall,axis=0)

#En todos los casos, mientrsa mas preguntas hacmoes, mejor precision y accuracy tiene el modelo.
#pero con 10 tarda mucho. Definimos por usar depth = 9
#%%
#Ahora salgamos al mundo real, y con el modelo de depth = 9 intentemos predecir:
model = tree.DecisionTreeClassifier(criterion = 'gini', max_depth= 9)
model.fit(X, Y) 
Y_pred = model.predict(X_validation)
Y_pred_train = model.predict(X)
matriz=metrics.confusion_matrix(Y_validation, Y_pred)

#%%

acc, prec, recall=metricas(Y_pred,Y_validation)

#%%
#figura 8
#grafico Gini K-FOLD

plt.scatter(valores_n,promedios_test_gini_acc, c='blue',label='Exactitud', alpha=0.6, edgecolors='w', s=20)
plt.scatter(valores_n,promedios_test_gini_prec, c='red',label='Recall', alpha=0.6, edgecolors='w', s=20)
plt.scatter(valores_n,prom_recalls_v_gini, c='green',label='Precisión', alpha=0.6, edgecolors='w', s=20)


plt.plot(valores_n, promedios_test_gini_acc, c='blue', alpha=0.6)  # Línea azul para Exactitud
plt.plot(valores_n, prom_recalls_v_gini, c='red', alpha=0.6)      # Línea roja para Recall
plt.plot(valores_n, promedios_test_gini_prec, c='green', alpha=0.6) # Línea verde para Precisión

plt.title('Métricas en función de profundidad del arbol GINI', fontsize=16)
plt.xlabel('Depth', fontsize=14)
plt.ylabel('Valor métrica', fontsize=14)

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Métrica')
plt.show()    

#%%
#grafico Entropy K-FOLD

plt.scatter(valores_n,promedios_test_entropy_acc, c='blue',label='Exactitud', alpha=0.6, edgecolors='w', s=20)
plt.scatter(valores_n,promedios_test_entropy_prec, c='red',label='Recall', alpha=0.6, edgecolors='w', s=20)
plt.scatter(valores_n,prom_recalls_v_entropy, c='green',label='Precisión', alpha=0.6, edgecolors='w', s=20)


plt.plot(valores_n, promedios_test_entropy_acc, c='blue', alpha=0.6)  # Línea azul para Exactitud
plt.plot(valores_n, prom_recalls_v_entropy, c='red', alpha=0.6)      # Línea roja para Recall
plt.plot(valores_n, promedios_test_entropy_prec, c='green', alpha=0.6) # Línea verde para Precisión

plt.title('Métricas en función de profundidad del arbol ENTROPY', fontsize=16)
plt.xlabel('Depth', fontsize=14)
plt.ylabel('Valor métrica', fontsize=14)

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Métrica')
plt.show()    





