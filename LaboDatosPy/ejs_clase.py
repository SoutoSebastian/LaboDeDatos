#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 13:19:55 2024

@author: Estudiante
"""

##EJERCICIOS BIEN HECHOS
#%%
import pandas as pd
import numpy as np

#%%

archivo = 'C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\LaboDatosPy\\arbolado-en-espacios-verdes.csv'

df = pd.read_csv(archivo, index_col = 2)

dJ = df[df['nombre_com']=='Jacarandá']

dP = df[df['nombre_com'].str.startswith('Palo')]


cantidad_Jacaranda = dJ['nombre_com'].value_counts(dropna = False)

cantidad_PB = dJ['nombre_com'].value_counts(dropna = False)

dJ['altura_tot'].agg('max')
dP['altura_tot'].agg('max')

#%%
def cantidad_arboles(parque):
    
    dp = dJ[dJ['espacio_ve']==parque]
    
    return len(dp)

#%%

#ej1

def leer_parque(nombre_archivo, parque):
    
    df = pd.read_csv(nombre_archivo, index_col = 2)
    
    df_parques = df[df['espacio_ve']==parque]
    
    lista_parque = []
    
    for e in df_parques.itertuples():
        d = {'long':e.long, 'lat':e.lat, 'altura_tot':e.altura_tot, 'diametro':e.diametro, 
             'inclinacio':e.inclinacio, 'id_especie':e.id_especie, 'nombre_com':e.nombre_com,
             'nombre_cie':e.nombre_cie, 'tipo_folla':e.tipo_folla, 'espacio_ve':e.espacio_ve,
             'ubicacion':e.ubicacion, 'nombre_fam':e.nombre_fam, 'nombre_gen':e.nombre_gen, 
             'origen':e.origen, 'coord_x':e.coord_x, 'coord_y':e.coord_y  }
        
        lista_parque.append(d)
        
    return lista_parque
#%%

#ej2

a = leer_parque(archivo, 'GENERAL PAZ')

def especies(lista_arboles):
    res = []
    
    for i in range(len(lista_arboles)):
        if lista_arboles[i]['nombre_com'] not in res:
            res.append(lista_arboles[i]['nombre_com'])
    
    return res
#%%

#ej3

def contar_ejemplares(lista_arboles):
    res = {}
    
    for i in range (len(lista_arboles)):
        if(lista_arboles[i]['nombre_com'] not in res):
            res[lista_arboles[i]['nombre_com']] = 1
        else:
            res[lista_arboles[i]['nombre_com']] += 1
            
    return res

especiesEnGP = contar_ejemplares(a)

#%%

#ej4

def obtener_alturas(lista_arboles, especie):
    res = []
    
    for i in range(len(lista_arboles)):
        if(lista_arboles[i]['nombre_com'] == especie):
            res.append(lista_arboles[i]['altura_tot'])

    return res

alturas_GP = obtener_alturas(a, 'Jacarandá')

def maximo(l):
    max = -1
    
    for i in range(len(l)):
        if (l[i] > max):
            max = l[i]
    
    return max

def prom(l):
    suma = 0
    for i in range (len(l)):
        suma += l[i]
    
    res = suma / len(l)
    
    return res

#%%

#ej5

def obtener_inclinaciones(lista_arboles, especie):
    res = []
    
    for i in range(len(lista_arboles)):
        if(lista_arboles[i]['nombre_com'] == especie):
            res.append(lista_arboles[i]['inclinacio'])

    return res

#%%

#ej6

def especimen_mas_inclinado(lista_arboles):
    especie: str 
    inclinacion = -1 
    lista_especies = especies(lista_arboles)
    
    for i in range (len(lista_especies)):
        inclinaciones= obtener_inclinaciones(lista_arboles, lista_especies[i])
        max_inclinacion = max(inclinaciones)
        
        if (max_inclinacion > inclinacion):
            especie = lista_especies[i]
            inclinacion = max_inclinacion
    
    return [especie, inclinacion]

#%%

#ej7

def especimen_promedio_mas_inclinada(lista_arboles):
    especie: str 
    inclinacion = -1 
    lista_especies = especies(lista_arboles)
    
    for i in range (len(lista_especies)):
        inclinaciones= obtener_inclinaciones(lista_arboles, lista_especies[i])
        prom_inclinacion = prom(inclinaciones)
        
        if (prom_inclinacion > inclinacion):
            especie = lista_especies[i]
            inclinacion = prom_inclinacion
    
    return [especie, inclinacion]

################EJERCICIO DE ARBOLES EN BSAS CLASE

import pandas as pd
import numpy as np

archivo = 'arbolado-en-espacios-verdes.csv'

df = pd.read_csv(archivo, index_col = 2)

dJ = df[df['nombre_com']== 'Jacarandá'] ##armo el dataframe de jacarandas

dJ['nombre_com'].value_counts(dropna = False) ##cuento la cantidad de arboles (3225)

dJ.sort_values(by = 'altura_tot', ascending = False) ##ordeno por altura decreciente y tengo el mas alto (49)

dJ.sort_values(by = 'altura_tot') ##ordeno por altura creciente (1)

#altura promedio
suma_alturas = 0
for e in dJ.itertuples():
    suma_alturas += e.altura_tot
    
promedio = suma_alturas / 3225

print(str(promedio))  ##10.466046511627907

dJ.sort_values(by = 'diametro', ascending = False) ##(159)

dJ.sort_values(by = 'diametro') ##(1)

#diametro promedio

suma_diametros = 0
for e in dJ.itertuples():
    suma_diametros += e.diametro
    
promediod = suma_diametros / 3225

print(str(promediod))  ##29.072248062015504


def cantidad_arboles3(parque:str):
    res =  (dJ['espacio_ve']==parque).sum()
    print (res)
    
def cantidad_nativos2(parque:str):
    dParque = dJ[dJ['espacio_ve']==parque]
    res = (dParque['origen']=='Nativo/Autóctono').sum()
    print(res)
    
#Palos borrachos ( hay distintos tipos entonces armo el data frame por el nombre_fam)

dPB = df[df['nombre_fam']=='Bombacáceas'] # creo el data frame y despues es todo lo mismo que las otras

#####EJERCICIO

#EJ1
def leer_parque(nombre_archivo, parque):
    df = pd.read_csv(nombre_archivo, index_col = 2)
    
    dP = df[df['espacio_ve']==parque]
    
    return dP

#EJ2
def especies(lista_arboles):
    res = lista_arboles['nombre_com'].unique()
    return res

#EJ3
def contar_ejemplares(lista_arboles):
    res = lista_arboles['nombre_com'].value_counts(dropna = False)
    
    return res

#EJ4
def obtener_alturas(lista_arboles, especie):
    lAlturas = lista_arboles[lista_arboles['nombre_com']==especie]['altura_tot']
    
    return lAlturas

#EJ5
def obtener_inclinaciones(lista_arboles, especie):
    lInclinacion = lista_arboles[lista_arboles['nombre_com']==especie]['inclinacio']
    
    return lInclinacion

#EJ6
def especimen_mas_inclinado(lista_arboles):
    listaEspecies = especies(lista_arboles)
    max = -1
    especie :str
    
    for i in range (len(listaEspecies)):
        inclinacion_por_especie = obtener_inclinaciones(lista_arboles,listaEspecies[i])
        maximo_por_especie = inclinacion_por_especie.agg('max')
        
        if(maximo_por_especie >= max):
            max = maximo_por_especie
            especie = listaEspecies[i]
            
    return [especie, max]

#EJ7
def especie_promedio_mas_inclinada(lista_arboles):
    listaEspecies = especies(lista_arboles)
    maxprom = -1
    especie :str
    
    for i in range (len(listaEspecies)):
        inclinacion_por_especie = obtener_inclinaciones(lista_arboles,listaEspecies[i])
        promedio_por_especie = inclinacion_por_especie.agg('mean')
        
        if(promedio_por_especie >= maxprom):
            maxprom = promedio_por_especie
            especie = listaEspecies[i]
            
    return [especie, maxprom]

#Arboles en veredad

dv = pd.read_csv('arbolado-publico-lineal-2017-2018.csv', index_col = 2)
dv2 = dv[['nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho', 'altura_arbol']]

especies_seleccionadas = ['Tilia x moltkei', 'Jacaranda mimosifolia', 'Tipuana tipu']

#EJ8
#parques:
#creo los dataframes con las columnas pedidas
df_tipas_parques = df[df['nombre_cie']=='Tipuana Tipu'][['diametro','altura_tot']]
df_tipas_veredas = dv[dv['nombre_cientifico']=='Tipuana tipu'][['diametro_altura_pecho','altura_arbol']]

#cambio los nombres para que queden columnas con los mismos nombres en ambos dataframes
df_tipas_veredas = df_tipas_veredas.rename(columns={'diametro_altura_pecho':'diametro'})
df_tipas_parques = df_tipas_parques.rename(columns={'altura_tot':'altura_arbol'})

#EJ9
df_tipas_veredas['ambiente']='vereda'
df_tipas_parques['ambiente']='parque'

#EJ10
df_tipas_vyp = pd.concat([df_tipas_parques, df_tipas_veredas])

#EJ11
#voy a sacar diametro max, min y prom y altura max min y prom para cada dataframe y comparar.

#max
df_tipas_vyp[df_tipas_vyp['ambiente']=='vereda'].agg('max') #diametro = 199, altura = 40
df_tipas_vyp[df_tipas_vyp['ambiente']=='parque'].agg('max') #diametro = 261, altura = 48

#min
df_tipas_vyp[df_tipas_vyp['ambiente']=='vereda'].agg('min') #diametro = 0.0, altura = 2
df_tipas_vyp[df_tipas_vyp['ambiente']=='parque'].agg('min') #diametro = 1, altura = 1

#prom
df_tipas_vyp[df_tipas_vyp['ambiente']=='vereda']['diametro','altura_arbol'].agg('mean') #diametro = 54.142719, altura = 15.056567
df_tipas_vyp[df_tipas_vyp['ambiente']=='parque'].agg('mean') #diametro = 57.994294, altura = 19.100223


            

        
        
        
