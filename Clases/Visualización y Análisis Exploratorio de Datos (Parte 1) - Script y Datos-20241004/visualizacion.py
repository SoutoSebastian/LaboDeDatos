#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase Visualizacion. Script clase.
Autor  : Ailen Altamirano
Fecha  : 2024-01-04
"""
#%%
# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns           # Para graficar histograma

# Carpeta donde se encuentran los archivos a utilizar
#carpeta = "~/Downloads/clase-12/scriptClase/"
carpeta = "~/Escritorio/LaboDeDatos/Visualización y Análisis Exploratorio de Datos (Parte 1) - Script y Datos-20241004/"



#%%##########################################################################
#                                                                           #
#                                WINES                                      #
#                                                                           #
#############################################################################

##### 1. SCATTER PLOT
wine = pd.read_csv(carpeta+"wine.csv", sep = ";") # con sep indicamos que el 
                                                    # separador es ;

# Genera el grafico que relaciona la acidez (no volatil) y el contenido de 
# acido citrico de cada vino
plt.scatter(data = wine, x='fixed acidity', y='citric acid')

# Genera un nuevo grafico que relaciona  la acidez (no volatil) 
# y el contenido de  acido citrico (cambiamos algunos 
# parametros para mejorar la informacion mostrada)
fig, ax = plt.subplots() 

# plt.subplots() es una función que devuelve una tupla que contiene: 
# i)  el objeto correspondiente a una figura
# ii) el objeto correspondiente a sus ejes
# 
# Contar con fig es útil si quiere cambiar los atributos a nivel de figura o guardar 
# la figura como un archivo de imagen más adelante, por ejemplo con 
# fig.savefig('yourfilename.png')

plt.rcParams['font.family'] = 'sans-serif'           
ax.scatter(data = wine,  
           x='fixed acidity', 
           y='citric acid',
           s=8,                       # Tamano de los puntos
           color='magenta')           # Color de los puntos

ax.set_title('Acidez vs contenido de ácido cítrico') # Titulo del gráfico
ax.set_xlabel('Acidez (g/dm3)', fontsize='medium')   # Nombre eje X           
ax.set_ylabel('Contenido de ácido cítrico (g/dm3)', 
              fontsize='medium')                     # Nombre eje Y

#%%

##### 2. BUBBLE CHART
# Genera el grafico que relaciona tres variables en simultaneo 
# (grafico por defecto)
plt.scatter(data=wine, x='fixed acidity', y='citric acid', s='residual sugar')

# Genera el grafico que relaciona tres variables en simultaneo 
# (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           

tamanoBurbuja = 5  # Cuanto queremos modificar
                     # el tamaño de cada burbuja

ax.scatter(data=wine, x='fixed acidity', 
           y='citric acid', s=wine['residual sugar']*tamanoBurbuja)

ax.set_title('Relación entre tres variables')
ax.set_xlabel('Acidez (g/dm3)', fontsize='medium')                       
ax.set_ylabel('Contenido de ácido cítrico (g/dm3)', 
              fontsize='medium')    


# remueve la variable remporal tamanoBurbuja que ya no utilizaremos
del(tamanoBurbuja)

#%%

##### 3. PIE PLOT

# Contamos cuantos vinos de cada tipo hay en el dataset
wine['type'].value_counts()

# Genera el grafico de torta (grafico por defecto)

fig, ax = plt.subplots()
wine['type'].value_counts().plot(kind='pie')


# Genera el grafico de barras torta (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           
plt.rcParams['font.size'] = 9.0
wine['type'].value_counts().plot(kind='pie', 
             ax=ax, 
             autopct='%1.1f%%',           # Añadir porcentajes
             colors=['#66b3ff','#ff9999'], # Cambiar los colores
             startangle=90,               # Iniciar en ángulo 90
             shadow=True,                 # Añadir sombra
             explode=(0.1, 0),            # Separar la primera slice
             legend=False                 # Evitar leyenda
            )
ax.set_ylabel('')  # Remover el label del eje Y
ax.set_title('Distribución de Tipos de Vino')  # Añadir un título

# Mostrar el gráfico
plt.show()
#%%
########################### EJERCICIOS#######################################
# Sigamos trabajando con el dataset de vinos

# ¿Existe alguna relación entre el pH de los vinos (pH) y alguna de las otras variables? 
# Muestrelo gráficamente 
# Justifique la elección del tipo de gráfico.

fig, ax = plt.subplots() 

plt.rcParams['font.family'] = 'sans-serif'           
ax.scatter(data = wine,  
           x='pH', 
           y='sulphates',
           s=8,                       # Tamano de los puntos
           color='magenta')           # Color de los puntos

ax.set_title('pH vs sulfato') # Titulo del gráfico
ax.set_xlabel('pH', fontsize='medium')   # Nombre eje X           
ax.set_ylabel('Sulfato', 
              fontsize='medium')                     # Nombre eje Y



# Discutir con el resto de la clase:
# ¿Cuál fue su objetivo: Explorar, Explicar, Otro?
# ¿Qué tipos de variables estaban en juego?
# ¿Mejoró alguna característica del gráfico para cumplir con el objetivo?
#%%##########################################################################
#############################################################################
#                                                                           #
#                              CHEETAH REGIONS                              #
#                                                                           #
#############################################################################

# Cargamos el dataset
cheetahRegion= pd.read_csv(carpeta+"cheetahRegion.csv")


##### 4. GRAFICO DE BARRAS (BAR PLOT)

# Genera el grafico de barras de las ventas mensuales (grafico por defecto)
fig, ax = plt.subplots()

ax.bar(data=cheetahRegion, x='Anio', height='Ventas')

# Genera el grafico de barras de las ventas mensuales (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           


ax.bar(data=cheetahRegion, x='Anio', height='Ventas')
       
ax.set_title('Ventas de la compañía Cheetah Sports')
ax.set_xlabel('Año', fontsize='medium')                       
ax.set_ylabel('Ventas (millones de $)', fontsize='medium')    
ax.set_xlim(0, 11)
ax.set_ylim(0, 250)

ax.set_xticks(range(1,11,1))               # Muestra todos los ticks del eje x
ax.set_yticks([])                          # Remueve los ticks del eje y
ax.bar_label(ax.containers[0], fontsize=8)   # Agrega la etiqueta a cada barra
#%%
##### 5. GRAFICO DE BARRAS AGRUPADAS

# Genera el grafico de barras de ambas series temporales (grafico por defecto)
fig, ax = plt.subplots()

cheetahRegion.plot(x='Anio', y=['regionEste', 'regionOeste'], kind='bar', ax = ax)


# Genera el grafico de barras de ambas series temporales (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           

cheetahRegion.plot(x='Anio', 
                    y=['regionEste', 'regionOeste'], 
                    kind='bar',
                    label=['Region Este', 'Region Oeste'],   # Agrega etiquetas a la serie
                    ax = ax)
ax.set_title('Ventas de la compañía Cheetah Sports según región')
ax.set_xlabel('Año')
ax.set_ylabel('Ventas (millones de $)')
ax.set_xlim(-1,10)
ax.set_ylim(0,140)

#%%
##### 6. GRAFICO DE BARRAS APILADAS

# Genera el grafico de barras apiladas de ambas series temporales (mejorando la informacion mostrada)
fig, ax = plt.subplots()

# Grafica la serie regionEste 
ax.bar(cheetahRegion['Anio'], cheetahRegion['regionEste'] , 
       label='Region Este', color = "#4A4063")
# Grafica la serie regionOeste
ax.bar(cheetahRegion['Anio'], cheetahRegion['regionOeste'], 
       bottom=cheetahRegion['regionEste'], label='Region Oeste',
       color = 'skyblue')

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
ax.set_title('Ventas de la compañía Cheetah Sports según región')
ax.set_xlabel('Año')
ax.set_ylabel('Ventas (millones de $)')
ax.set_xlim(0,10.9)
ax.set_ylim(0,250)
ax.set_xticks(range(1,11,1))    # Muestra todos los ticks del eje x

plt.legend()                    # Muestra la leyenda


#%%
##### 7. GRAFICO DE LINEAS
# Genera el grafico de la serie temporal (grafico por defecto)
plt.scatter(data=cheetahRegion, x='Anio', y='Ventas')

# Genera el grafico de la serie temporal (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           

ax.plot('Anio','Ventas', data=cheetahRegion, marker="o")

ax.set_title('Ventas de la compañía Cheetah Sports')
ax.set_xlabel('Año', fontsize='medium')                       
ax.set_ylabel('Ventas (millones de $)', fontsize='medium')    
ax.set_xlim(0, 12)
ax.set_ylim(0, 250)

#%%
##### 8. DOS LINEAS EN UN MISMO EJE
# Genera el grafico de ambas series temporales (grafico por defecto)
fig, ax = plt.subplots()
ax.plot('Anio', 'regionEste' , data=cheetahRegion)
ax.plot('Anio', 'regionOeste', data=cheetahRegion)

# Genera el grafico de ambas series temporales (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           

# Grafica la serie regionEste 
ax.plot('Anio', 'regionEste', data=cheetahRegion, 
        marker='.',                                 # Tipo de punto (redondo, triángulo, cuadrado, etc.)
        linestyle='-',                              # Tipo de linea (solida, punteada, etc.)
        linewidth=0.5,                              # Ancho de linea 
        label='Ventas de la region Este',                        # Etiqueta que va a mostrar en la leyenda
        )

# Grafica la serie regionOeste
ax.plot('Anio', 'regionOeste', data=cheetahRegion, 
        marker='.',                                 # Tipo de punto (redondo, triángulo, cuadrado, etc.)
        linestyle='-',                              # Tipo de linea (solida, punteada, etc.)
        linewidth=0.5,                              # Ancho de linea 
        label='Región Oeste'                        # Etiqueta que va a mostrar en la leyenda
        )

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
ax.set_title('Ventas de la compañía Cheetah Sports según región')
ax.set_xlabel('Año')
ax.set_ylabel('Ventas (millones de $)')
ax.set_xlim(0,12)
ax.set_ylim(0,140)
# Muestra la leyenda
ax.legend()

#%%
#############################################################################
#                                                                           #
#                              MTCARS                                       #
#                                                                           #
#############################################################################
#### 9. HEATMAP + DENDOGRAMA

df = pd.read_csv(carpeta+"mtcars.csv") # Cargamos los datos
df = df.set_index('model') # Usamos el modelo de cada auto como indice del df

# Generamos el grafico por defecto
sns.clustermap(df) 
# Las escalas de las distintas columnas son muy distintas!
# Necesitamos estandarizar los datos a la hora de graficar

# Generamos el grafico mejorando la información mostrada
sns.clustermap(df,
               col_cluster = False,    # elimina el dendograma superior
               method = "single",      # método de agrupamiento utilizado
               cmap = "Blues",         # paleta de colores
               standard_scale = 1)     # estandarizamos los datos de c/ columna
plt.show()

#%%#########################EJERCICIOS#######################################
# Sean los siguientes datos correspondientes a los precios del 
# biodiesel en distintos períodos en la Argentina
# (se encuentran subidos en el campus) 


# Generar un gráfico para representarlos gráficamente
# Analizar los resultados obtenidos
# Discutir con el resto de la clase
# ¿Cuál fue su objetivo: Explorar, Explicar, Otro?
# ¿Qué tipos de variables estaban en juego?
# ¿Qué tipo de gráfico decidió utilizar?
# ¿Qué resultados obtuvo?
# ¿Mejoró alguna característica del gráfico para cumplir con el objetivo?
#############################################################################
# Sean los siguientes datos correspondientes a 
# poseedores de teléfonos 
# (se encuentran subidos en el campus) 


# Generar un gráfico para representarlos gráficamente
# Analizar los resultados obtenidos
# Discutir con el resto de la clase
# ¿Cuál fue su objetivo: Explorar, Explicar, Otro?
# ¿Qué tipos de variables estaban en juego?
# ¿Qué tipo de gráfico decidió utilizar?
# ¿Qué resultados obtuvo?
# ¿Mejoró alguna característica del gráfico para cumplir con el objetivo?
# Responder Verdadero o Falso y justificar visualmente. 
# “Es más probable que las personas mayores posean un teléfono 
# inteligente a que las personas más jóvenes posean uno inteligente.”



########## Precio Biodiesel########

# Genera el grafico de la serie temporal (grafico por defecto)
plt.scatter(data=df, x='Periodo', y='Precio')

df = sql^"""
        SELECT *
        FROM df
        ORDER BY periodo ASC;
        """
# Genera el grafico de la serie temporal (mejorando la informacion mostrada)
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'           

ax.plot('Periodo','Precio', data=df, marker="o")

plt.xticks(rotation=90)    
ax.set_title('Relacion Periodo-Precio')
ax.set_xlabel('Periodo', fontsize='medium')                       
ax.set_ylabel('Precio', fontsize='medium')    

#############################################################################
#%%##########################################################################
#                                                                           #
#                    DISTRIBUCION DE LOS DATOS                              #
#                                                                           #
#############################################################################


##### 1. DATOS CATEGORICOS - GASEOSAS

# Cargamos dataset gaseosas
gaseosas= pd.read_csv(carpeta+"gaseosas.csv")

# Mostramos las primeras observaciones
gaseosas.head()

# Tabla de frecuencias
gaseosas['Compras_gaseosas'].value_counts()    

# Genera el grafico de frecuencias (grafico por defecto)
gaseosas['Compras_gaseosas'].value_counts().plot.bar()

#%%
# Genera el grafico de frecuencias (mejorando la informacion mostrada)

plt.rcParams['font.family'] = 'sans-serif'           # Modifica el tipo de letra
plt.rcParams['axes.spines.right'] = False            # Elimina linea derecha  del recuadro
plt.rcParams['axes.spines.left']  = False            # Elimina linea izquierda  del recuadro
plt.rcParams['axes.spines.top']   = False            # Elimina linea superior del recuadro

fig, ax = plt.subplots()
gaseosas['Compras_gaseosas'].value_counts().plot.bar(ax = ax)

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
ax.set_title('Frecuencia Venta de Gaseosas')
ax.set_xlabel('Marcas de gaseosas') 
ax.set_yticks([])                                  # Remueve los ticks del eje y
ax.bar_label(ax.containers[0], fontsize=8)         # Agrega la etiqueta a cada barra
ax.tick_params(axis='x', labelrotation=0)          # Rota las etiquetas del eje x
                                                    # para que las muestre horizontales
plt.show()                 

#%%######### Frecuencias relativas
    
# Tabla de frecuencias relativas
gaseosas['Compras_gaseosas'].value_counts(normalize=True)
 

# Genera el grafico de frecuencias relativas (mejorando la informacion mostrada)

plt.rcParams['font.family'] = 'sans-serif'           # Modifica el tipo de letra
plt.rcParams['axes.spines.right'] = False            # Elimina linea derecha  del recuadro
plt.rcParams['axes.spines.left']  = False            # Elimina linea izquierda  del recuadro
plt.rcParams['axes.spines.top']   = False            # Elimina linea superior del recuadro

fig, ax = plt.subplots()

ax = gaseosas['Compras_gaseosas'].value_counts(normalize=True).plot.bar()


# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
ax.set_title('Frecuencia Relativa de Venta de Gaseosas')
ax.set_yticks([])                                           # Remueve los ticks del eje y
ax.bar_label(ax.containers[0], fontsize=8)                  # Agrega la etiqueta a cada barra
ax.tick_params(axis='x', labelrotation=0)                   # Rota las etiquetas del eje x para que las muestre horizontales
# En formato porcentual
# ax.set_title('Frecuencia Porcentual de Venta de Gaseosas')
# ax.bar_label(ax.containers[0], fontsize=8, fmt='{:.2%}') # Agrega la etiqueta a cada barra en formato de porcentaje

#%%

# # # # # # # # # # # # # # # # # # # # # # # # 
# #   Age at Death
# # # # # # # # # # # # # # # # # # # # # # # # 
# Cargamos dataset 
ageAtDeath= pd.read_csv(carpeta+"ageAtDeath.csv")

# Mostramos las primeras observaciones
ageAtDeath.head()

# Genera el grafico de frecuencias (mejorando la informacion mostrada)

plt.rcParams['font.family'] = 'sans-serif'           # Modifica el tipo de letra
plt.rcParams['axes.spines.right'] = False            # Elimina linea derecha  del recuadro
plt.rcParams['axes.spines.left']  = True             # Agrega  linea izquierda  del recuadro
plt.rcParams['axes.spines.top']   = False            # Elimina linea superior del recuadro

fig, ax = plt.subplots()

sns.histplot(data = ageAtDeath['AgeAtDeath'], bins = 17)

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes    
ax.set_title('Distribución de edades al momento de muerte')
ax.set_xlabel('Edad al momento de muerte (años)')
ax.set_ylabel('Cantidad de personas')
ax.set_ylim(0,160)


# ¿Que pasa si cambiamos la cantidad de bins?

# Vuelvan a generar el histograma/gráfico de frecuencias usando 2, 8 y 70 bins







########################## EXTRA ############################

# Pueden incluir un 'suavizado' del histograma configurando 
# como TRUE el parametro kde

fig, ax = plt.subplots()
sns.histplot(data = ageAtDeath['AgeAtDeath'], bins = 17, kde = True)

# La curva añadida se llama curva de densidad de kernel. Es una representación 
# suave de la distribución de los datos, que intenta estimar la función de 
# densidad de probabilidad de una variable continua.


#%% POR CATEGORIA
sns.histplot(data = ageAtDeath, x = 'AgeAtDeath', bins = 17, hue= 'Sex',
             palette = 'colorblind')
### HACER LO MISMO CON FREQ RELATIVA 
#%%############## DISTRIBUCION SEGUN DOS VARIABLES

fig, ax = plt.subplots()
sns.histplot(data = ageAtDeath,
             x = 'AgeAtDeath', 
             bins = 17, 
             hue= 'Sex',                # Coloreamos segun los valores de la columna 'Sex'
             palette = 'colorblind')

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes    
ax.set_title('Distribución de edades al momento de muerte')
ax.set_xlabel('Edad al momento de muerte (años)')
ax.set_ylabel('Cantidad de personas')
ax.set_ylim(0,100)


#%%
# - - - - - - - - - - - - - - - - - 
# Graficamos la frecuencia relativa
# - - - - - - - - - - - - - - - - - 

fig, ax = plt.subplots()
sns.histplot(data = ageAtDeath,
             x = 'AgeAtDeath', 
             bins = 17, 
             hue= 'Sex',                # Coloreamos segun los valores de la columna 'Sex'
             palette = 'colorblind',
             stat='probability')        # Mostrar frecuencias relativas en lugar de absolutas)

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes    
ax.set_title('Distribución de edades al momento de muerte')
ax.set_xlabel('Edad al momento de muerte (años)')
ax.set_ylabel('Frecuencia Relativa de Cantidad de personas')
ax.set_ylim(0,0.2)



#%%
# - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Graficamos la frecuencia relativa en forma de lineas
# - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig, ax = plt.subplots()
sns.histplot(data=ageAtDeath, 
             x='AgeAtDeath', 
             hue='Sex', 
             bins=17, 
             palette='colorblind', 
             stat='probability',  # Graficar frecuencias relativas
             element='poly',      # Mostrar como líneas
             fill=False)          # No llenar bajo la curva

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes 
ax.set_title('Distribución de edades al momento de muerte')
ax.set_xlabel('Edad al momento de muerte (años)')
ax.set_ylabel('Frecuencia Relativa de Cantidad de personas')
ax.set_ylim(0,0.2)
# Mostrar el gráfico
plt.show()
#%%
# Sean los datos correspondientes a las propinas de un bar 
# (están cargados en el campus en el archivo tips.csv)
# Generar un gráfico para analizar la distribución de la propina en función del:
# Sexo
# Día de la semana
# Comentar los resultados obtenidos

tips = pd.read_csv(carpeta+"tips.csv")

fig, ax = plt.subplots()
sns.histplot(data = tips,
             x = 'tip', 
             bins = 10, 
             hue= 'sex',             # Coloreamos segun los valores de la columna 'Sex'
             palette = 'colorblind',
             stat = 'probability')

# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes    
ax.set_title('Propinas')
ax.set_xlabel('Propina total')
ax.set_ylabel('Cantidad de personas')


# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes    
ax.set_title('Propinas')
ax.set_xlabel('Propina total')
ax.set_ylabel('Cantidad de personas')


fig, ax = plt.subplots()
sns.histplot(data = tips,
             x = 'tip', 
             bins = 10, 
             hue= 'day',             # Coloreamos segun los valores de la columna 'Sex'
             palette = 'colorblind',
             stat = 'probability')


# Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes    
ax.set_title('Propinas')
ax.set_xlabel('Propina total')
ax.set_ylabel('Cantidad de personas')

