import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from utils_rf import config_util
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar ruta base y carpeta ejecución (reutiliza tu código)
base_folder_config = config_util.cargar_ruta_base()
prefijo = 'ejecución_'
existentes = [d for d in os.listdir(base_folder_config) if os.path.isdir(os.path.join(base_folder_config, d)) and d.startswith(prefijo)]
numeros = [int(d.replace(prefijo, '')) for d in existentes if d.replace(prefijo, '').isdigit()]
if numeros:
    ejec_numero = max(numeros)
    carpeta_ejecucion = os.path.join(base_folder_config, f"{prefijo}{str(ejec_numero).zfill(3)}")
else:
    raise FileNotFoundError("No se encontró carpeta de ejecución.")

# Cargar datos clasificados
archivo_clasificado = os.path.join(carpeta_ejecucion, 'clientes_riesgo_clasificado.csv')
df = pd.read_csv(archivo_clasificado)

# Asumimos que hay columnas 'Riesgo' y 'Prediccion_Riesgo'
y_true = df['Riesgo']
y_pred = df['Prediccion_Riesgo']

# Métricas
acc = accuracy_score(y_true, y_pred)
report = classification_report(y_true, y_pred, output_dict=True)
cm = confusion_matrix(y_true, y_pred)

# Guardar matriz de confusión
df_cm = pd.DataFrame(cm, index=[f'Actual_{c}' for c in sorted(y_true.unique())],
                     columns=[f'Pred_{c}' for c in sorted(y_true.unique())])
df_cm.to_csv(os.path.join(carpeta_ejecucion, 'matriz_confusion.csv'))

# Guardar reporte clasificación
df_report = pd.DataFrame(report).transpose()
df_report.to_csv(os.path.join(carpeta_ejecucion, 'reporte_clasificacion.csv'))

# Guardar métrica accuracy en txt
with open(os.path.join(carpeta_ejecucion, 'accuracy.txt'), 'w') as f:
    f.write(f"Accuracy: {acc:.4f}\n")

print("✅ Reporte desempeño modelo guardado.")

# Matriz de confusión visual
plt.figure(figsize=(6, 4))
sns.heatmap(df_cm, annot=True, cmap='Blues', fmt='d')
plt.title('Matriz de Confusión')
plt.ylabel('Actual')
plt.xlabel('Predicción')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_ejecucion, 'matriz_confusion.png'))
plt.close()