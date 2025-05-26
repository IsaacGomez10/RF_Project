import sys
import os
import pandas as pd
import numpy as np
from faker import Faker
from utils_rf import config_util, utils

faker = Faker('es_ES')

# 1. Obtener ruta de ejecución desde argumento
if len(sys.argv) > 1:
    base_folder = sys.argv[1]
else:
    # En caso de ejecutar sin argumento, puedes decidir qué hacer
    base_folder_config = config_util.cargar_ruta_base()
    base_folder = utils.crear_carpeta_ejecucion(base_folder_config)

# 2. Generar datos falsos
num_registros = 1000
data = {
    'ID_cliente': range(1, num_registros + 1),
    'Edad': np.random.randint(18, 70, size=num_registros),
    'Ingresos_mensuales': np.random.randint(500000, 10000000, size=num_registros),
    'Monto_solicitado': np.random.randint(100000, 5000000, size=num_registros),
    'Historial_credito': np.random.choice(['Bueno', 'Regular', 'Malo'], size=num_registros),
    'Nivel_educativo': np.random.choice(['Secundaria', 'Universidad', 'Postgrado'], size=num_registros),
    'Estado_civil': np.random.choice(['Soltero', 'Casado', 'Divorciado'], size=num_registros),
    'Ocupacion': np.random.choice(['Empleado', 'Independiente', 'Desempleado'], size=num_registros),
    'Ubicacion': np.random.choice(['Bogotá', 'Medellín', 'Cali', 'Barranquilla'], size=num_registros),
    'Score_credito': np.random.randint(300, 850, size=num_registros),
    'Deudas_previas': np.random.randint(0, 10000000, size=num_registros),
    'Cuotas_morosas': np.random.randint(0, 5, size=num_registros),
    'Creditos_anteriores': np.random.randint(0, 10, size=num_registros),
    'Tiene_vivienda_propia': np.random.randint(0, 2, size=num_registros),
    'Tiene_tarjeta_credito': np.random.randint(0, 2, size=num_registros),
    'Aprobado': np.random.randint(0, 2, size=num_registros)
}
df = pd.DataFrame(data)

# 3. Clasificación de riesgo
df['Riesgo'] = np.where(df['Aprobado'] == 1, 'Bajo', 'Alto')
df.loc[(df['Score_credito'] < 500) & (df['Aprobado'] == 0), 'Riesgo'] = 'Medio'

# 4. Guardar CSV sin número consecutivo
nombre_archivo = 'clientes_riesgo.csv'
ruta_archivo = os.path.join(base_folder, nombre_archivo)

try:
    df.to_csv(ruta_archivo, index=False)
    print(f"✅ Archivo generado correctamente: {ruta_archivo}")
except Exception as e:
    print(f"❌ Error al guardar el archivo: {e}")
