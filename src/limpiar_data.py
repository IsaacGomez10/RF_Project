import os
import pandas as pd
import numpy as np
from utils_rf import config_util

# 1. Cargar ruta base desde config
base_folder_config = config_util.cargar_ruta_base()

# 2. Identificar carpeta de ejecución más reciente
prefijo = 'ejecución_'
existentes = [d for d in os.listdir(base_folder_config)
              if os.path.isdir(os.path.join(base_folder_config, d)) and d.startswith(prefijo)]
numeros = []
for carpeta in existentes:
    try:
        num = int(carpeta.replace(prefijo, ''))
        numeros.append(num)
    except:
        pass

if numeros:
    ejec_numero = max(numeros)
    carpeta_ejecucion = os.path.join(base_folder_config, f"{prefijo}{str(ejec_numero).zfill(3)}")
else:
    raise FileNotFoundError("No se encontró carpeta de ejecución.")

# 3. Cargar archivo clientes_riesgo.csv
archivo = os.path.join(carpeta_ejecucion, 'clientes_riesgo.csv')
if not os.path.exists(archivo):
    raise FileNotFoundError(f"No se encontró el archivo: {archivo}")

df = pd.read_csv(archivo)

print("📋 Resumen antes de limpieza:")
print(df.info())

# 4. Limpiar datos

# 4.1 Eliminar filas duplicadas si existen
num_antes = len(df)
df = df.drop_duplicates()
num_despues = len(df)
print(f"🔄 Filas duplicadas eliminadas: {num_antes - num_despues}")

# 4.2 Tratar valores nulos (si hay)
nulos_por_col = df.isnull().sum()
print("❗ Valores nulos por columna:")
print(nulos_por_col)

# Por ejemplo, si hay nulos, rellenamos con la media (numéricos) o moda (categóricos)
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype in [np.float64, np.int64]:
            media = df[col].mean()
            df[col].fillna(media, inplace=True)
            print(f"🔧 Nulos en {col} rellenados con media: {media:.2f}")
        else:
            moda = df[col].mode()[0]
            df[col].fillna(moda, inplace=True)
            print(f"🔧 Nulos en {col} rellenados con moda: {moda}")

# 4.3 Convertir tipos de datos si es necesario (por ejemplo, variables binarias 0/1 a booleanos)
binarias = ['Tiene_vivienda_propia', 'Tiene_tarjeta_credito', 'Aprobado']
for col in binarias:
    if col in df.columns:
        df[col] = df[col].astype(bool)
        print(f"✅ Columna {col} convertida a tipo booleano")

# 4.4 Eliminar columnas irrelevantes o con muchas nulas (si hay alguna)
# Por ahora no tenemos, pero aquí es donde iría la lógica

# 4.5 Resetear índice tras limpieza
df.reset_index(drop=True, inplace=True)

print("\n📋 Resumen después de limpieza:")
print(df.info())

# Guardar el archivo limpio para futuros pasos
archivo_limpio = os.path.join(carpeta_ejecucion, 'clientes_riesgo_limpio.csv')
df.to_csv(archivo_limpio, index=False)
print(f"✅ Archivo limpio guardado en: {archivo_limpio}")
