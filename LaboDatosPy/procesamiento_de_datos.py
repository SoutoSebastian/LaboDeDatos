[# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:16:01 2024

@author: Sebastián
"""
#%%
#0
empleado_01 = [[20222333, 45, 2, 20000], [33456234, 40, 0, 25000], [45432345, 41, 1, 10000]]

#%%
#1

def superanSalarioActividad01(e, u):
    res = []
    
    for i in range (len(e)):
        if(e[i][3] > u):
            res.append(e[i])
    
    return res

#no costo mucho
#%%

#2

empleado_02 = [[20222333, 45, 2, 20000], [33456234, 40, 0, 25000], [45432345, 41, 1, 10000],
               [43967304, 37, 0, 12000], [42236276, 36, 0, 18000]]
#sigue funcionando

#%%

#3

#no funciona si se cambian las columnas

empleado_03 = [[20222333, 20000, 45, 2], [33456234, 25000, 40, 0], [45432345, 10000, 41, 1],
               [43967304, 12000, 37, 0], [42236276, 18000, 36, 0]]


def superanSalarioActividad3(e, u):
    res = []
    
    for i in range (len(e)):
        if(e[i][1] > u ):
            res.append([e[i][0], e[i][2], e[i][3], e[i][1]])
    
    return res

#%%

#4

empleado_04 = [[20222333, 33456234, 45432345, 43967304, 42236276], 
               [20000, 25000, 10000, 12000,18000], [45,40,41,37,26], [2,0,1,0,0]]

#no funciona con ninguna de las funciones anteriores

def superanSalarioActividad4(e, u):
    res = []
    
    for i in range (len(e[1])):
        if(e[1][i] > u ):
            res.append([e[0][i], e[1][i], e[2][i], e[3][i]])
    
    return res

#%%

#1. cuando se agregaron más filas siguió funcionando bien . cuando se cambio el orden de las
#   columnas tuve que cambiar el indice donde tomaba los salarios para compararlos con el 
#   umbral

#2. cuando se paso a lista de columnas cambie el iterador que estaba usando para ahora iterar
#   sobre los elementos de la columna de indice 1, es decir los salarios.

#3. la ventaja es que el usuario no se preocupa por estos temas de implementacion, donde
#   ademas puede modificar algo y que la funcion ya no haga lo que tiene que hacer  




