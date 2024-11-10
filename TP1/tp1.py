# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:39:08 2024

@author: Sebastián
"""

import numpy as np
import pandas as pd
from inline_sql import sql, sql_val
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns  

ruta = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\TP1\\TablasOriginales\\"

archivo_secciones = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\TP1\\TablasOriginales\\lista-secciones.csv"
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
                         "Country Dest Name", "Migration by Gender Code", "1960 [1960]", "1970 [1970]",
                         "1980 [1980]", "1990 [1990]", REPLACE ("2000 [2000]", '..', '0') AS "2000 [2000]"
                  FROM datos_migraciones
                  WHERE "Migration by Gender Name" == 'Total';
                 """

datos_migraciones20 = sql^consulta_sql20

#%%

consulta_sql = """
                SELECT * 
                FROM datos_migraciones
                WHERE "2000 [2000]" == '..'
               """

probando = sql^consulta_sql


#%%

#Armado de las tablas del Modelo Relacional:

############PAIS#############:

#Primero cambio los valores de flujo donde hay '..' por '0'.

                
consulta_sql20 = """
                  SELECT *
                  FROM datos_migraciones
                  WHERE "Migration by Gender Name" == 'Total' AND "2000 [2000]" != '..' ;
                 """

datos_migraciones2 = sql^consulta_sql20


#Tomo las inmigraciones y las emigraciones y sumo.
    
consulta_sql = """
                SELECT DISTINCT "Country Origin Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS emigraciones00
                FROM datos_migraciones2
                GROUP BY "Country Origin Code"
                ORDER BY codigo;
               """
               
emigraciones00 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT "Country Dest Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS inmigraciones00
                FROM datos_migraciones2
                GROUP BY "Country Dest Code"
                ORDER BY codigo;
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
                GROUP BY "Country Origin Code"
                ORDER BY codigo;
               """
               
emigraciones00ARG = sql^consulta_sql  

consulta_sql = """
                SELECT DISTINCT "Country Dest Code" AS codigo, SUM(CAST("2000 [2000]" AS DECIMAL)) AS inmigraciones00ARG
                FROM datos_migraciones2
                WHERE "Country Origin Code" = 'ARG'
                GROUP BY "Country Dest Code"
                ORDER BY codigo;
               """
               
inmigraciones00ARG = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT i.codigo, (i.inmigraciones00ARG - e.emigraciones00ARG) AS flujo_ARG
                FROM inmigraciones00ARG AS i
                INNER JOIN emigraciones00ARG AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

migraciones00ARG = sql^consulta_sql

#ahora hago una tabla que tenga flujo migratorio de 1960 hasta 2000 (para el punto I ii)

#calculo las emigraciones
consulta_sql = """
                SELECT DISTINCT "Country Origin Code" AS codigo, SUM(CAST("1960 [1960]" AS DECIMAL)) AS emigraciones60,
                                SUM(CAST("1970 [1970]" AS DECIMAL)) AS emigraciones70,
                                SUM(CAST("1980 [1980]" AS DECIMAL)) AS emigraciones80,
                                SUM(CAST("1990 [1990]" AS DECIMAL)) AS emigraciones90,
                                SUM(CAST("2000 [2000]" AS DECIMAL)) AS emigraciones00
                FROM datos_migraciones2
                GROUP BY "Country Origin Code";
               """
               
emigraciones = sql^consulta_sql

#calculo la inmigraciones
consulta_sql = """
                SELECT DISTINCT "Country Dest Code" AS codigo, SUM(CAST("1960 [1960]" AS DECIMAL)) AS inmigraciones60,
                                SUM(CAST("1970 [1970]" AS DECIMAL)) AS inmigraciones70,
                                SUM(CAST("1980 [1980]" AS DECIMAL)) AS inmigraciones80,
                                SUM(CAST("1990 [1990]" AS DECIMAL)) AS inmigraciones90,
                                SUM(CAST("2000 [2000]" AS DECIMAL)) AS inmigraciones00
                FROM datos_migraciones2
                GROUP BY "Country Dest Code";
               """
               
inmigraciones = sql^consulta_sql


#calculo el flujo migratorio
consulta_sql = """
                SELECT DISTINCT i.codigo, 
                                (i.inmigraciones60 - e.emigraciones60) AS flujo_mundo60,
                                (i.inmigraciones70 - e.emigraciones70) AS flujo_mundo70,
                                (i.inmigraciones80 - e.emigraciones80) AS flujo_mundo80,
                                (i.inmigraciones90 - e.emigraciones90) AS flujo_mundo90,
                                (i.inmigraciones00 - e.emigraciones00) AS flujo_mundo00
                                
                FROM inmigraciones AS i
                INNER JOIN emigraciones AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

