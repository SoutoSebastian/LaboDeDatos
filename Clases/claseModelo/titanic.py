#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:01:49 2024

@author: Estudiante
"""

import numpy as np
import pandas as pd
from inline_sql import sql, sql_val
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns 


ruta ="/home/Estudiante/Escritorio/LaboDeDatos/claseModelo/"

archivo = "titanic_training.csv"

archivo2 = "titanic_competencia.csv"
df_c = pd.read_csv(ruta+archivo2)
df = pd.read_csv(ruta+archivo)

#%%

consulta_sql = """
                SELECT DISTINCT Sex, COUNt(Survived) AS cant_sobrevivientes
                FROM df
                WHERE Survived == 1
                GROUP BY Sex
               """

sobrevivientesXSexo = sql^consulta_sql

mujeres = sql^"""SELECT DISTINCT COUNT(Sex)
                  FROM df
                  WHERE Sex = 'female' AND Pclass = 1
                  """

consulta_sql = """
                SELECT DISTINCT Pclass, COUNt(Pclass)
                FROM df
                WHERE Survived == 1
                GROUP BY Pclass;
               """

sobrevivientesXclase = sql^consulta_sql

cantidad1 = sql^"""SELECT DISTINCT COUNT(Pclass)
                  FROM df
                  WHERE Pclass = 1
                  """

consulta_sql = """
                SELECT DISTINCT COUNT(Age)
                FROM df
                WHERE Survived == 1 AND Age < 10
               """

sobrevivientesNiños = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT Sex, COUNt(Survived) AS cant_sobrevivientes
                FROM df
                WHERE Survived == 1 AND Pclass ==1 
                GROUP BY Sex
               """

sobrevivientesXSexo1 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT Sex, COUNt(Survived) AS cant_sobrevivientes
                FROM df
                WHERE Survived == 1 AND Pclass = 3 AND Age> 40
                GROUP BY Sex
               """

sobrevivientesXSexo3 = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT Count(Sex)
                FROM df
                WHERE  Sex == 'male' AND Pclass = 3 AND Age > 40
                GROUP BY Sex
               """

mujeres3 = sql^consulta_sql
#%%


def clasificador_titanic(x):
    vive = False
    
    if (x.Sex == 'female') and (x.Pclass < 3):
        vive = True
    elif (x.Sex == 'male') and (x.Pclass == 1) and x['Age'] < 18:
        vive = True
    elif (x.Sex == 'female') and (x.Pclass == 3) and (x.Age > 50 or x.Age < 18) :
        vive = True
    
    return vive


for i in range(0,10):
    print(clasificador_titanic(df_c.iloc[i]))