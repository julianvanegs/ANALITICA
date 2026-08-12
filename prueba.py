# PASO 1 INSTALACION DE ENTORNO VIRTUAL
# python -m venv venv o python -m venv venv --without-pip
# venv\Scripts\Activate.ps1}
# python -m ensurepip --default-pi

# PASO 2 ESTABLECER CONEXION CON PANDA , NUMYP , POSTGRESS Y MATPLOITLIB E INSTALARLOS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Conexión adaptada a tu contenedor Docker funcional
engine = create_engine(
    "postgresql+psycopg2://postgres:1974@localhost:5434/postgres"
)

# PASO 4 LECTURA DE ARCHIVO
df = pd.read_csv(r"C:\Users\coder\Downloads\practica\my_file.csv")

# PASO 5 NORMALIZACION DE COLUMNAS
print("Estructura original:", df.shape)

# Convertimos columnas a minúsculas y guiones bajos
df.columns = (
    df.columns.str.strip().str.lower().str.replace(r'\s+', '_', regex=True)
)
df.columns = df.columns.str.replace('.', '_', regex=False)

# 🚀 CORRECCIÓN CLAVE: Renombramos explícitamente tanto la de dinero como la de años para evitar variaciones raras
df = df.rename(
    columns={
        'adjusted_gross_(in_2022_dollars)': 'adjusted_gross_in_2022_dollars',
        'year(s)': 'years',
        'year_s_': 'years'  # Por si el reemplazo automático ya lo había alterado
    }
)

# Listas de limpieza
columnas_dinero = ['actual_gross', 'adjusted_gross_in_2022_dollars', 'average_gross']
columnas_corchetes = ['rank', 'peak', 'tour_title', 'all_time_peak', 'actual_gross']

# Limpieza de corchetes y caracteres raros
for col in columnas_corchetes:
    df[col] = df[col].astype(str).str.replace(r'\[.*?\]', '', regex=True)

if 'ref_' in df.columns:
    df['ref_'] = df['ref_'].astype(str).str.replace(r'\[(.*?)\]', r'\1', regex=True)

# Limpieza de signos de dinero y comas
for col in columnas_dinero:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
    )

# Relleno de nulos y conversión de tipos
df = df.fillna('Desconocido') 
df['actual_gross'] = df['actual_gross'].astype(int)
df['tour_title'] = df['tour_title'].astype(str).str.title()
df['artist'] = df['artist'].astype(str).str.title()

df = df.drop_duplicates()

# =====================================================================
# 🚀 PROCESO DE NORMALIZACIÓN A LA TERCERA FORMA NORMAL (3FN)
# =====================================================================

# 1. Entidad: ARTISTAS (Catálogo Único)
artistas = df[['artist']].drop_duplicates().reset_index(drop=True)
artistas['id_artista'] = artistas.index + 1
artistas = artistas[['id_artista', 'artist']]

# 2. Entidad: TOURS / GIRAS (Depende del Artista) - 🚀 Usando el nuevo nombre 'years'
tours = df[['tour_title', 'artist', 'years']].drop_duplicates().reset_index(drop=True)
tours = tours.merge(artistas, on='artist')
tours['id_tour'] = tours.index + 1
tours = tours[['id_tour', 'tour_title', 'id_artista', 'years']]

# 3. Entidad de Hechos: REGISTRO CONCIERTOS (Vincula las métricas con el Tour)
registro_conciertos = df.copy()
# Combinamos con la tabla intermedia para obtener el ID del tour correlativo
registro_conciertos = registro_conciertos.merge(tours, on=['tour_title', 'years'])

# Seleccionamos las columnas numéricas y de control, usando 'id_tour' como nexo relacional
registro_conciertos = registro_conciertos[[
    'rank',
    'peak',
    'all_time_peak',
    'id_tour',        # Llave foránea hacia tours
    'shows',
    'actual_gross',
    'adjusted_gross_in_2022_dollars',
    'average_gross',
    'ref_'
]]

# =====================================================================
# 🚀 PASO FINAL: ENVIAR LAS TABLAS SEPARADAS A POSTGRESQL (3FN)
# =====================================================================

print("Cargando entidades 3FN a la base de datos...")

artistas.to_sql(
    "artistas",
    engine,
    if_exists="replace",
    index=False
)

tours.to_sql(
    "tours",
    engine,
    if_exists="replace",
    index=False
)

registro_conciertos.to_sql(
    "registro_conciertos",
    engine,
    if_exists="replace",
    index=False
)

print("¡Tablas creadas y cargadas con éxito en la 3FN! 🎉")

# Prueba rápida de lectura para verificar que los datos estén arriba
consulta_prueba = pd.read_sql(
    "SELECT * FROM artistas LIMIT 5",
    engine
)
print("\n--- MUESTRA TABLA ARTISTAS DESDE POSTGRES ---")
print(consulta_prueba)

# Configuración de salida
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
