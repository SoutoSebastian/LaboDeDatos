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

#carpeta = "~/Escritorio/LaboDeDatos/ejSQL/"

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

departamentosC = sql^"""
                      SELECT DISTINCT id_depto
                      FROM casos
                     """
departamentos = sql^"""
                     SELECT DISTINCT id
                     FROM departamento
                    """

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
                        SELECT DISTINCT te.descripcion, c.anio, c.cantidad, c.id
                        FROM casos AS c
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
                        SELECT DISTINCT te.descripcion, c.anio, c.cantidad, c.id
                        FROM casos AS c
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
                SELECT id_provincia, p.descripcion,  count(*) as cantidad_deptos
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
                HAVING cantidad_casos = 1
                ORDER BY cantidad_casos ASC;
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
                SELECT DISTINCT c.id, c.anio, c.cantidad, d.id_provincia
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """
              
casosConProv = sql^"""
                    SELECT DISTINCT c.id, c.anio, c.cantidad, p.descripcion AS prov
                    FROM casosConDepto as c
                    INNER JOIN provincia as p
                    ON c.id_provincia = p.id
                   """

dataframeResultado = sql^"""
                          SELECT  anio, prov, AVG(cantidad) AS prom_cantidad
                          FROM casosConProv
                          GROUP BY anio, prov
                          ORDER BY anio;
                         """

#%%

#h

casosConDepto = sql^"""
                SELECT DISTINCT c.id, c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """
              
casosConProv = sql^"""
                    SELECT DISTINCT c.id, c.anio, c.cantidad, c.depto, p.descripcion AS prov, 
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
                SELECT DISTINCT c.id, c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
                WHERE c.anio = 2019
              """

casosBSAS = sql^"""
                 SELECT DISTINCT c.id, c.anio, c.cantidad, p.descripcion
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
                SELECT DISTINCT c.id, c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
                WHERE c.anio = 2019 AND c.cantidad > 1000
              """

casosBSAS = sql^"""
                 SELECT DISTINCT c.id, c.anio, c.cantidad, p.descripcion
                 FROM casosConDepto as c
                 INNER JOIN provincia as p
                 ON c.id_provincia = p.id
                 WHERE p.descripcion = 'Buenos Aires'
                """                    
                         
dataFrameResultado = sql^"""
                          SELECT SUM(cantidad) AS casos_totales, MAX(cantidad) AS casos_max, MIN(cantidad) AS casos_min, AVG(cantidad) AS casos_prom
                          FROM casosBSAS
                         """
#no entiendo bien la consigna, otra opcion seria ver todas las provincias que tengan cant_total > 1000


casosConDepto = sql^"""
                SELECT DISTINCT c.id, c.anio, c.cantidad, d.id_provincia, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """

casosConProv = sql^"""
                 SELECT DISTINCT c.id, c.anio, c.cantidad, p.descripcion AS prov
                 FROM casosConDepto as c
                 INNER JOIN provincia as p
                 ON c.id_provincia = p.id;
                """  

dataFrameResultado2 = sql^"""
                          SELECT prov, SUM(cantidad) AS casos_totales, MAX(cantidad) AS casos_max, MIN(cantidad) AS casos_min, AVG(cantidad) AS casos_prom
                          FROM casosConProv
                          GROUP BY prov
                          HAVING casos_totales >1000
                         """                         

#%%

#k

casosConDepto = sql^"""
                SELECT DISTINCT c.id, c.anio, c.cantidad, d.id_provincia, d.id AS id_depto, d.descripcion AS depto
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """

casosConProv = sql^"""
                    SELECT DISTINCT c.id, c.anio, c.cantidad, c.id_depto, c.depto, p.descripcion AS prov
                    FROM casosConDepto AS c
                    INNER JOIN provincia AS p 
                    ON c.id_provincia = p.id
                   """

deptos19Y20 = sql^"""
                    SELECT DISTINCT c1.prov, c1.depto, AVG(c1.cantidad) AS prom
                    FROM casosConProv as c1
                    WHERE c1.id_depto IN (
                        SELECT DISTINCT c2.id_depto
                        FROM casosConProv AS c2
                        GROUP BY c2.prov, c2.id_depto
                        HAVING COUNT(DISTINCT c2.anio) = 2
                        )
                    GROUP BY c1.prov, c1.depto
                    ORDER BY c1.depto, c1.prov, c1.depto;
                  """

#otra opcion con interseccion:

deptos19 = sql^"""
                SELECT DISTINCT  id_depto
                FROM casosConProv
                WHERE anio = 2019
               """
deptos20 = sql^"""
                SELECT DISTINCT  id_depto
                FROM casosConProv
                WHERE anio = 2020
               """               

deptosAmbosAños = sql^"""
                        SELECT DISTINCT *
                        FROM deptos19
                        INTERSECT
                        SELECT DISTINCT *
                        FROM deptos20;
                      """


                  
#%%

#l


casosConDepto = sql^"""
                SELECT DISTINCT c.id, c.id_depto, d.descripcion AS depto, d.id_provincia, c.cantidad, c.id_tipoevento, c.anio
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """

casosConProv = sql^"""
                    SELECT DISTINCT c.id, c.id_depto, c.depto, c.id_provincia, p.descripcion AS prov, c.cantidad, c.id_tipoevento, c.anio
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
                         

