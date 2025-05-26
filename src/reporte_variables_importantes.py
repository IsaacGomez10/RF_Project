import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from utils_rf import config_util
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar ruta base y carpeta ejecución
base_folder_config = config_util.cargar_ruta_base()
prefijo = 'ejecución_'
existentes = [d for d in os.listdir(base_folder_config) if os.path.isdir(os.path.join(base_folder_config, d)) and d.startswith(prefijo)]
numeros = [int(d.replace(prefijo, '')) for d in existentes if d.replace(prefijo, '').isdigit()]
if not numeros:
    raise FileNotFoundError("No se encontró carpeta de ejecución.")

ejec_numero = max(numeros)
carpeta_ejecucion = os.path.join(base_folder_config, f"{prefijo}{str(ejec_numero).zfill(3)}")

# Cargar dataset limpio
archivo_limpio = os.path.join(carpeta_ejecucion, 'clientes_riesgo_limpio.csv')
df = pd.read_csv(archivo_limpio)

# Definir variables predictoras y target
columnas_no_uso = ['ID_cliente', 'Riesgo', 'Aprobado']
X = df.drop(columns=columnas_no_uso)
X = pd.get_dummies(X, drop_first=True)
y = df['Riesgo']

# Entrenar modelo RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Guardar modelo
modelo_path = os.path.join(carpeta_ejecucion, 'modelo_rf.pkl')
joblib.dump(model, modelo_path)

print(f"✅ Modelo RandomForest entrenado y guardado en: {modelo_path}")

# Importancias
importancia = pd.DataFrame({
    'Variable': X.columns,
    'Importancia': model.feature_importances_
}).sort_values(by='Importancia', ascending=False)

importancia.to_csv(os.path.join(carpeta_ejecucion, 'importancia_variables.csv'), index=False)

# Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(data=importancia.head(20), y='Variable', x='Importancia', hue='Variable', palette='viridis', legend=False)
plt.title('Importancia de Variables - Top 20')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_ejecucion, 'importancia_variables.png'))
plt.close()