import os
import glob
import shutil
from datetime import datetime

def obtener_ultimo_csv(ruta):
    """
    Obtiene el archivo CSV más reciente en la ruta especificada
    """
    # Obtener todos los archivos CSV en la ruta
    patron = os.path.join(ruta, "*.csv")
    archivos_csv = glob.glob(patron)
    
    if not archivos_csv:
        raise FileNotFoundError("No se encontraron archivos CSV en la ruta especificada")
    
    # Obtener el archivo más reciente por fecha de modificación
    ultimo_archivo = max(archivos_csv, key=os.path.getmtime)
    return ultimo_archivo

def generar_nuevo_nombre():
    """
    Genera un nuevo nombre de archivo con la fecha actual en formato DDMMYY
    """
    fecha_actual = datetime.now()
    nuevo_nombre = fecha_actual.strftime("%d%m%y") + ".csv"
    return nuevo_nombre

def mover_y_renombrar_archivo(origen, destino):
    """
    Mueve un archivo a la carpeta de destino y lo renombra con la fecha actual
    """
    try:
        # Generar el nuevo nombre con la fecha
        nuevo_nombre = generar_nuevo_nombre()
        
        # Construir la ruta de destino completa con el nuevo nombre
        ruta_destino = os.path.join(destino, nuevo_nombre)
        
        # Mover el archivo con el nuevo nombre
        shutil.move(origen, ruta_destino)
        print(f"Archivo movido y renombrado exitosamente a: {ruta_destino}")
        
    except Exception as e:
        print(f"Error al mover y renombrar el archivo: {str(e)}")

def main():
    # Ruta donde están los archivos descargados
    ruta_origen = r"/home/mankolepantos/downloaded_files"
    
    # Aquí puedes especificar la ruta de destino donde quieres mover el archivo
    ruta_destino = r'/home/mankolepantos/Smol_Holders_Daily/Smol_Holders_Daily/smol_ko/data'
    
    try:
        # Obtener el último archivo CSV
        ultimo_archivo = obtener_ultimo_csv(ruta_origen)
        
        # Mover y renombrar el archivo
        mover_y_renombrar_archivo(ultimo_archivo, ruta_destino)
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()