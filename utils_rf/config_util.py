import configparser
import os

def cargar_ruta_base(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)

    if 'PATHS' not in config or 'base_folder' not in config['PATHS']:
        raise ValueError("⚠️ No se encontró la sección PATHS o la clave base_folder en el archivo config.ini")

    base_folder = config.get('PATHS', 'base_folder')
    return base_folder.rstrip('\\/')
