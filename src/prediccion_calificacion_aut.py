import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
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

# 3. Cargar archivo limpio
archivo_limpio = os.path.join(carpeta_ejecucion, 'clientes_riesgo_limpio.csv')
if not os.path.exists(archivo_limpio):
    raise FileNotFoundError(f"No se encontró el archivo limpio: {archivo_limpio}")

df = pd.read_csv(archivo_limpio)

# 4. Preparar variables predictoras (X) y objetivo (y)
# Excluimos columnas no predictoras o target
columnas_no_uso = ['ID_cliente', 'Riesgo', 'Aprobado']
X = df.drop(columns=columnas_no_uso)

# Algunas variables categóricas las convertimos a dummies (one-hot)
X = pd.get_dummies(X, drop_first=True)

y = df['Riesgo']  # Nuestro target

# 5. Dividir datos en train/test para evaluar el modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 6. Entrenar modelo RandomForest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 7. Predecir y evaluar
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"📊 Precisión del modelo: {acc:.4f}")
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

# 8. Aplicar modelo a todo el dataset para agregar predicciones y probabilidades
df['Prediccion_Riesgo'] = model.predict(X)
probs = model.predict_proba(X)
# Añadir columna con probabilidad máxima de la clase predicha
df['Probabilidad_Riesgo'] = probs.max(axis=1)

# 9. Guardar archivo con predicción y probabilidad
archivo_resultado = os.path.join(carpeta_ejecucion, 'clientes_riesgo_clasificado.csv')
df.to_csv(archivo_resultado, index=False)
print(f"✅ Archivo con clasificación guardado en: {archivo_resultado}")
