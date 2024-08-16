#Abriendo archivos
# con '../Descargas/datame.txt' voy armando el path para llegar al archivo

nombre_archivo = 'datame.txt'

f = open(nombre_archivo, 'rt')

data = f.read()

print(data)
f.read()
f.close()
