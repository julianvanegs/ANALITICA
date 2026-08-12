# PASO 1 INSTALACION DE ENTORNO VIRTUAL
# python -m venv venv o python -m venv venv --without-pip
# venv\Scripts\Activate.ps1}
# python -m ensurepip --default-pi

# PASO 2 ESTABLECER CONEXION CON PANDA , NUMYP , POSTGRESS Y MATPLOITLIB E INSTALARLOS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# PASO 4 LECTURA DE ARCHIVO
df = pd.read_csv(r"C:\Users\coder\Downloads\practica\my_file.csv")

# PASO 5 NORMALIZACION DE COLUMNAS
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())

# 1. CORRECCIÓN: Renombramos la columna con paréntesis ANTES de cambiar todas las columnas a minúsculas
df = df.rename(
    columns={
        'Adjusted gross (in 2022 dollars)': 'adjusted_gross_in_2022_dollars'
    }
)

# 2. Convertimos el resto de columnas a minúsculas y guiones bajos
df.columns = (
    df.columns.str.strip().str.lower().str.replace(r'\s+', '_', regex=True)
)

# Como el punto de 'Ref.' pasó por la normalización, ahora se llama 'ref_' (con guión bajo)
df.columns = df.columns.str.replace('.', '_', regex=False)

# Listas de trabajo con los nombres de columnas ya normalizados
columnas_dinero = [
    'actual_gross',
    'adjusted_gross_in_2022_dollars',
    'average_gross',
]

columnas_corchetes = [
    'rank',
    'peak',
    'tour_title',
    'all_time_peak',
    'actual_gross',
]

# 3. QUITAR CORCHETES CON NÚMEROS O SIGNOS RAROS
for col in columnas_corchetes:
    df[col] = df[col].astype(str).str.replace(r'\[.*?\]', '', regex=True)

# 4. QUITAR CORCHETES DEJANDO EL NÚMERO INTERNO EN LA REFERENCIA
if 'ref_' in df.columns:
    df['ref_'] = (
        df['ref_'].astype(str).str.replace(r'\[(.*?)\]', r'\1', regex=True)
    )

# 5. LIMPIAR SIGNOS DE DINERO ($ y comas)
for col in columnas_dinero:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
    )

# 6. Convertir textos vacíos o "nan" accidentales en valores nulos reales (NaN)
df = df.fillna('Desconocido') 


df['actual_gross'] = df['actual_gross'].astype(int) 
# 7. CORRECCIÓN: Cambiar tipos de datos de forma masiva y segura (Soporta celdas vacías)

# Convertir las columnas de texto explícitamente
df['tour_title'] = df['tour_title'].astype(str)
df['artist'] = df['artist'].astype(str)

# ELIMINAR DUPLICADOS EN TODAS LAS COLUMNAS
df = df.drop_duplicates(ignore_index=True)

# CONFIGURACIÓN DE VISUALIZACIÓN
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(df)
