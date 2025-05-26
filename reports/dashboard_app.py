import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Ruta fija a la carpeta de ejecución actual
ruta = "C:\\temporal\\.PJ_RF_DOCUMENTS\\ejecución_006"
nombre_ejecucion = os.path.basename(ruta)

# Cargar archivos
def cargar_csv(nombre):
    path = os.path.join(ruta, nombre)
    return pd.read_csv(path) if os.path.exists(path) else None

st.title("📊 Dashboard de Riesgo Financiero")

# Cargar datasets
clientes = cargar_csv("clientes_riesgo_clasificado.csv")
limpio = cargar_csv("clientes_riesgo_limpio.csv")
outliers = cargar_csv("outliers.csv")
resumen = cargar_csv("resumen_riesgo.csv")
indicadores = cargar_csv("indicadores_clave.csv")
matriz = cargar_csv("matriz_confusion.csv")
reporte_clasificacion = cargar_csv("reporte_clasificacion.csv")
cambios = cargar_csv("cambios_prediccion.csv")

# Filtros
if clientes is not None:
    st.sidebar.header("🔎 Filtros de Clientes")
    riesgo = st.sidebar.multiselect("Riesgo:", clientes["Riesgo"].unique(), default=clientes["Riesgo"].unique())
    aprobado = st.sidebar.multiselect("Aprobado:", clientes["Aprobado"].unique(), default=clientes["Aprobado"].unique())
    clientes_filtrado = clientes[clientes["Riesgo"].isin(riesgo) & clientes["Aprobado"].isin(aprobado)]

    st.subheader("📄 Clientes Clasificados")
    st.dataframe(clientes_filtrado)

    st.subheader("📊 Distribución por Riesgo")
    fig = px.histogram(clientes_filtrado, x="Riesgo", color="Aprobado", barmode="group")
    st.plotly_chart(fig)

if resumen is not None:
    st.subheader("📊 Resumen de Riesgo")
    st.dataframe(resumen)

if indicadores is not None:
    st.subheader("📌 Indicadores Clave")
    st.dataframe(indicadores)

if matriz is not None:
    st.subheader("📊 Matriz de Confusión")
    st.dataframe(matriz)

if outliers is not None:
    st.subheader("🚨 Outliers Detectados")
    variable = st.selectbox("Filtrar por Variable:", outliers["Variable"].unique())
    st.dataframe(outliers[outliers["Variable"] == variable])

if reporte_clasificacion is not None:
    st.subheader("📑 Reporte de Clasificación")
    st.dataframe(reporte_clasificacion)

if cambios is not None:
    st.subheader("🔄 Cambios en Predicción")
    st.dataframe(cambios)

st.markdown("---")
st.caption(f"📂 Fuente: {nombre_ejecucion}")