migraciones = sql^consulta_sql

#hago la suma de los flujos migratorios por cada decada
consulta_sql = """
                SELECT DISTINCT codigo, (flujo_mundo60 + flujo_mundo70 + flujo_mundo80 + flujo_mundo90 +flujo_mundo00) flujo60_00
                FROM migraciones
                ORDER BY codigo ASC;
               """
               
flujo_total = sql^consulta_sql 
#Ahora voy a armar una tabla que tenga Codigo, Pais y region geografica



consulta_sql = """
                SELECT DISTINCT pais_iso_3, pais_castellano AS nombre_pais, region_geografica
                FROM datos_completos;
               """

info_pais = sql^consulta_sql

#Finalmente armo la relacion PAIS.

consulta_sql = """
                SELECT DISTINCT i.nombre_pais, i.region_geografica, m1.flujo_mundo, m2.flujo_ARG, f.flujo60_00
                FROM info_pais as i
                INNER JOIN migraciones00 AS m1
                ON i.pais_iso_3 = m1.codigo
                INNER JOIN migraciones00ARG AS m2
                ON i.pais_iso_3 = m2.codigo
                INNER JOIN flujo_total AS f
                ON i.pais_iso_3 = f.codigo
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
###########REDES SOCIALES#################
#Para armar la tabla de Redes Sociales hay que dividir los valores originales que hay 
#en datos completos, para cumplir con las formas normales.


consulta_sql = """
                SELECT DISTINCT redes_sociales, sede_id
                FROM datos_completos
               """

redes_sociales0 = sql^consulta_sql


#Aca separamos el texto de las celdad de redes sociales con "//", ya que ese es el formato en
#el csv para dividir cada red social de cada sede.
redes_sociales0['redes_sociales'] = redes_sociales0['redes_sociales'].str.split(' // ')

redes_sociales01 = redes_sociales0.explode('redes_sociales').reset_index(drop=True)

consulta_sql = """
                SELECT DISTINCT sede_id, redes_sociales AS URL
                FROM redes_sociales01
                WHERE redes_sociales IS NOT NULL 
                    AND TRIM(redes_sociales) != '';
               """

redes_sociales = sql^consulta_sql


#%% 
#quiero agregar a red social un atributo que sea tipo de red.

consulta_sql = """
                SELECT DISTINCT  sede_id, URL, 
                                CASE 
                                    WHEN URL LIKE '%facebook%' THEN 'facebook'
                                    WHEN URL LIKE '%instagram%' THEN 'instagram'
                                    WHEN URL LIKE '%twitter%' THEN 'twitter'
                                    WHEN URL LIKE '%linkedin%' THEN 'linkedin'
                                    WHEN URL LIKE '%flickr%' THEN 'flickr'
                                    WHEN URL LIKE '%youtube%' THEN 'youtube'
                                    WHEN URL LIKE '%gmail%' THEN 'gmail'
                                    ELSE 'desconocida'
                                END AS tipo_red
                FROM redes_sociales;
               """
 
redes_sociales = sql^consulta_sql
# %%
# ############SECCIONES ##################:

#hay que hacer la tabal de secciones y también la tabla de dividida_en

consulta_sql = """
                SELECT DISTINCT sede_desc_castellano
                
                FROM datos_secciones;
               """
secciones = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT sede_id, sede_desc_castellano
                FROM datos_secciones;
               """

dividida_en = sql^consulta_sql

#cambiar secciones
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
                      FROM dividida_en
                      GROUP BY sede_id) AS s2
                ON s1.sede_id = s2.sede_id
                ORDER BY s1.nombre_pais;
               """
               
cant_seccionesXsede = sql^consulta_sql

#hay sedes que no tienen secciones, para resolver esto hacemos la siguiente consulta.

consulta_sql = """
                SELECT DISTINCT nombre_pais, sede_id, COALESCE(cant_secciones, 0) AS cant_secciones
                FROM cant_seccionesXsede
                ORDER BY nombre_pais;
               """

cant_seccionesXsede2 = sql^consulta_sql

#use ese comando (COALESCE) para reemplazar los nulls por 0.

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
                ON cs.nombre_pais = p.nombre_pais
                ORDER BY cs.cant_sedes DESC , cs.nombre_pais; 
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
                SELECT DISTINCT  s.nombre_pais, r.tipo_red
                FROM sedes AS s
                INNER JOIN  redes_sociales AS r
                ON s.sede_id = r.sede_id
                ORDER BY s.nombre_pais ASC;
               """

