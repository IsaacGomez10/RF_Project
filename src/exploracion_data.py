import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

print("\n📊 Información general del DataFrame:")
print(df.info())

print("\n📈 Estadísticas descriptivas numéricas:")
print(df.describe())

print("\n📈 Estadísticas descriptivas categóricas:")
print(df.describe(include=['object', 'category']))

print("\n🧮 Conteo de valores nulos por columna:")
print(df.isnull().sum())

print("\n🎯 Distribución de la variable objetivo 'Riesgo':")
print(df['Riesgo'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

print("\n📊 Primeras filas del DataFrame:")
print(df.head())

# Distribución variables numéricas - histogramas
num_cols = df.select_dtypes(include=np.number).columns.tolist()

print("\n📊 Histogramas de variables numéricas:")
import matplotlib.ticker as mtick

plt.figure(figsize=(15, 10))
for i, col in enumerate(num_cols):
    plt.subplot(4, 4, i+1)
    sns.histplot(df[col], bins=30, kde=True, color='skyblue')
    plt.title(col)
    plt.tight_layout()
plt.show()

# Boxplots para detectar outliers
print("\n📊 Boxplots para variables numéricas:")
plt.figure(figsize=(15, 10))
for i, col in enumerate(num_cols):
    plt.subplot(4, 4, i+1)
    sns.boxplot(x=df[col], color='salmon')
    plt.title(col)
    plt.tight_layout()
plt.show()

# Variables categóricas - conteo y barras
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

print("\n📊 Conteo de categorías por variable categórica:")
for col in cat_cols:
    print(f"\n-- {col} --")
    print(df[col].value_counts())
    plt.figure(figsize=(6, 3))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index, palette='pastel')
    plt.title(f'Distribución de {col}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Correlaciones (solo numéricas)
print("\n📈 Matriz de correlación entre variables numéricas:")
corr = df[num_cols].corr()
print(corr)

plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title("Mapa de calor - Correlación variables numéricas")
plt.show()

# Análisis cruzado entre Riesgo y variables categóricas
print("\n📊 Distribución de Riesgo por variables categóricas:")
for col in cat_cols:
    ct = pd.crosstab(df[col], df['Riesgo'], normalize='index').mul(100).round(2)
    print(f"\n-- Riesgo vs {col} --")
    print(ct)
    ct.plot(kind='bar', stacked=True, figsize=(7, 4), colormap='viridis')
    plt.title(f"Distribución Riesgo según {col}")
    plt.ylabel('Porcentaje')
    plt.legend(title='Riesgo')
    plt.tight_layout()
    plt.show()

# Análisis cruzado con variables numéricas vs Riesgo - boxplots
print("\n📊 Boxplots de variables numéricas según Riesgo:")
for col in num_cols:
    plt.figure(figsize=(6, 3))
    sns.boxplot(x='Riesgo', y=col, data=df, palette='Set2')
    plt.title(f"{col} por Riesgo")
    plt.tight_layout()
    plt.show()

print("\n✅ Exploración de datos finalizada.")
