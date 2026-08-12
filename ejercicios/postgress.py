import numpy as np
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:@localhost:5432/tiendamax"
)


columnas_str = ['cliente_nombre', 'cliente_tipo', 
                'sucursal', 'ciudad_sucursal', 'vendedor', 'producto',
                'categoria_producto','metodo_pago']




df = pd.read_csv(r"C:\Users\coder\Downloads\julian\ventas_desnormalizado.csv")

print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
df.columns = (df.columns.str.replace(' ', '_')
              .str.lower()
              .str.strip())


df[columnas_str] = df[columnas_str].astype(str).apply(lambda x: x.str.title())

df['cliente_email'] = df['cliente_email'].fillna('Desconocido') 


df['total_venta'] = df['total_venta'].fillna(df['total_venta'].median())

df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], format="mixed")

df = df.drop_duplicates()


##NORMALIZATION 3FN

categorias = df[['categoria_producto']].drop_duplicates().reset_index(drop=True)
categorias["id_categoria"] = categorias.index + 1
categorias = categorias[['id_categoria', 'categoria_producto']]


productos = df[["producto", "categoria_producto", "precio_unitario"]].drop_duplicates()
productos = productos.merge(categorias, on="categoria_producto")
productos["id_producto"] = range(1, len(productos) + 1)
productos = productos[["id_producto", "producto", "id_categoria", "precio_unitario"]]


clientes = df[["cliente_nombre", "cliente_email", "cliente_tipo"]].drop_duplicates()
clientes["id_cliente"] = range(1, len(clientes) + 1)
clientes = clientes[["id_cliente", "cliente_nombre", "cliente_email", "cliente_tipo"]]

sucursales = df[["sucursal", "ciudad_sucursal"]].drop_duplicates()
sucursales["id_sucursal"] = range(1, len(sucursales) + 1)
sucursales = sucursales[["id_sucursal", "sucursal", "ciudad_sucursal"]]

vendedores = df[["vendedor", "sucursal"]].drop_duplicates()
vendedores = vendedores.merge(sucursales, on="sucursal")
vendedores["id_vendedor"] = range(1, len(vendedores) + 1)
vendedores = vendedores[["id_vendedor", "vendedor", "id_sucursal"]]

metodos = df[["metodo_pago"]].drop_duplicates()
metodos["id_metodo"] = range(1, len(metodos) + 1)
metodos = metodos[["id_metodo", "metodo_pago"]]

ventas = df.copy()
ventas = ventas.merge(clientes,on=["cliente_nombre", "cliente_email", "cliente_tipo"])
ventas = ventas.merge(productos,on=["producto", "precio_unitario"])
ventas = ventas.merge(vendedores,on="vendedor")

ventas = ventas.merge(metodos,on="metodo_pago")

ventas = ventas[[
        "id_venta",
        "fecha_venta",
        "id_cliente",
        "id_vendedor",
        "id_producto",
        "cantidad",
        "descuento_pct",
        "id_metodo",
        "total_venta",
    ]
]

categorias.to_sql(
    "categorias",
    engine,
    if_exists="replace",
    index=False
)

productos.to_sql(
    "productos",
    engine,
    if_exists="replace",
    index=False
)

clientes.to_sql(
    "clientes",
    engine,
    if_exists="replace",
    index=False
)

sucursales.to_sql(
    "sucursales",
    engine,
    if_exists="replace",
    index=False
)

vendedores.to_sql(
    "vendedores",
    engine,
    if_exists="replace",
    index=False
)

metodos.to_sql(
    "metodos_pago",
    engine,
    if_exists="replace",
    index=False
)

ventas.to_sql(
    "ventas",
    engine,
    if_exists="replace",
    index=False
)
consulta = pd.read_sql(
    "SELECT * FROM clientes LIMIT 5",
    engine
)

print(consulta)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


