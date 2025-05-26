import configparser
import os

def cargar_ruta_base():
    config = configparser.ConfigParser()
    ruta = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    ruta = os.path.abspath(ruta)

    config.read(ruta, encoding='utf-8')

    if 'PATHS' not in config or 'base_folder' not in config['PATHS']:
        raise ValueError("⚠️ No se encontró la sección PATHS o la clave base_folder en el archivo config.ini")

    return config['PATHS']['base_folder']