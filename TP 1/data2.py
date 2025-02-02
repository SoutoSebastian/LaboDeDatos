#%%
# Importamos bibliotecas
import os
from pathlib import Path
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns           # Para graficar histograma


# Cambiar el directorio de trabajo al del archivo actual
ruta_base = Path(__file__).parent

os.chdir(ruta_base)

miprefijo="TablasLimpias/"


archivo_completo=  "lista-sedes-completos.csv"

#Este archivo es archivo_completo pero solucionando el error que tenia una fila que no nos permitia
#visualizarla (Republica de Chile).

archivo_completo_copia=  "lista-sedes-completos - copia.csv"

archivo_basico = "lista-sedes-basicos.csv"

archivo_secciones= "lista-secciones.csv"

archivo_migraciones = "datos_migraciones.csv"

datos_basicos= pd.read_csv(archivo_basico)

datos_secciones = pd.read_csv(archivo_secciones)

datos_completos= pd.read_csv(archivo_completo_copia)

datos_migraciones = pd.read_csv(archivo_migraciones)


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

# %%

# ######################SEDES##################:

#Los atributos son sede_id y nombre_pais. 

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

#hay que hacer la tabla de secciones y también la tabla de dividida_en

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

migraciones00 = sql^consulta_sql


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

migraciones00ARG = sql^consulta_sql


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
                SELECT DISTINCT i.codigo, (i.inmigraciones60_00 - e.emigraciones60_00) AS flujo60_00
                FROM inmigraciones AS i
                INNER JOIN emigraciones AS e
                ON i.codigo = e.codigo
                ORDER BY i.codigo;
               """

flujo_total = sql^consulta_sql


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
                SELECT DISTINCT cs.nombre_pais, cs.cant_sedes, a.secciones_promedio, p.flujo_mundo as flujo_mundo_2000
                FROM cantidad_sedes AS cs
                INNER JOIN avg_secciones AS a
                ON cs.nombre_pais = a.nombre_pais
                LEFT JOIN flujos_pais AS p
                ON cs.nombre_pais = p.nombre_pais
                ORDER BY cant_sedes DESC, cs.nombre_pais;
               """

resultado = sql^consulta_sql

#%%

#ii)
#Selecciono region geografica y calculo el promedio del flujo con argentina.
consultaSQL = """
                Select distinct region_geografica, AVG(flujo_ARG) as flujo_promedio_arg 
                From flujos_pais
                Group by region_geografica
                """
regionYflujo = sql^consultaSQL

#Selecciono region geografica y cuento cuantos países tienen sedes argentinas
paisesConSedes = sql^"""
                Select distinct region_geografica, COUNT(nombre_pais) AS paises_con_sedes
                From flujos_pais
                Group by region_geografica;
                """

#Con los datos conseguidos anteriormente hago los joins para obtener la tabla pedida.
consulta_sql = """
                SELECT r.region_geografica, p.paises_con_sedes, r.flujo_promedio_arg as flujo_promedio_arg_2000
                FROM regionYflujo AS r
                INNER JOIN paisesConSedes AS p
                ON r.region_geografica = p.region_geografica
                ORDER BY r.flujo_promedio_arg DESC;
               """

flujoPorRegionYSedes = sql^consulta_sql

#%%

#Selecciono nombre del pais, sede id y red social.
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
#cantidad de sedes por region geografica:
sedesxregionbien=sql^"""
SELECT COUNT(s.nombre_pais) as cant_sedes, region_geografica
FROM sedes as s
INNER JOIN flujos_pais as ip
ON s.nombre_pais = ip.nombre_pais
GROUP BY region_geografica
ORDER BY cant_sedes
"""



#%%
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           

#Usamos unos colores seleccionados manualmente para ser constante con cada región.
colores = ['blue', "#A0C4FF", '#00FF00', '#8B4513', '#FFB3BA', '#40E0D0', '#800080', '#FF0000', '#FFF700']

sns.barplot(data=sedesxregionbien, x='region_geografica', y='cant_sedes',palette=colores,
            legend='full',errorbar=None,edgecolor="black",linewidth=2.5)



ax.set_title('Sedes x Region Geografica')
ax.set_xlabel('Región', fontsize='medium')                       
ax.set_ylabel('Cantidad', fontsize='medium')    
#ax.set_xlim(0, 11)
#ax.set_ylim(0, 250)
plt.xticks(rotation=90)
plt.grid(True,linestyle="--",linewidth=0.5)

#%%
#Hago un flujo_ARG_promedio de todos los tiempos (no solo )
consulta_sql = """
                SELECT "Country Dest Code" AS destino, 
                       SUM(CAST("1960 [1960]" AS DECIMAL)) AS emigraciones60,
                       SUM(CAST("1970 [1970]" AS DECIMAL)) AS emigraciones70,
                       SUM(CAST("1980 [1980]" AS DECIMAL)) AS emigraciones80,
                       SUM(CAST("1990 [1990]" AS DECIMAL)) AS emigraciones90,
                       SUM(CAST("2000 [2000]" AS DECIMAL)) AS emigraciones00
                FROM datos_migraciones2
                WHERE "Country Origin Code" = 'ARG'
                GROUP BY "Country Dest Code";
               """
