#Abriendo archivos
# con '../Descargas/datame.txt' voy armando el path para llegar al archivo

nombre_archivo = 'datame.txt'

f = open(nombre_archivo, 'rt')

data = f.read()

print(data)
f.read()
f.close()

promedio = (df['nota1']+df['nota2'])/2
df['promedio'] = promedio

alu_nue = {'lu':['125/45'], 'nombre':['Juan'], 'apellido':['Perez'], 'nota1':[2], 'nota2':[10]}

df_alu_nue = pd.DataFrame(data = alu_nue)
df_alu_nue.set_index('lu', inplace = True)

df_nuevo = pd.concat([df, df_alu_nue])

df_nuevo.loc['125/45', 'promedio'] = 1

df_nuevo.loc['125/45', 'promedio'] = (df_nuevo.loc['125/45','nota1'] + df_nuevo.loc['125/45', 'nota2'])/2

df_nuevo['aprueba'] = (df_nuevo['nota1'] >= 5) & (df_nuevo['nota2'] >= 5)

df_nuevo['promociona'] = (df_nuevo['nota1'] >= 8) & (df_nuevo['nota2'] >= 8)

df_aprobados = df_nuevo[df_nuevo['nota1']>=5]
