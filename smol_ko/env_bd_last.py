import os
from dotenv import load_dotenv
import pymysql
import pandas as pd
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de la base de datos desde las variables de entorno
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Función para procesar un archivo CSV e insertarlo en la base de datos
def procesar_csv_archivo(ruta_csv, fecha):
    # Leer el CSV
    df = pd.read_csv(ruta_csv)
    
    # Eliminar espacios extra en las columnas (por si hay algún espacio innecesario)
    df.columns = df.columns.str.strip()
    
    # Reemplazar comas en los balances para poder convertirlos a números
    df['Balance'] = df['Balance'].str.replace(',', '').astype(float)
    
    # Crear una lista de tuplas con los datos a insertar
    data_to_insert = [(fecha, row['HolderAddress'], row['Balance']) for _, row in df.iterrows()]
    
    return data_to_insert

# Función para insertar el último archivo CSV de la carpeta
def insertar_ultimo_csv(carpeta_csv, conn):
    # Obtener todos los archivos CSV en la carpeta
    archivos_csv = [archivo for archivo in os.listdir(carpeta_csv) if archivo.endswith('.csv')]
    
    if not archivos_csv:
        print('No hay archivos CSV en la carpeta.')
        return
    
    # Ordenar los archivos por la fecha en el nombre (asumiendo el formato diamesaño, por ejemplo 180125)
    archivos_csv.sort(key=lambda archivo: datetime.strptime(archivo[:-4], '%d%m%y'), reverse=True)
    
    # Seleccionar el archivo más reciente
    archivo_reciente = archivos_csv[0]
    
    # Obtener la fecha del archivo
    nombre_sin_extension = archivo_reciente[:-4]
    try:
        fecha = datetime.strptime(nombre_sin_extension, '%d%m%y').date()
    except ValueError as e:
        print(f"Error al procesar el archivo {archivo_reciente}: {e}")
        return
    
    # Ruta completa del archivo CSV
    ruta_csv = os.path.join(carpeta_csv, archivo_reciente)
    
    # Obtener los datos a insertar
    data_to_insert = procesar_csv_archivo(ruta_csv, fecha)
    
    # Insertar los datos en la base de datos
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO HOLDERS (FECHA, DIRECCION, CANTIDAD)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    cursor.close()
    print(f'Datos del archivo {archivo_reciente} insertados exitosamente.')

# Conexión a la base de datos
connection = None  # Inicializar variable de conexión

try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    print('Conexión ok')

    with connection.cursor() as cursor:
        cursor.execute('SELECT DATABASE();')
        database_HOLDERS = cursor.fetchone()
        print('Conectado a la base de datos', database_HOLDERS)

    # Ruta a la carpeta con los archivos CSV
    carpeta_csv = '/home/mankolepantos/Smol_Holders_Daily/Smol_Holders_Daily/smol_ko/data'

    # Insertar el último archivo CSV a la base de datos
    insertar_ultimo_csv(carpeta_csv, connection)

except pymysql.MySQLError as e:
    print('Error al conectar a la base de datos:', e)

finally:
    if connection:
        connection.close()
        print('Conexión cerrada')
    else:
        print('No se pudo establecer la conexión')
