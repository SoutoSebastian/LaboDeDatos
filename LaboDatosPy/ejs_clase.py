#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 13:19:55 2024

@author: Estudiante
"""
#%%
import pandas as pd
import numpy as np

#%%

archivo = 'arbolado-en-espacios-verdes.csv'

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

def leer_parque(nombre_archivo, parque):
    
    df = pd.read_csv(nombre_archivo, index_col = 2)
    
    df_parques = df[df['espacio_ve']==parque]
    
    lista_parque = []
    
    for e in dJ.itertuples():
        d = {'long':e.long, 'lat':e.lat, 'altura_tot':e.altura_tot, 'diametro':e.diametro, 
             'inclinacio':e.inclinacio, 'id_especie':e.id_especie, 'nombre_com':e.nombre_com,
             'nombre_cie':e.nombre_cie, 'tipo_folla':e.tipo_folla, 'espacio_ve':e.espacio_ve,
             'ubicacion':e.ubicacion, 'nombre_fam':e.nombre_fam, 'nombre_gen':e.nombre_gen, 
             'origen':e.origen, 'coord_x':e.coord_x, 'coord_y':e.coord_y  }
        
        lista_parque.append(d)
        
    return lista_parque
#%%

a = leer_parque(archivo, 'GENERAL PAZ')

        
        
        