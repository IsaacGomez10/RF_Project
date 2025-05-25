import os

_ruta_nueva_carpeta = None  # mejor None para saber si está asignado


def crear_carpeta_ejecucion(base_folder, prefijo='ejecución_'):
    global _ruta_nueva_carpeta

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        print(f"📁 Carpeta base creada: {base_folder}")

    existentes = [d for d in os.listdir(base_folder)
                  if os.path.isdir(os.path.join(base_folder, d)) and d.startswith(prefijo)]

    numeros = []
    for carpeta in existentes:
        try:
            num = int(carpeta.replace(prefijo, ''))
            numeros.append(num)
        except:
            pass

    nuevo_num = max(numeros) + 1 if numeros else 1
    nombre_carpeta = f"{prefijo}{str(nuevo_num).zfill(3)}"
    _ruta_nueva_carpeta = os.path.join(base_folder, nombre_carpeta)
    os.makedirs(_ruta_nueva_carpeta)
    print(f"📁 Carpeta creada para ejecución: {_ruta_nueva_carpeta}")
    return _ruta_nueva_carpeta


def ruta_carpeta_exec():
    global _ruta_nueva_carpeta
    if _ruta_nueva_carpeta is None:
        raise Exception("La carpeta de ejecución no ha sido creada aún. Ejecuta 'crear_carpeta_ejecucion' primero.")
    print(_ruta_nueva_carpeta)
    return _ruta_nueva_carpeta


def obtener_ultimo_archivo(folder, base_name='clientes_riesgo'):
    archivos = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith('.csv')]
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos CSV en la carpeta de datos.")
    archivos.sort(key=lambda x: int(x.split('_')[-1].replace('.csv', '')) if x.split('_')[-1].replace('.csv', '').isdigit() else 0)
    return archivos[-1]
