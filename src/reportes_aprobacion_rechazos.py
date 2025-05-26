import os
import pandas as pd
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

# Agrupar por 'Aprobado' y 'Riesgo'
aprob_rechazo = df.groupby