paisSedesRedes = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT nombre_pais, count(nombre_pais) AS cant_redes
                FROM paisSedesRedes
                WHERE tipo_red != 'desconocida'
                GROUP BY nombre_pais
                ORDER BY nombre_pais ASC;
               """
               
cantRedesPais = sql^consulta_sql
#%%
#iv)
consulta_sql="""
SELECT s.nombre_pais, s.sede_id, r.tipo_red, r.URL
FROM redes_sociales as r 
INNER JOIN sedes as s
ON s.sede_id = r.sede_id
"""

redes_paises = sql^consulta_sql

#%%


#!!!!!!!!!!!!!!!!!!!VISUALIZACION!!!!!!!!!!!!!!!!!!!!!!!!

#i)


#i)
#cntd sdes por region geografica:
    
sedesxregion=sql^"""
SELECT SUM(cs.cant_sedes) as cant_sedes, region_geografica
FROM cantidad_sedes as cs
INNER JOIN info_pais as ip
ON cs.nombre_pais = ip.nombre_pais
GROUP BY region_geografica
ORDER BY cant_sedes
"""


#%%
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           


sns.barplot(data=sedesxregion, x='region_geografica', y='cant_sedes',palette="colorblind",
            legend='full',errorbar=None,edgecolor="black",linewidth=2.5)



ax.set_title('Sedes x Region Geografica')
ax.set_xlabel('Región', fontsize='medium')                       
ax.set_ylabel('Cantidad', fontsize='medium')    
#ax.set_xlim(0, 11)
#ax.set_ylim(0, 250)
plt.xticks(rotation=90)
plt.grid(True,linestyle="--",linewidth=0.5)
##ax.set_xticks(range(1,11,1))               # Muestra todos los ticks del eje x
#ax.set_yticks([])                          # Remueve los ticks del eje y
#ax.bar_label(ax.containers[0], fontsize=8)   # Agrega la etiqueta a cada barra




#%%
#ii)

#boxplot

medianas = Pais.groupby('region_geografica')['flujo_mundo'].median().sort_values(ascending=False)

ax = sns.boxplot(x="region_geografica", 
                 y="flujo60_00",  
                 data=Pais,
                 order = medianas.index,
                 palette = "colorblind")

ax.set_title('Flujo Migratorio Por Región')
ax.set_xlabel('Región Geográfica')
ax.set_ylabel('Flujo Migratorio')
 
plt.xticks(rotation=90)
plt.grid(True,linestyle="--",linewidth=0.5)

#%%

consultaSQL = """
                Select distinct d.pais_iso_3 AS codigo , d.pais_castellano AS País, c.cant_sedes
                From datos_basicos AS d
                INNER JOIN cantidad_sedes AS c
                ON d.pais_castellano = c.nombre_pais
                """
codigo_pais_sede = sql^consultaSQL

consultaSQL = """
                Select c.cant_sedes, m.flujo_ARG
                From codigo_pais_sede AS c
                INNER JOIN migraciones00ARG AS m
                ON c.codigo = m.codigo
                """

sedes_flujo = sql^consultaSQL


plt.scatter(data = sedes_flujo, x='cant_sedes', y='flujo_ARG')
fig, ax = plt.subplots() 
plt.rcParams['font.family'] = 'sans-serif'           
ax.scatter(data = sedes_flujo,  
            x='cant_sedes', 
            y='flujo_ARG',
            s=30,      
            color='red')

ax.set_title('Flujo migratorio en relación a la cantidad de sedes')
ax.set_xlabel('Cantidad de sedes', fontsize='medium')          
ax.set_ylabel('Flujo migratorio ', 
              fontsize='medium')
#%%

#GQM PARA MIGRACIONES 


consulta_sql = """
                SELECT DISTINCT COUNT("2000 [2000]") AS cant_de_puntos
                FROM datos_migraciones 
                WHERE "2000 [2000]" = '..'
               """

gqm_migraciones = sql^consulta_sql



#%%

# %%
# ############REDES SOCIALES ##################:

#Los atributos son url. 

consulta_sql = """
                SELECT DISTINCT redes_sociales, sede_id
                FROM datos_completos
               """

redes_sociales = sql^consulta_sql


#vamos a splittear las redes sociales por url
a=redes_sociales["redes_sociales"]
b=a[2]

def splitRedes(df):
    listadelistaurls:list=[] #contiene listas de listas, algunas listas de un solo elemento y otras vacias (supongo the later)
    redes = df["redes_sociales"]
    for i in range(len(redes)):
        urls = redes[i]
        listaurl=[]
        if urls != None:
            listaurl=urls.split(' //')
            listaurl.pop()  ##TODAS LAS LISTAS terminan con //, asi que saco el ultimo elemento a todas dif de null (si no, siempre qeudaba un ultimo vacio).
        listadelistaurls.append(listaurl)
    return listadelistaurls
 

redes_urls_separados=splitRedes(redes_sociales)

def matcheoListaSede(df,listadelistas):
    #matchea cada lista con una sede, y las hace dfs
    
    u1=[]
    s1=[]
    
    d={"sede_id":s1,"url":u1}
    
    res = pd.DataFrame(data=d)
    
    sedes_id=df["sede_id"]
    
    for i in range(len(listadelistas)):
        
        urls = listadelistas[i]
        id= sedes_id[i]
        
        repeticionId=[]
        for j in range(len(urls)):
            repeticionId.append(id)
        
        #tal vez no necesito este for!! me tengo q ir al cumple!
            
        datosede = {"sede_id":repeticionId,"url":urls}
        dfsede=pd.DataFrame(data=datosede)
        
        res.concat(dfsede)
    return res
        
        
        
matcheoListaSede(redes_sociales, redes_urls_separados)

#%%
##########NUEVO DER#####################

#Armado de las tablas del Modelo Relacional:

#%%
############PAIS#############:

consulta_sql = """
                SELECT DISTINCT pais_iso_3, pais_castellano AS nombre_pais, region_geografica
                FROM datos_completos;
               """

Pais = sql^consulta_sql

#%%

##########Registra_movimiento############

#Primero nos quedamos con las filas donde tendría que ir genero dice 'total' y eliminamos
#las filas que tienen '..' como valores.

                
consulta_sql = """
                  SELECT *
                  FROM datos_migraciones
                  WHERE "Migration by Gender Name" == 'Total' AND "2000 [2000]" != '..' 
                  ORDER BY "Country Origin Code", "Country Dest Code";
                 """

datos_migraciones2 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT "Country Origin Code", "Country Dest Code", CASE 
                                                                                    WHEN True THEN '2000'
                                                                                END AS Decada, "2000 [2000]" AS cantidad
                FROM datos_migraciones2 
                ORDER BY "Country Origin Code", "Country Dest Code";
               """
               
