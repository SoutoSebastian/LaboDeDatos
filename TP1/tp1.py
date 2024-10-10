# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:39:08 2024

@author: Sebastián
"""

import numpy as np
import pandas as pd
from inline_sql import sql, sql_val

ruta = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\TP1\\"

archivo_secciones = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\TP1\\lista-secciones.csv"
archivo_migraciones = 'datos_migraciones.csv'
archivo_completo = 'lista-sedes-completos.csv'
archivo_basico ='lista-sedes-basicos.csv'

datos_secciones = pd.read_csv(archivo_secciones)
datos_migraciones = pd.read_csv(ruta + archivo_migraciones)
datos_completos = pd.read_csv(ruta+archivo_completo, on_bad_lines = 'skip')
datos_basicos = pd.read_csv(ruta+archivo_basico)

#%%
consulta_sql20 = """
                  SELECT "Country Origin Name", "Country Origin Code",
                         "Migration by Gender Name", "Migration by Gender Code",
                         "Country Dest Name", "Country Dest Code", "1960 [1960]", "1970 [1970]",
                         "1980 [1980]", "1990 [1990]", REPLACE ("2000 [2000]", '..', '0') AS "2000 [2000]"
                  FROM datos_migraciones;
                 """

datos_migraciones20 = sql^consulta_sql20

#%%

#Armado de las tablas del Modelo Relacional:

#PAIS:

#Primero saco todos los valores que no se pueden convertir a decimal de la columna 2000
consulta_sql2 = """
                 SELECT * 
                 FROM datos_migraciones
                 WHERE TRY_CAST("2000 [2000]" AS DECIMAL) IS NOT NULL;
                """
                
consulta_sql20 = """
                  SELECT "Country Origin Name", "Country Origin Code",
                         "Migration by Gender Name", "Migration by Gender Code",
                         "Country Dest Name", "Country Dest Code", "1960 [1960]", "1970 [1970]",
                         "1980 [1980]", "1990 [1990]", REPLACE ("2000 [2000]", '..', '0') AS "2000 [2000]"
                  FROM datos_migraciones;
                 """


datos_migraciones2 = sql^consulta_sql20

#Tomo las inmigraciones y las emigraciones y sumo.
    
consulta_sql = """
                SELECT DISTINCT "Country Origin Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS emigraciones00
                FROM datos_migraciones2
                GROUP BY "Country Origin Code";
               """
               
emigraciones00 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT "Country Dest Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS inmigraciones00
                FROM datos_migraciones2
                GROUP BY "Country Dest Code";
               """
               
inmigraciones00 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT i.codigo, (i.inmigraciones00 - e.emigraciones00) AS flujo_mundo
                FROM inmigraciones00 AS i
                INNER JOIN emigraciones00 AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

migraciones00 = sql^consulta_sql

#Ahora hay que poner el flujo migratorio con ARG.

consulta_sql = """
                SELECT DISTINCT "Country Origin Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS emigraciones00ARG
                FROM datos_migraciones2
                WHERE "Country Dest Code" = 'ARG'
                GROUP BY "Country Origin Code";
               """
               
emigraciones00ARG = sql^consulta_sql  

consulta_sql = """
                SELECT DISTINCT "Country Dest Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS inmigraciones00ARG
                FROM datos_migraciones2
                WHERE "Country Origin Code" = 'ARG'
                GROUP BY "Country Dest Code";
               """
               
