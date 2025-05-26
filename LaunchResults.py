import subprocess
import os
from utils_rf import config_util, utils
import sys


base_folder_config = config_util.cargar_ruta_base()
ruta_ejecucion = utils.crear_carpeta_ejecucion(base_folder_config)

SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')

scripts = [
    "generar_data.py",
    "exploracion_data.py",
    "limpiar_data.py",
    "correlacion_data.py",
    "prediccion_calificacion_aut.py",
    "integracion_pwbi.py",
    "reporte_cambios_ejecuciones.py",
    "reporte_variables_importantes.py",
    "reportes_aprobacion_rechazos.py",
    "reportes_desempenio_modelo.py",
    "reportes_outliers.py"
]

for script in scripts:
    script_path = os.path.join(SRC_DIR, script)
    print(f"\n🚀 Ejecutando: {script_path}")
    result = subprocess.run(
        ["python", script_path, ruta_ejecucion],  # pasamos la ruta como argumento
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    print(result.stdout)
    if result.stderr:
        print("❌ Error:")
        print(result.stderr)

# Ejecutar script para generar el PDF (esperar que termine)
pdf_script = os.path.join(REPORTS_DIR, "generar_reporte_pdf.py")
print(f"\n🚀 Ejecutando generación de PDF: {pdf_script}")
result = subprocess.run(
    ["python", pdf_script],
    capture_output=True,
    text=True,
    encoding='utf-8'
)
print(result.stdout)
if result.stderr:
    print("❌ Error en PDF:")
    print(result.stderr)

# Lanzar Streamlit (queda corriendo)
streamlit_script = os.path.join(REPORTS_DIR, "dashboard_analisis.py")
print(f"\n🚀 Lanzando Streamlit para dashboard: {streamlit_script}")
if not os.path.exists(streamlit_script):
    print(f"❌ No se encontró el archivo: {streamlit_script}")
    sys.exit(1)

try:
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", streamlit_script],
        cwd=REPORTS_DIR,
        stdout=subprocess.DEVNULL,  # silencia si quieres
        stderr=subprocess.DEVNULL
    )
    print("\n✅ Todos los scripts ejecutados. Streamlit dashboard está corriendo.")
except Exception as e:
    print(f"❌ Error al lanzar Streamlit: {e}")
    sys.exit(1)
