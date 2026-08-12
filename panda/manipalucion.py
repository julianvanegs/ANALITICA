import numpy as np
import pandas as pd

df = pd.read_csv(r"C:\Users\coder\Downloads\julian\MOCK_DATA.csv")

#Convert a negative number tu positive
df['stock'] = df['stock'].abs()
df['precio_compra'] = df['precio_compra'].abs()
df['precio_venta'] = df['precio_venta'].abs()

#Normalize all string have the firt letter upper
df['producto'] = df['producto'].str.capitalize()
df['categoria'] = df['categoria'].str.capitalize()
df['proveedor'] = df['proveedor'].str.capitalize()

#Change the Nan text to a Desconocido
df["proveedor"] = df["proveedor"].fillna("Desconocido")

#Get the median 
mediana = df["precio_compra"].median()

#Change the Nan to the median
df["precio_compra"] = df["precio_compra"].fillna(mediana)

#Eliminate the row with a stock Nan
df = df.dropna(subset=["stock"])

#filter
filtro = df[df["precio_venta"] < df["precio_compra"]]


df['margen'] = df['precio_venta'] - df['precio_compra']

df['margen_porcentual'] = df['margen'] / df['precio_venta'] * 100
margen_categoria = df.groupby('categoria')['margen_porcentual'].mean()
margen_porcentual_total = df['margen_porcentual'].sum()
margen_total = df['margen'].sum()

producto_mayor_margen = df.loc[df['margen_porcentual'].idxmax()]

df['fecha_actualizacion'] = df['fecha_actualizacion'].str.strip()

df['fecha_actualizacion'] = pd.to_datetime(
    df['fecha_actualizacion'],
    format="%d/%m/%Y"
)

productos_antiguos = (
    df.sort_values("fecha_actualizacion")
    [["producto", "fecha_actualizacion"]]
    .head(5)
)




duplicados = df.drop_duplicates(['id_producto', 'producto', 'categoria', 'proveedor', 'stock', 'precio_compra', 'precio_venta', 'fecha_actualizacion'])


print("\n========== RESUMEN DEL INVENTARIO ==========")

print("\n========== VALOR TOTAL DEL INVENTARIO ==========")

df["valor_inventario"] = df["stock"] * df["precio_compra"]

valor_total_inventario = df["valor_inventario"].sum()

print(f"Capital total invertido: {valor_total_inventario:.2f} €")


print("\n========== CAPITAL INVERTIDO POR CATEGORÍA ==========")

inventario_categoria = (
    df.groupby("categoria")["valor_inventario"].sum()
  
)

print(inventario_categoria)




print(f"Margen total: {margen_total:.2f}")

print(f"Margen porcentual promedio: {margen_porcentual_total / len(df):.2f}%")


print("\n========== PRODUCTO CON MAYOR MARGEN ==========")

print(f"Producto: {producto_mayor_margen['producto']}")
print(f"Categoría: {producto_mayor_margen['categoria']}")
print(f"Margen porcentual: {producto_mayor_margen['margen_porcentual']:.2f}%")
print(f"Ganancia por unidad: {producto_mayor_margen['margen']:.2f}")


print("\n========== MARGEN POR CATEGORÍA ==========")

print(margen_categoria.round(2))





print(filtro[['producto', 'categoria', 'precio_compra', 'precio_venta']])


print("\n========== PRODUCTOS MAS ANTIGUOS ==========")
print(productos_antiguos)

print("\n========== TABLA LIMPIA ==========")

print(duplicados)



