# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 09:53:16 2024

@author: Sebastián
"""

# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val

#%%

carpeta = "C:\\Users\\Sebastián\\Documents\\LaboDeDatos\\ejSQL\\"

casos = pd.read_csv(carpeta+"casos.csv")

departamento = pd.read_csv(carpeta+"departamento.csv")

grupoetario = pd.read_csv(carpeta+"grupoetario.csv")

provincia = pd.read_csv(carpeta+"provincia.csv")

tipoevento = pd.read_csv(carpeta+"tipoevento.csv")

#%%

#ej A

#a

consultaSQL = """
                SELECT Descripcion
                FROM departamento;
              """

dataframeResultado = sql^ consultaSQL

#%%
#b

consultaSQL = """
                SELECT DISTINCT Descripcion
                FROM departamento;
              """

dataframeResultado = sql^ consultaSQL

#%%
#c

consultaSQL = """
                SELECT DISTINCT id, Descripcion
                FROM departamento;
              """

dataframeResultado = sql^ consultaSQL

#%%
#d

consultaSQL = """
                SELECT DISTINCT *
                FROM departamento;
              """

dataframeResultado = sql^ consultaSQL

#%%
#e

consultaSQL = """
                SELECT DISTINCT id AS codigo_depto, Descripcion AS nombre_depto
                FROM departamento;
              """

dataframeResultado = sql^ consultaSQL

#%%
#f

consultaSQL = """
                SELECT DISTINCT *
                FROM departamento
                WHERE id_provincia = 54;
              """

dataframeResultado = sql^ consultaSQL

#%%
#g

consultaSQL = """
                SELECT DISTINCT *
                FROM departamento
                WHERE id_provincia = 22 OR id_provincia = 78 OR id_provincia = 86;
              """

dataframeResultado = sql^ consultaSQL

#%%
#h

consultaSQL = """
               SELECT DISTINCT *
               FROM departamento
               WHERE id_provincia >= 50 AND id_provincia <=59;
              """

dataframeResultado = sql^ consultaSQL

#%%
#ej B

#a

consultaSQL = """
               SELECT DISTINCT d.id, d.Descripcion, p.Descripcion
               FROM departamento as d
               INNER JOIN provincia as p
               ON d.id_provincia = p.id;
              """

dataframeResultado = sql^ consultaSQL

#%%

#b

consultaSQL = """

              """

dataframeResultado = sql^ consultaSQL

#%%

#c

casosConIdProv = sql^"""
                         SELECT DISTINCT c.id, c.id_tipoevento, c.anio, c.semana_epidemiologica, c.id_grupoetario, c.cantidad, d.id_provincia
                         FROM casos as c
                         INNER JOIN departamento as d
                         ON c.id_depto = d.id;
                        """
                     
casosEnChaco = sql^"""
                    SELECT DISTINCT c.id, c.id_tipoevento, c.anio, c.semana_epidemiologica, c.id_grupoetario, c.cantidad, p.descripcion 
                    FROM casosConIdProv as c
                    INNER JOIN provincia as p
                    ON c.id_provincia = p.id
                    WHERE p.descripcion = 'Chaco';
                   """


#%%

#d

casosConIdProvMA10 = sql^"""
                         SELECT DISTINCT c.id, c.id_tipoevento, c.anio, c.semana_epidemiologica, c.id_grupoetario, c.cantidad, d.id_provincia
                         FROM casos AS c
                         INNER JOIN departamento AS d
                         ON c.id_depto = d.id
                         WHERE c.cantidad > 10;
                        """
                     
casosEnBA = sql^"""
                    SELECT DISTINCT c.id, c.id_tipoevento, c.anio, c.semana_epidemiologica, c.id_grupoetario, c.cantidad, p.deScripcion AS prov
                    FROM casosConIdProvMA10 AS c
                    INNER JOIN provincia AS p
                    ON c.id_provincia = p.id
                    WHERE prov = 'Buenos Aires';
                   """


#%%

#EJ C

#a
consultaSQL = """
                SELECT DISTINCT d.descripcion
                FROM departamento AS d
                LEFT OUTER JOIN casos AS c
                ON d.id = c.id_depto
                WHERE c.cantidad IS NULL;
              """

dataframeResultado = sql^ consultaSQL

#%% 
#b

consultaSQL = """
                SELECT DISTINCT te.id, te.descripcion
                FROM tipoevento as te
                lEFT OUTER JOIN casos as c
                ON te.id = c.id_tipoevento
                WHERE c.cantidad IS NULL;
              """

dataframeResultado = sql^ consultaSQL

#%%

#ej D

#a

consultaSQL = """
                SELECT count(*) AS cantidad_de_casos
                FROM casos;
              """

dataframeResultado = sql^ consultaSQL

#%%

#b
tablaCasosEvento = sql^"""
                        SELECT DISTINCT te.descripcion, c.anio, c.cantidad
                        FROM casos AS C
                        INNER JOIN tipoevento as te
                        ON c.id_tipoevento = te.id
                   """


consultaSQL = """
                SELECT DISTINCT  descripcion,anio, sum(cantidad) as cantidad_de_casos
                FROM tablaCasosEvento
                GROUP BY anio, descripcion
                ORDER BY descripcion ASC, anio ASC;
              """

dataframeResultado = sql^ consultaSQL

#%%

#c

tablaCasosEvento = sql^"""
                        SELECT DISTINCT te.descripcion, c.anio, c.cantidad
                        FROM casos AS C
                        INNER JOIN tipoevento as te
                        ON c.id_tipoevento = te.id
                        WHERE c.anio = 2019;
                   """


consultaSQL = """
                SELECT DISTINCT  descripcion,anio, sum(cantidad) as cantidad_de_casos
                FROM tablaCasosEvento
                GROUP BY anio, descripcion
                ORDER BY descripcion ASC, anio ASC;
              """

dataframeResultado = sql^ consultaSQL


#%%

#d

consultaSQL = """
                SELECT DISTINCT id_provincia, p.descripcion,  count(*) as cantidad_deptos
                FROM departamento AS d
                INNER JOIN provincia AS p
                ON d.id_provincia = p.id
                GROUP BY p.descripcion, id_provincia
                ORDER BY id_provincia ASC;
              """

dataframeResultado = sql^ consultaSQL

#%%

#e

consultaSQL = sql^"""
                SELECT DISTINCT d.id, d.descripcion, SUM(c.cantidad) AS cantidad_casos
                FROM departamento AS d
                INNER JOIN casos AS c
                ON d.id = c.id_depto
                WHERE c.anio = 2019
                GROUP BY d.id, d.descripcion
                ORDER BY cantidad_casos ASC
                LIMIT 10;
              """

                         
#%%                         

#f

consultaSQL = """
                SELECT DISTINCT d.id, d.descripcion, SUM(c.cantidad) AS cantidad_casos
                FROM departamento AS d
                INNER JOIN casos AS c
                ON d.id = c.id_depto
                WHERE c.anio = 2020
                GROUP BY d.id, d.descripcion
                ORDER BY cantidad_casos DESC
                LIMIT 10;
              """

dataframeResultado = sql^ consultaSQL



#%%

#g

casosConDepto = sql^"""
                SELECT DISTINCT c.anio, c.cantidad, d.id_provincia
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """
              
casosConProv = sql^"""
                    SELECT DISTINCT c.anio, c.cantidad, p.descripcion
                    FROM casosConDepto as c
                    INNER JOIN provincia as p
                    ON c.id_provincia = p.id
                   """

dataframeResultado = sql^"""
                          SELECT DISTINCT anio, descripcion, AVG(cantidad) AS prom_cantidad
                          FROM casosConProv
                          GROUP BY anio, descripcion
                         """

#%%

#h

casosConDepto = sql^"""
                SELECT DISTINCT c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """
              
casosConProv = sql^"""
                    SELECT DISTINCT c.anio, c.cantidad, c.depto, p.descripcion AS prov, 
                    FROM casosConDepto as c
                    INNER JOIN provincia as p
                    ON c.id_provincia = p.id
                   """
                   
casosTotalesXDepto = sql^"""
                          SELECT DISTINCT depto, prov, anio, SUM(cantidad) AS cant_total
                          FROM casosConProv
                          GROUP BY anio, prov, depto
                          ORDER BY cant_total DESC
                         """

dataFrameResultado = sql^"""
                         SELECT DISTINCT c.prov, c.anio, c.depto, c.cant_total
                         FROM casosTotalesXDepto AS c
                         INNER JOIN (
                             SELECT prov, anio, MAX(cant_total) AS max_cant_total
                             FROM casosTotalesXDepto
                             GROUP BY prov, anio
                         ) AS max_casos
                         ON c.prov = max_casos.prov AND c.anio = max_casos.anio AND c.cant_total = max_casos.max_cant_total
                         ORDER BY c.prov, c.anio;
                         """
                         
#%%                         
                         
#i
                         
casosConDepto = sql^"""
                SELECT DISTINCT c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
                WHERE c.anio = 2019
              """

casosBSAS = sql^"""
                 SELECT DISTINCT c.anio, c.cantidad, p.descripcion
                 FROM casosConDepto as c
                 INNER JOIN provincia as p
                 ON c.id_provincia = p.id
                 WHERE p.descripcion = 'Buenos Aires'
                """                    
                         
dataFrameResultado = sql^"""
                          SELECT SUM(cantidad) AS casos_totales, MAX(cantidad) AS casos_max, MIN(cantidad) AS casos_min, AVG(cantidad) AS casos_prom
                          FROM casosBSAS
                         """

#%%
     
#j                    
casosConDepto = sql^"""
                SELECT DISTINCT c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
                WHERE c.anio = 2019 AND c.cantidad > 1000
              """

casosBSAS = sql^"""
                 SELECT DISTINCT c.anio, c.cantidad, p.descripcion
                 FROM casosConDepto as c
                 INNER JOIN provincia as p
                 ON c.id_provincia = p.id
                 WHERE p.descripcion = 'Buenos Aires'
                """                    
                         
dataFrameResultado = sql^"""
                          SELECT SUM(cantidad) AS casos_totales, MAX(cantidad) AS casos_max, MIN(cantidad) AS casos_min, AVG(cantidad) AS casos_prom
                          FROM casosBSAS
                         """                         

#%%

#k

casosConDepto = sql^"""
                SELECT DISTINCT c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """

casosConProv = sql^"""
                    SELECT DISTINCT c.anio, c.cantidad, c.depto, p.descripcion AS prov
                    FROM casosConDepto AS c
                    INNER JOIN provincia AS p 
                    ON c.id_provincia = p.id
                   """

deptos19Y20 = sql^"""
                    SELECT DISTINCT c1.prov, c1.depto, AVG(c1.cantidad) AS prom
                    FROM casosConProv as c1
                    WHERE c1.depto IN (
                        SELECT DISTINCT depto
                        FROM casosConProv AS c2
                        GROUP BY c2.depto
                        HAVING COUNT(DISTINCT c2.anio) = 2
                        )
                    GROUP BY c1.prov, c1.depto
                    ORDER BY c1.prov, c1.depto;
                  """
                  
#%%

#l


casosConDepto = sql^"""
                SELECT DISTINCT c.id_depto, d.descripcion AS depto, d.id_provincia, c.cantidad, c.id_tipoevento, c.anio
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """

casosConProv = sql^"""
                    SELECT DISTINCT c.id_depto, c.depto, c.id_provincia, p.descripcion AS prov, c.cantidad, c.id_tipoevento, c.anio
                    FROM casosConDepto AS c
                    INNER JOIN provincia AS p 
                    ON c.id_provincia = p.id
                   """

casosConTipoEvento = sql^"""
                          SELECT DISTINCT te.descripcion AS tipo_evento, c.id_depto, c.depto, c.id_provincia, c.prov 
                          FROM casosConProv AS c
                          INNER JOIN tipoevento AS te
                          ON c.id_tipoevento = te.id;
                         """

casos19 = sql^"""
               SELECT DISTINCT c.id_depto, SUM(c.cantidad) AS total_de_casos19
               FROM casosConProv AS c
               WHERE c.anio = 2019
               GROUP BY c.id_depto;
              """
                         
casos20 = sql^"""
               SELECT DISTINCT c.id_depto, SUM(c.cantidad) AS total_de_casos20
               FROM casosConProv AS c
               WHERE c.anio = 2020
               GROUP BY c.id_depto;
              """              

dataframeResultado19 = sql^"""
                          SELECT c.tipo_evento, c.id_depto, c.depto, c.id_provincia, c.prov, c1.total_de_casos19
                          FROM casosConTipoEvento AS c
                          LEFT OUTER JOIN casos19 AS c1
                          ON c.id_depto = c1.id_depto;
                         """

dataframeResultado = sql^"""
                          SELECT c.tipo_evento, c.id_depto, c.depto, c.id_provincia, c.prov, c.total_de_casos19, c1.total_de_casos20
                          FROM dataframeResultado19 AS c
                          LEFT OUTER JOIN casos20 AS c1
                          ON c.id_depto = c1.id_depto;
                         """
                         
                         
                         
                         