reg_mov00 = sql^consulta_sql               
             
               
consulta_sql = """
                SELECT DISTINCT "Country Origin Code", "Country Dest Code", CASE 
                                                                                    WHEN True THEN '1960'
                                                                                END AS Decada, "1960 [1960]" AS cantidad
                FROM datos_migraciones2 
                ORDER BY "Country Origin Code", "Country Dest Code";
               """
               
reg_mov60 = sql^consulta_sql                    
               

consulta_sql = """
                SELECT DISTINCT "Country Origin Code", "Country Dest Code", CASE 
                                                                                    WHEN True THEN '1970'
                                                                                END AS Decada, "1970 [1970]" AS cantidad
                FROM datos_migraciones2 
                ORDER BY "Country Origin Code", "Country Dest Code";
               """
               
reg_mov70 = sql^consulta_sql                    
               

consulta_sql = """
                SELECT DISTINCT "Country Origin Code", "Country Dest Code", CASE 
                                                                                    WHEN True THEN '1980'
                                                                                END AS Decada, "1980 [1980]" AS cantidad
                FROM datos_migraciones2 
                ORDER BY "Country Origin Code", "Country Dest Code";
               """
               
reg_mov80 = sql^consulta_sql                       
               

consulta_sql = """
                SELECT DISTINCT "Country Origin Code", "Country Dest Code", CASE 
                                                                                    WHEN True THEN '1990'
                                                                                END AS Decada, "1990 [1990]" AS cantidad
                FROM datos_migraciones2 
                ORDER BY "Country Origin Code", "Country Dest Code";
               """
               
reg_mov90 = sql^consulta_sql        
               
               
consulta_sql = """
                SELECT DISTINCT *
                FROM reg_mov00
                UNION
                SELECT DISTINCT *
                FROM reg_mov60
                UNION
                SELECT DISTINCT *
                FROM reg_mov70
                UNION
                SELECT DISTINCT *
                FROM reg_mov80
                UNION
                SELECT DISTINCT *
                FROM reg_mov90;
               """               

