import pandas as pd
datos = {'Mes':['Enero','Febrero','Marzo','Abril'],'Ventas':[2000,3000,4000,5000], 'Gastos':[1000,200,3000,4000]}

contabilidad = pd.DataFrame(datos)

def balance(contabilidad, meses):
    contabilidad['Balance'] = contabilidad.Ventas - contabilidad.Gastos
    return contabilidad.set_index('Mes').loc[meses,'Balance'].sum()


print(balance)
print(balance(contabilidad,['Enero','Febrero']))

     