import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils_rf import config_util
import matplotlib.ticker as mtick

plt.ion()  # activar modo interactivo

# 1. Cargar ruta base desde config
base_folder_config = config_util.cargar_ruta_base()

# 2. Identificar carpeta de ejecución más reciente
prefijo = 'ejecución_'
existentes = [
    d for d in os.listdir(base_folder_config)
    if os.path.isdir(os.path.join(base_folder_config, d)) and d.startswith(prefijo)
]

numeros = []
for carpeta in existentes:
    try:
        num = int(carpeta.replace(prefijo, ''))
        numeros.append(num)
    except ValueError:
        pass  # Ignorar carpetas que no cumplen el formato esperado

if not numeros:
    raise FileNotFoundError("No se encontró carpeta de ejecución.")

ejec_numero = max(numeros)
carpeta_ejecucion = os.path.join(base_folder_config, f"{prefijo}{str(ejec_numero).zfill(3)}")

# 3. Cargar archivo clientes_riesgo.csv
archivo = os.path.join(carpeta_ejecucion, 'clientes_riesgo.csv')
if not os.path.exists(archivo):
    raise FileNotFoundError(f"No se encontró el archivo: {archivo}")

df = pd.read_csv(archivo)

# --- Información básica del DataFrame ---
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

# Variables numéricas y categóricas
num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# --- Histogramas variables numéricas ---
print("\n📊 Histogramas de variables numéricas:")
plt.figure(figsize=(15, 10))
for i, col in enumerate(num_cols):
    plt.subplot(4, 4, i + 1)
    sns.histplot(df[col], bins=30, kde=True, color='skyblue')
    plt.title(col)
    plt.tight_layout()
    plt.show()
    plt.close()

# --- Boxplots variables numéricas ---
print("\n📊 Boxplots para variables numéricas:")
plt.figure(figsize=(15, 10))
for i, col in enumerate(num_cols):
    plt.subplot(4, 4, i + 1)
    sns.boxplot(x=df[col], color='salmon')
    plt.title(col)
    plt.tight_layout()
    plt.show()
    plt.close()

# --- Conteo y barras para variables categóricas ---
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
    plt.close()

# --- Matriz de correlación (numéricas) ---
print("\n📈 Matriz de correlación entre variables numéricas:")
corr = df[num_cols].corr()
print(corr)

plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title("Mapa de calor - Correlación variables numéricas")
plt.tight_layout()
plt.show()
plt.close()
plt.ioff()

# --- Guardar gráficos ---
def guardar_figura(fig, filename):
    path = os.path.join(carpeta_ejecucion, filename)
    fig.savefig(path)
    plt.close(fig)

# --- Análisis cruzado: Riesgo vs categóricas ---
# Guardar histogramas
for col in num_cols:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df[col], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title(col)
    fig.tight_layout()
    guardar_figura(fig, f'histograma_{col}.png')

# Guardar boxplots numéricas
for col in num_cols:
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.boxplot(x=df[col], color='salmon', ax=ax)
    ax.set_title(col)
    fig.tight_layout()
    guardar_figura(fig, f'boxplot_{col}.png')

# Guardar conteo categorías
for col in cat_cols:
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index, palette='pastel', ax=ax)
    ax.set_title(f'Distribución de {col}')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    fig.tight_layout()
    guardar_figura(fig, f'conteo_{col}.png')

# Guardar heatmap correlación
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, ax=ax)
ax.set_title("Mapa de calor - Correlación variables numéricas")
fig.tight_layout()
guardar_figura(fig, 'correlacion_heatmap.png')

# Guardar boxplots numéricas vs Riesgo
for col in num_cols:
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.boxplot(x='Riesgo', y=col, data=df, palette='Set2', ax=ax)
    ax.set_title(f"{col} por Riesgo")
    fig.tight_layout()
    guardar_figura(fig, f'boxplot_{col}_riesgo.png')

# Guardar análisis cruzado Riesgo vs categorías
for col in cat_cols:
    ct = pd.crosstab(df[col], df['Riesgo'], normalize='index').mul(100).round(2)
    plot = ct.plot(kind='bar', stacked=True, colormap='viridis', figsize=(7, 4))
    plot.set_title(f"Distribución Riesgo según {col}")
    plot.set_ylabel('Porcentaje')
    plot.legend(title='Riesgo')
    fig = plot.get_figure()
    fig.tight_layout()
    guardar_figura(fig, f'analisis_riesgo_{col}.png')