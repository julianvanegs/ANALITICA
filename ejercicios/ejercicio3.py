import pandas as pd
datos = {'Mes':['Enero','Febrero','Marzo','Abril'],'Ventas':[2000,3000,4000,5000], 'Gastos':[1000,200,3000,4000]}

tabla = pd.DataFrame(datos)

filter = tabla[['Mes', 'Ventas']]
filterForRows = tabla.iloc[0:5]


filter_by_cost = tabla[(tabla.Mes == 'Enero') & (tabla.Gastos == 1000)]
filter_by_age = tabla[(tabla.Ventas >= 2000) &(tabla.Ventas <= 4000)]

#change with loc the column Gastos on the 3 row to 2000
tabla.loc[3,'Gastos'] = 2000

#sum of columns and mean of the results
resultado = tabla[['Gastos' , 'Ventas']].sum()
mean = resultado.mean()



