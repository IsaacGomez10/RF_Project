import os
import pandas as pd
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

# 3. Cargar archivo clasificado (resultado de paso 4)
archivo_clasificado = os.path.join(carpeta_ejecucion, 'clientes_riesgo_clasificado.csv')
if not os.path.exists(archivo_clasificado):
    raise FileNotFoundError(f"No se encontró el archivo clasificado: {archivo_clasificado}")

df = pd.read_csv(archivo_clasificado)

# 4. Generar resumen para Power BI

# Resumen distribución por nivel de riesgo
resumen_riesgo = df['Prediccion_Riesgo'].value_counts().reset_index()
resumen_riesgo.columns = ['Nivel_Riesgo', 'Cantidad_Clientes']
resumen_riesgo['Porcentaje'] = (resumen_riesgo['Cantidad_Clientes'] / resumen_riesgo['Cantidad_Clientes'].sum()) * 100

print("📊 Distribución de clientes por nivel de riesgo:")
print(resumen_riesgo)

# Guardar resumen en CSV (opcional para Power BI)
archivo_resumen = os.path.join(carpeta_ejecucion, 'resumen_riesgo.csv')
resumen_riesgo.to_csv(archivo_resumen, index=False)
print(f"✅ Resumen de riesgo guardado en: {archivo_resumen}")

# 5. Otras tablas para análisis por zona, ingresos, estado civil...

# Por ejemplo, distribución de riesgo por zona
if 'Zona' in df.columns:
    resumen_zona = df.groupby(['Zona', 'Prediccion_Riesgo']).size().unstack(fill_value=0)
    resumen_zona.to_csv(os.path.join(carpeta_ejecucion, 'resumen_riesgo_por_zona.csv'))
    print("✅ Resumen de riesgo por zona guardado")

# Por ejemplo, promedio de ingresos por nivel de riesgo
if 'Ingresos' in df.columns:
    ingresos_riesgo = df.groupby('Prediccion_Riesgo')['Ingresos'].mean().reset_index()
    ingresos_riesgo.to_csv(os.path.join(carpeta_ejecucion, 'promedio_ingresos_por_riesgo.csv'))
    print("✅ Promedio de ingresos por riesgo guardado")

# 6. Indicadores clave

total_clientes = len(df)
print(f"Total clientes: {total_clientes}")

# Puede preparar un CSV con indicadores generales
indicadores = {
    'Total_Clientes': [total_clientes],
    'Clientes_Alto_Riesgo': [resumen_riesgo.loc[resumen_riesgo['Nivel_Riesgo'] == 'Alto', 'Cantidad_Clientes'].sum() if 'Alto' in resumen_riesgo['Nivel_Riesgo'].values else 0],
    'Clientes_Medio_Riesgo': [resumen_riesgo.loc[resumen_riesgo['Nivel_Riesgo'] == 'Medio', 'Cantidad_Clientes'].sum() if 'Medio' in resumen_riesgo['Nivel_Riesgo'].values else 0],
    'Clientes_Bajo_Riesgo': [resumen_riesgo.loc[resumen_riesgo['Nivel_Riesgo'] == 'Bajo', 'Cantidad_Clientes'].sum() if 'Bajo' in resumen_riesgo['Nivel_Riesgo'].values else 0],
}

df_indicadores = pd.DataFrame(indicadores)
archivo_indicadores = os.path.join(carpeta_ejecucion, 'indicadores_clave.csv')
df_indicadores.to_csv(archivo_indicadores, index=False)
print(f"✅ Indicadores clave guardados en: {archivo_indicadores}")

