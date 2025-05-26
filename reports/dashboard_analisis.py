import streamlit as st
import pandas as pd
import os
from utils_rf import config_util
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

# --- Cargar última carpeta de ejecución ---
base_folder = config_util.cargar_ruta_base()
prefijo = "ejecución_"
carpetas = [d for d in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, d)) and d.startswith(prefijo)]

if not carpetas:
    st.error("No se encontraron carpetas de ejecución.")
    st.stop()

ult_ejecucion = max(carpetas, key=lambda x: int(x.replace(prefijo, '')))
ruta_datos = os.path.join(base_folder, ult_ejecucion, "clientes_riesgo_limpio.csv")

if not os.path.exists(ruta_datos):
    st.error("No se encontró el archivo limpio de datos.")
    st.stop()

# --- Cargar DataFrame ---
df = pd.read_csv(ruta_datos)
st.title("📊 Dashboard de Análisis de Riesgo Crediticio")

# --- Sidebar: filtros dinámicos ---
st.sidebar.header("🔍 Filtros")

# 1. Filtro por columnas categóricas
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
for col in cat_cols:
    opciones = df[col].dropna().unique().tolist()
    seleccion = st.sidebar.multiselect(f"{col}", opciones, default=opciones)
    df = df[df[col].isin(seleccion)]

# 2. Filtros por columnas numéricas (rangos)
num_cols = df.select_dtypes(include=np.number).columns.tolist()
for col in num_cols:
    min_val = float(df[col].min())
    max_val = float(df[col].max())
    rango = st.sidebar.slider(f"{col}", min_val, max_val, (min_val, max_val))
    df = df[df[col].between(rango[0], rango[1])]

# 3. Filtro por búsqueda de texto (solo para columnas de texto)
text_cols = df.select_dtypes(include='object').columns.tolist()
for col in text_cols:
    texto = st.sidebar.text_input(f"Buscar en {col} (contiene)", "")
    if texto:
        df = df[df[col].str.contains(texto, case=False, na=False)]

# --- Mostrar tabla filtrada ---
st.subheader("📄 Tabla de datos filtrados")
st.dataframe(df, use_container_width=True)

# --- Estadísticas descriptivas ---
with st.expander("📈 Estadísticas descriptivas (numéricas)", expanded=False):
    st.dataframe(df.describe().transpose())

# --- Visualización: Distribución de variable objetivo ---
if 'Riesgo' in df.columns:
    st.subheader("🎯 Distribución de Riesgo")
    fig_riesgo = px.histogram(df, x='Riesgo', color='Riesgo')
    st.plotly_chart(fig_riesgo, use_container_width=True)

# --- Visualización: Boxplots por variable numérica ---
st.subheader("📦 Boxplots por variable numérica")
num_col_selec = st.multiselect("Selecciona variables numéricas para visualizar", num_cols)
if num_col_selec:
    for col in num_col_selec:
        fig = px.box(df, y=col, color='Riesgo' if 'Riesgo' in df.columns else None, points="all")
        st.plotly_chart(fig, use_container_width=True)

# --- Visualización: Histogramas ---
st.subheader("📊 Histogramas")
hist_cols = st.multiselect("Selecciona columnas para histogramas", num_cols, default=num_cols[:3])
for col in hist_cols:
    fig = px.histogram(df, x=col, nbins=30)
    st.plotly_chart(fig, use_container_width=True)

# --- Descargar datos filtrados ---
@st.cache_data
def convertir_csv(data):
    return data.to_csv(index=False).encode('utf-8')

csv_data = convertir_csv(df)
st.download_button("📥 Descargar datos filtrados (CSV)", data=csv_data, file_name='clientes_filtrados.csv', mime='text/csv')