emigraciones_ARG = sql^consulta_sql

#Inmigraciones a Argentina por década
consulta_sql = """
                SELECT "Country Origin Code" AS origen, 
                       SUM(CAST("1960 [1960]" AS DECIMAL)) AS inmigraciones60,
                       SUM(CAST("1970 [1970]" AS DECIMAL)) AS inmigraciones70,
                       SUM(CAST("1980 [1980]" AS DECIMAL)) AS inmigraciones80,
                       SUM(CAST("1990 [1990]" AS DECIMAL)) AS inmigraciones90,
                       SUM(CAST("2000 [2000]" AS DECIMAL)) AS inmigraciones00
                FROM datos_migraciones2
                WHERE "Country Dest Code" = 'ARG'
                GROUP BY "Country Origin Code";
               """
inmigraciones_ARG = sql^consulta_sql


#Calcular flujo de migración por década
consulta_sql = """
                SELECT i.origen AS codigo,
                       (AVG(i.inmigraciones60) - AVG(e.emigraciones60)) AS flujo60,
                       (AVG(i.inmigraciones70) - AVG(e.emigraciones70)) AS flujo70,
                       (AVG(i.inmigraciones80) - AVG(e.emigraciones80)) AS flujo80,
                       (AVG(i.inmigraciones90) - AVG(e.emigraciones90)) AS flujo90,
                       (AVG(i.inmigraciones00) - AVG(e.emigraciones00)) AS flujo00
                FROM inmigraciones_ARG AS i
                INNER JOIN emigraciones_ARG AS e
                ON i.origen = e.destino
                GROUP BY i.origen;
               """
flujo_ARG_por_decada = sql^consulta_sql

consulta_sql = """
                Select codigo, (flujo60 + flujo70 + flujo80 + flujo90 + flujo00) / 5 AS flujo_promedio
                From flujo_ARG_por_decada
                """
flujo_ARG_promedio = sql^consulta_sql

consulta_sql = """
                SELECT m.region_geografica, f.flujo_promedio AS flujo_ARG
                FROM flujo_ARG_promedio AS f
                INNER JOIN datos_completos AS m 
                ON f.codigo = m.pais_iso_3
                """
flujo_promedio_por_region = sql^consulta_sql
#%%
#colores = ['blue', "#A0C4FF", '#00FF00', '#8B4513', '#FFB3BA', '#40E0D0', '#800080', '#FF0000', '#FFF700']
#ii)
data = flujo_promedio_por_region
colores = ['#FFF700', '#FF0000', '#00FF00', '#800080', '#A0C4FF', '#8B4513','#FFB3BA','blue', "#40E0D0"]

# #esto es para poder ordenar el boxplot segun la mediana.
medianas = data.groupby('region_geografica')['flujo_ARG'].median().sort_values(ascending=False)

ax = sns.boxplot(x="region_geografica", 
                  y="flujo_ARG",  
                  data=data,
                  order = medianas.index,
                  palette = colores)

ax.set_title('Flujo Migratorio Por Región')
ax.set_xlabel('Región Geográfica')
ax.set_ylabel('Flujo Migratorio')

plt.xticks(rotation=90)
plt.grid(True,linestyle="--",linewidth=0.5)

#%%
#iii)
consultaSQL = """
                Select c.cant_sedes, m.flujo_ARG
                From cantidad_sedes AS c
                INNER JOIN flujos_pais AS m
                ON c.nombre_pais = m.nombre_pais
                """

sedes_flujo = sql^consultaSQL

#Aca remarcamos la sección de la izquieda donde se juntan los puntos:
sedes_flujo['color'] = ['red' if x == 1 else '#0d99ff' for x in sedes_flujo['cant_sedes']]

sns.scatterplot(data=sedes_flujo, x='cant_sedes', y='flujo_ARG', hue='color', palette=['#0d99ff', 'red'], s=50, legend=False)

plt.xlabel('Cantidad de sedes', fontsize='medium')
plt.ylabel('Flujo migratorio', fontsize='medium')
plt.title('Flujo migratorio en relación a la cantidad de sedes')
plt.show()

#%%
#mismo gráfico enfocado en los paises con 1 sede

jitter_strength = 0.3

sns.scatterplot(x=sedes_flujo['cant_sedes'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(sedes_flujo)), 
    y=sedes_flujo['flujo_ARG'],
    color='red', 
    s=50, 
    legend=False)

plt.xlabel('', fontsize='medium')
plt.ylabel('Flujo migratorio', fontsize='medium')
plt.title('Flujo migratorio en los países con 1 sede')
plt.xlim(0.5, 1.5)
plt.ylim(-6000, 5000)
plt.xticks([])
plt.show()