#%%


#ej E

#a

casosConDepto = sql^"""
                SELECT DISTINCT c.id_depto, d.descripcion, SUM(c.cantidad) AS cantidad_casos
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
                GROUP BY c.id_depto, d.descripcion;
              """

DeptoConMasCasos = sql^"""
                        SELECT c1.descripcion
                        FROM casosConDepto AS c1
                        WHERE c1.cantidad_casos >= ALL (
                            SELECT c2.cantidad_casos
                            FROM casosConDepto AS c2
                            );
                      """

#%%

#b

dataframeResultado = sql^"""
                         SELECT te.descripcion
                         FROM tipoevento AS te
                         WHERE te.id = ANY (
                             SELECT DISTINCT c.id_tipoevento
                             FROM casos AS c
                             );
                        """

#%%

#EJF

#a

dataframeResultado = sql^"""
                          SELECT te.descripcion
                          FROM tipoevento AS te
                          WHERE te.id IN(
                              SELECT DISTINCT c.id_tipoevento
                              FROM casos AS c
                              );
                         """
                         
#%%

#b

dataframeResultado = sql^"""
                          SELECT te.descripcion
                          FROM tipoevento AS te
                          WHERE te.id NOT IN(
                              SELECT DISTINCT c.id_tipoevento
                              FROM casos AS c
                              );
                         """

#%%

#EJH

#a

dataframeResultado = sql^"""
                          SELECT te.descripcion
                          FROM tipoevento AS te
                          WHERE EXISTS (
                              SELECT DISTINCT c.id_tipoevento
                              FROM casos AS c
                              WHERE te.id = c.id_tipoevento
                              );
                         """

#%%

#b

dataframeResultado = sql^"""
                          SELECT te.descripcion
                          FROM tipoevento AS te
                          WHERE NOT EXISTS (
                              SELECT DISTINCT c.id_tipoevento
                              FROM casos AS c
                              WHERE te.id = c.id_tipoevento
                              );
                         """
                      
#%%

#EJH

#a

casosConDepto = sql^"""
                SELECT DISTINCT c.id_depto, d.descripcion AS depto, d.id_provincia, c.cantidad, c.anio
                FROM casos as c
                INNER JOIN departamento as d
                ON c.id_depto = d.id
              """

casosConProv = sql^"""
                    SELECT DISTINCT c.id_depto, c.depto, c.id_provincia, p.descripcion AS prov, c.cantidad, c.anio
                    FROM casosConDepto AS c
                    INNER JOIN provincia AS p 
                    ON c.id_provincia = p.id
                   """

casosProv = sql^"""
                 SELECT DISTINCT c.anio, c.prov, SUM(c.cantidad) AS cantidad_casos
                 FROM casosConProv AS c
                 GROUP BY c.anio, c.prov;
                """


dataframeResultado = sql^"""
                          SELECT DISTINCT c1.anio, c1.prov, c1.cantidad_casos
                          FROM casosProv AS c1
                          WHERE c1.cantidad_casos >= (
                              SELECT AVG(c2.cantidad_casos)
                              FROM casosProv AS c2
                              );
                         
                         """

#%%
                         
                         
#b
                         













