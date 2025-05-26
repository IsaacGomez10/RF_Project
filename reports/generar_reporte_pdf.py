import os
from fpdf import FPDF
from PIL import Image
from utils_rf import config_util

# Función para formatear títulos
def camel_case(s):
    return ' '.join(word.capitalize() for word in s.replace('.png', '').replace('_', ' ').split())

# Ruta carpeta ejecución
base_folder = config_util.cargar_ruta_base()
prefijo = 'ejecución_'
folders = [f for f in os.listdir(base_folder) if f.startswith(prefijo) and os.path.isdir(os.path.join(base_folder, f))]
numeros = [int(f.replace(prefijo, '')) for f in folders if f.replace(prefijo, '').isdigit()]
if not numeros:
    raise FileNotFoundError("No se encontró carpeta de ejecución.")
carpeta = os.path.join(base_folder, f"{prefijo}{str(max(numeros)).zfill(3)}")

# Inicializar PDF
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Título y descripción general
pdf.set_font("Arial", "B", 20)
pdf.cell(0, 15, "Reporte Financiero de Análisis de Riesgo", ln=True, align='C')

pdf.set_font("Arial", "", 12)
descripcion = (
    "Este reporte contiene las visualizaciones clave para el análisis de riesgos financieros, "
    "incluyendo matrices de correlación, importancia de variables y otras métricas relevantes "
    "para la toma de decisiones."
)
pdf.multi_cell(0, 10, descripcion, align='C')
pdf.ln(10)  # Espacio después del texto

# Obtener imágenes
imagenes = [f for f in os.listdir(carpeta) if f.endswith('.png')]
imagenes.sort()

# Configuración de imagen
max_width = 180  # casi todo el ancho útil (210mm - 2*20mm margen)
x_center = (220 - max_width) / 2

def add_image_full_width(pdf, img_path):
    title = camel_case(os.path.basename(img_path))
    image = Image.open(img_path)
    iw, ih = image.size

    w = max_width
    h = ih * w / iw  # mantener proporción

    # Altura total que ocupará: título (10) + imagen + pequeño margen (5)
    altura_total = 10 + h + 5
    espacio_disponible = pdf.h - pdf.get_y() - pdf.b_margin

    # Si no cabe, agregar nueva página
    if altura_total > espacio_disponible:
        pdf.add_page()

    # Agregar título
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, ln=True, align='C')

    # Agregar imagen
    y = pdf.get_y()
    pdf.image(img_path, x=x_center, y=y, w=w)
    pdf.ln(h + 5)

# Agregar cada imagen en una fila
for img in imagenes:
    add_image_full_width(pdf, os.path.join(carpeta, img))

# Guardar PDF
reporte_path = os.path.join(carpeta, 'reporte_analisis_financiero.pdf')
pdf.output(reporte_path)
print(f"✅ PDF generado en: {reporte_path}")

# Abrir automáticamente (solo Windows)
os.startfile(reporte_path)