registra_movimiento = sql^consulta_sql
               
#%%

#ARMAMOS TABLA PARA TRABAJAR CON VALORES DE FLUJO:
    

#Tomo las inmigraciones y las emigraciones y sumo.
    
consulta_sql = """
                SELECT DISTINCT "Country Origin Code" AS codigo, SUM(CAST(cantidad AS DECIMAL)) AS emigraciones00
                FROM registra_movimiento
                WHERE decada = '2000'
                GROUP BY "Country Origin Code"
                ORDER BY codigo;
               """
               
emigraciones00 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT "Country Dest Code" AS codigo, SUM(CAST("cantidad" AS DECIMAL)) AS inmigraciones00
                FROM registra_movimiento
                WHERE decada = '2000'
                GROUP BY "Country Dest Code"
                ORDER BY codigo;
               """
               
inmigraciones00 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT i.codigo, (i.inmigraciones00 - e.emigraciones00) AS flujo_mundo
                FROM inmigraciones00 AS i
                INNER JOIN emigraciones00 AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

migraciones002 = sql^consulta_sql


#Ahora hay que poner el flujo migratorio con ARG.

consulta_sql = """
                SELECT DISTINCT "Country Origin Code" AS codigo, SUM(CAST("cantidad" AS DECIMAL)) AS emigraciones00ARG
                FROM registra_movimiento
                WHERE "Country Dest Code" = 'ARG' AND "decada" = '2000'
                GROUP BY "Country Origin Code"
                ORDER BY codigo;
               """
               
emigraciones00ARG = sql^consulta_sql  

consulta_sql = """
                SELECT  "Country Dest Code" AS codigo, SUM(CAST("cantidad" AS DECIMAL)) AS inmigraciones00ARG
                FROM registra_movimiento
                WHERE "Country Origin Code" = 'ARG' AND "decada" = '2000'
                GROUP BY "Country Dest Code"
                ORDER BY codigo;
               """
               
inmigraciones00ARG = sql^consulta_sql

consulta_sql = """
                SELECT DISTINCT i.codigo, (i.inmigraciones00ARG - e.emigraciones00ARG) AS flujo_ARG
                FROM inmigraciones00ARG AS i
                INNER JOIN emigraciones00ARG AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

migraciones00ARG2 = sql^consulta_sql


#ahora hago una tabla que tenga flujo migratorio de 1960 hasta 2000 (para el punto I ii)


#con lo que tengo ahora

consulta_sql = """
                SELECT  "Country Origin Code" AS codigo, SUM(CAST(cantidad AS DECIMAL)) AS emigraciones60_00
                FROM registra_movimiento
                GROUP BY "Country Origin Code";
               """

emigraciones = sql^consulta_sql


consulta_sql = """
                SELECT "Country Dest Code" AS codigo , SUM(CAST(cantidad AS DECIMAL)) AS inmigraciones60_00
                FROM registra_movimiento
                GROUP BY "Country Dest Code";
               """

inmigraciones = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT i.codigo, (i.inmigraciones60_00 - e.emigraciones60_00) AS flujo00_60
                FROM inmigraciones AS i
                INNER JOIN emigraciones AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

flujo_total2 = sql^consulta_sql


consulta_sql = """
                SELECT DISTINCT p.nombre_pais, p.region_geografica, m1.flujo_mundo, m2.flujo_ARG, f.flujo60_00
                FROM Pais as p
                INNER JOIN migraciones00 AS m1
                ON p.pais_iso_3 = m1.codigo
                INNER JOIN migraciones00ARG AS m2
                ON p.pais_iso_3 = m2.codigo
                INNER JOIN flujo_total AS f
                ON p.pais_iso_3 = f.codigo
                ORDER BY p.nombre_pais;
               """

flujos_pais = sql^consulta_sql

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
                      FROM dividida_en
                      GROUP BY sede_id) AS s2
                ON s1.sede_id = s2.sede_id
                ORDER BY s1.nombre_pais;
               """
               
cant_seccionesXsede = sql^consulta_sql

#hay sedes que no tienen secciones, debo reemplazar los nulls por 0s.

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
                LEFT JOIN flujos_pais AS p
                ON cs.nombre_pais = p.nombre_pais
                ORDER BY cant_sedes DESC, cs.nombre_pais;
               """

resultado = sql^consulta_sql
