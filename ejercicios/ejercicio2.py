import pandas as pd
datos = {'Mes':['Enero','Febrero','Marzo','Abril'],'Ventas':[2000,3000,4000,5000], 'Gastos':[1000,200,3000,4000]}

tabla = pd.DataFrame(datos)


print(tabla['Mes'])
