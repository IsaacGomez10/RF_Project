import os
import pandas as pd
import numpy as np
from utils_rf import config_util

base_folder_config = config_util.cargar_ruta_base()
prefijo = 'ejecución_'
existentes = [d for d in os.listdir(base_folder_config) if os.path.isdir(os.path.join(base_folder_config, d)) and d.startswith(prefijo)]
numeros = [int(d.replace(prefijo, '')) for d in existentes if d.replace(prefijo, '').isdigit()]
if not numeros:
    raise FileNotFoundError("No se encontró carpeta de ejecución.")

ejec_numero = max(numeros)
carpeta_ejecucion = os.path.join(base_folder_config, f"{prefijo}{str(ejec_numero).zfill(3)}")

archivo_limpio = os.path.join(carpeta_ejecucion, 'clientes_riesgo_limpio.csv')
df = pd.read_csv(archivo_limpio)

if 'ID_cliente' not in df.columns:
    raise KeyError("La columna 'ID_cliente' no existe en el archivo CSV.")

if df['ID_cliente'].isnull().any():
    raise ValueError("Existen valores nulos en la columna 'ID_cliente', lo que puede causar problemas en la identificación de outliers.")

num_cols = df.select_dtypes(include=np.number).columns.tolist()

outliers_list = []

for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    outlier_mask = (df[col] < limite_inferior) | (df[col] > limite_superior)
    outliers_col = df.loc[outlier_mask, ['ID_cliente', col]].copy()

    if not outliers_col.empty:
        outliers_col['Variable'] = col
        # Aquí aseguramos que 'Valor' es el valor numérico correcto
        outliers_col['Valor'] = outliers_col[col]
        outliers_col = outliers_col.reset_index(drop=True)
        outliers_col = outliers_col[['ID_cliente', 'Variable', 'Valor']]
        outliers_list.append(outliers_col)
        print(f"Se encontraron {len(outliers_col)} outliers en la columna '{col}'.")

if outliers_list:
    outliers = pd.concat(outliers_list, ignore_index=True)
    outliers.to_csv(os.path.join(carpeta_ejecucion, 'outliers.csv'), index=False)
    print(f"✅ Reporte de outliers guardado. Total filas: {len(outliers)}")
else:
    print("⚠️ No se detectaron outliers en las columnas numéricas.")