inmigraciones00ARG = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT i.codigo, (i.inmigraciones00ARG - e.emigraciones00ARG) AS flujo_ARG
                FROM inmigraciones00ARG AS i
                INNER JOIN emigraciones00ARG AS e
                ON i.codigo = e.codigo;
               """

migraciones00ARG = sql^consulta_sql

#Ahora voy a armar una tabla que tenga Codigo, Pais y region geografica



consulta_sql = """
                SELECT DISTINCT pais_iso_3, pais_castellano AS nombre_pais, region_geografica
                FROM datos_completos;
               """

info_pais = sql^consulta_sql

#Finalmente armo la relacion PAIS.

consulta_sql = """
                SELECT DISTINCT i.nombre_pais, i.region_geografica, m1.flujo_mundo, m2.flujo_ARG
                FROM info_pais as i
                INNER JOIN migraciones00 AS m1
                ON i.pais_iso_3 = m1.codigo
                INNER JOIN migraciones00ARG AS m2
                ON i.pais_iso_3 = m2.codigo
                ORDER BY i.nombre_pais;
               """

Pais = sql^consulta_sql

# %%

# ######################SEDES##################:

#Los atributos son sede_id y region geografica. 

consulta_sql = """
                SELECT DISTINCT sede_id, pais_castellano AS nombre_pais
                FROM datos_completos
               """

sedes = sql^consulta_sql

#%%
#Probando split en dataframe

consulta_sql = """
                SELECT DISTINCT redes_sociales, sede_id
                FROM datos_completos
               """

redes_sociales0 = sql^consulta_sql

redes_sociales0['redes_sociales'] = redes_sociales0['redes_sociales'].str.split(' // ')

redes_sociales01 = redes_sociales0.explode('redes_sociales').reset_index(drop=True)

consulta_sql = """
                SELECT DISTINCT sede_id, redes_sociales
                FROM redes_sociales01
                WHERE redes_sociales IS NOT NULL 
                    AND TRIM(redes_sociales) != '';
               """

redes_sociales = sql^consulta_sql

 
# %%
# ############SECCIONES ##################:

#Los atributos descripcion de la sede en castellano. 

consulta_sql = """
                SELECT DISTINCT sede_id, sede_desc_castellano
                FROM datos_secciones;
               """

secciones = sql^consulta_sql


#%%

##########EJERCICIO H#########

#%%

#i)

#Primero hago una tabla de paises con la cantidad de sedes
consulta_sql = """
                SELECT DISTINCT nombre_pais, COUNT(nombre_pais) AS cant_sedes
                FROM sedes
                GROUP BY nombre_pais
                ORDER BY nombre_pais;
               """

cantidad_sedes = sql^consulta_sql



#Ahora una tabla de sedes con la cantidad de secciones (ademas guardo el pais de la sede)
consulta_sql = """
                SELECT DISTINCT s1.nombre_pais, s1.sede_id, s2.cant_secciones
                FROM sedes AS s1
                LEFT JOIN (SELECT DISTINCT sede_id, COUNT(sede_id) AS cant_secciones
                      FROM secciones
                      GROUP BY sede_id) AS s2
                ON s1.sede_id = s2.sede_id
                ORDER BY s1.nombre_pais;
               """
               
cant_seccionesXsede = sql^consulta_sql

#hay sedes que no tienen secciones, eso me esta cagando todo

consulta_sql = """
                SELECT DISTINCT nombre_pais, sede_id, COALESCE(cant_secciones, 0) AS cant_secciones
                FROM cant_seccionesXsede
                ORDER BY nombre_pais;
               """

cant_seccionesXsede2 = sql^consulta_sql

#use ese comando para reemplazar los nulls por 0, nose porq no funciona replace.

#Ahora saco el promedio de secciones por sede.
consulta_sql = """
                SELECT DISTINCT nombre_pais, AVG(cant_secciones) AS secciones_promedio
                FROM cant_seccionesXsede2
                GROUP BY nombre_pais
                ORDER BY nombre_pais;
               """

avg_secciones = sql^consulta_sql


#Finalmente los joins de las tablas que hice para obtener el resultado.

consulta_sql = """
                SELECT DISTINCT cs.nombre_pais, cs.cant_sedes, a.secciones_promedio, p.flujo_mundo
                FROM cantidad_sedes AS cs
                INNER JOIN avg_secciones AS a
                ON cs.nombre_pais = a.nombre_pais
                LEFT JOIN Pais AS p
                ON cs.nombre_pais = p.nombre_pais;
               """

resultado = sql^consulta_sql

#hay algo raro que es que cuando hago el inner join con pais pierdo 3 paises, osea
#hay 3 paises que no tienen datos en la tabla de migraciones que nos dieron, un ejemplo es
#serbia. 
#cambios = cambie el .. por 0 cuando hice datos migratorios

#%%
#ii)

consultaSQL = """
                Select distinct region_geografica, AVG(flujo_ARG) as flujo_promedio 
                From Pais
                Group by region_geografica
                """
regionYflujo = sql^consultaSQL

paisesConSedes = sql^"""
                Select distinct region_geografica, COUNT(nombre_pais) AS paises_con_sedes
                From Pais
                Group by region_geografica;
                """
                
consulta_sql = """
                SELECT r.region_geografica, p.paises_con_sedes, r.flujo_promedio
                FROM regionYflujo AS r
                INNER JOIN paisesConSedes AS p
                ON r.region_geografica = p.region_geografica
                ORDER BY r.flujo_promedio DESC;
               """

flujoPorRegionYSedes = sql^consulta_sql

#%%
#iii)

consulta_sql = """
                SELECT DISTINCT  s.nombre_pais, s.sede_id, r.redes_sociales
                FROM sedes AS s
                INNER JOIN  redes_sociales AS r
                ON s.sede_id = r.sede_id
                ORDER BY s.nombre_pais ASC;
               """

paisSedesRedes = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT  nombre_pais, 
                                CASE 
                                    WHEN redes_sociales LIKE '%facebook%' THEN 'facebook'
                                    WHEN redes_sociales LIKE '%instagram%' THEN 'instagram'
                                    WHEN redes_sociales LIKE '%twitter%' THEN 'twitter'
                                    WHEN redes_sociales LIKE '%linkedin%' THEN 'linkedin'
                                    WHEN redes_sociales LIKE '%flickr%' THEN 'flickr'
                                    WHEN redes_sociales LIKE '%youtube%' THEN 'youtube'
                                    WHEN redes_sociales LIKE '%gmail%' THEN 'gmail'
                                    ELSE 'desconocida'
                                END AS red_social
                FROM paisSedesRedes
                ORDER BY nombre_pais ASC;
               """

paisesConRedes = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT nombre_pais, count(nombre_pais) AS cant_redes
                FROM paisesConRedes
                WHERE red_social != 'desconocida'
                GROUP BY nombre_pais
                ORDER BY nombre_pais ASC;
               """
               
cantRedesPais = sql^consulta_sql
#%%
#iv)









