import os
import pandas as pd
from utils_rf import config_util

base_folder_config = config_util.cargar_ruta_base()
prefijo = 'ejecución_'
existentes = [d for d in os.listdir(base_folder_config) if os.path.isdir(os.path.join(base_folder_config, d)) and d.startswith(prefijo)]
numeros = sorted([int(d.replace(prefijo, '')) for d in existentes if d.replace(prefijo, '').isdigit()])

if len(numeros) < 2:
    raise ValueError("Se necesitan al menos 2 ejecuciones para comparar.")

ultima = numeros[-1]
anterior = numeros[-2]

carpeta_ultima = os.path.join(base_folder_config, f"{prefijo}{str(ultima).zfill(3)}")
carpeta_anterior = os.path.join(base_folder_config, f"{prefijo}{str(anterior).zfill(3)}")

file_ultima = os.path.join(carpeta_ultima, 'clientes_riesgo_clasificado.csv')
file_anterior = os.path.join(carpeta_anterior, 'clientes_riesgo_clasificado.csv')

df_ultima = pd.read_csv(file_ultima)
df_anterior = pd.read_csv(file_anterior)

# Asumimos que tienen columna ID_cliente y Prediccion_Riesgo
df_merge = pd.merge(df_anterior[['ID_cliente', 'Prediccion_Riesgo']],
                    df_ultima[['ID_cliente', 'Prediccion_Riesgo']],
                    on='ID_cliente', suffixes=('_anterior', '_actual'))

# Detectar cambios en la predicción
df_merge['Cambio_Prediccion'] = df_merge['Prediccion_Riesgo_anterior'] != df_merge['Prediccion_Riesgo_actual']

df_cambios = df_merge[df_merge['Cambio_Prediccion']]

df_cambios.to_csv(os.path.join(carpeta_ultima, 'cambios_prediccion.csv'), index=False)

print("✅ Reporte de cambios entre ejecuciones guardado.")
