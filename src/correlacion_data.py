import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# 3. Cargar archivo limpio para análisis
archivo_limpio = os.path.join(carpeta_ejecucion, 'clientes_riesgo_limpio.csv')
if not os.path.exists(archivo_limpio):
    raise FileNotFoundError(f"No se encontró el archivo limpio: {archivo_limpio}")

df = pd.read_csv(archivo_limpio)

# 4. Matriz de correlación solo numéricos
corr = df.select_dtypes(include=[np.number]).corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Matriz de correlación de variables numéricas')
plt.tight_layout()
plt.show()

# 5. Estadísticas descriptivas detalladas para variables numéricas
print("\n📊 Estadísticas descriptivas de variables numéricas:")
print(df.select_dtypes(include=[np.number]).describe())

# 6. Boxplots para detectar outliers en variables numéricas
num_cols = df.select_dtypes(include=[np.number]).columns

for col in num_cols:
    plt.figure(figsize=(6, 3))
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot de {col}')
    plt.show()

# 7. Opcional: detectar outliers con IQR y mostrar cantidad por variable
print("\n🔎 Detección básica de outliers (IQR):")
for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
    print(f"{col}: {len(outliers)} outliers detectados")