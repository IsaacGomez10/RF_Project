import subprocess
import os
from utils_rf import config_util, utils


base_folder_config = config_util.cargar_ruta_base()
ruta_ejecucion = utils.crear_carpeta_ejecucion(base_folder_config)

SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')

scripts = [
    "generar_data.py",
    "exploracion_data.py",
    "limpiar_data.py",
    "correlacion_data.py",
    "prediccion_calificacion_aut.py",
    "integracion_pwbi.py"
]

for script in scripts:
    script_path = os.path.join(SRC_DIR, script)
    print(f"\n🚀 Ejecutando: {script_path}")
    result = subprocess.run(
        ["python", script_path, ruta_ejecucion],  # <-- pasamos la ruta como argumento
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    print(result.stdout)
    if result.stderr:
        print("❌ Error:")
        print(result.stderr)
