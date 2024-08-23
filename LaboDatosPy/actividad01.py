import pandas as pd
import numpy as np

archivo = 'Clase-03-Actividad-01-Datos.csv'

df = pd.read_csv(archivo)

archivo2 = 'Encuesta de Movilidad - Respuestas de formulario 1.csv'

dfTransport = pd.read_csv(archivo2)
