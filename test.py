import pyodbc
from faker import Faker
import random
from config import server, database, username, password, driver
from datetime import datetime
import requests

# Función para establecer la conexión con la base de datos
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Inicializar Faker
fake = Faker('es_AR')

# Rango aproximado de coordenadas dentro de CABA
latitud_min = -34.70
latitud_max = -34.55
longitud_min = -58.53
longitud_max = -58.35

# Función para generar coordenadas aleatorias dentro de CABA
def generar_coordenadas():
    latitud = round(random.uniform(latitud_min, latitud_max), 6)
    longitud = round(random.uniform(longitud_min, longitud_max), 6)
    return latitud, longitud

# Función para generar un precio sesgado hacia los valores más bajos
def generar_precio_alquiler():
    precio_base = 150000
    precio_max = 4000000
    factor = random.random() ** 4
    precio = round(precio_base + (precio_max - precio_base) * factor, 2)
    return precio

# Función para obtener dirección real usando Nominatim y extraer el barrio
def obtener_direccion_y_barrio(latitud, longitud):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}&zoom=18&addressdetails=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extraemos la dirección completa
        direccion = data['display_name'] if 'display_name' in data else 'Desconocida'
        
        # Extraemos el barrio, puede estar dentro de la key 'suburb' o 'neighbourhood'
        barrio = data['address'].get('suburb') or data['address'].get('neighbourhood') or 'Desconocido'
        
        return direccion, barrio
    else:
        return 'Desconocida', 'Desconocido'

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Declaración de variables
id_publicacion = 154
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 1500 publicaciones
for _ in range(200):
    # Fecha de publicación
    fecha_publicacion = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    
    # Tipo de publicación: será siempre 'Alquiler'
    tipo_publicacion = 'Alquiler'
    
    # Generar precio con sesgo más fuerte hacia valores más bajos
    precio_publicacion = generar_precio_alquiler()

    # Random randint para el id de usuario
    id_usuario = random.randint(1, 1300)

    # Generar coordenadas y obtener dirección y barrio
    latitud, longitud = generar_coordenadas()
    direccion, barrio = obtener_direccion_y_barrio(latitud, longitud)
    
    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_publicaciones2 (
            id_publicacion, fecha_publicacion, precio_publicacion, tipo_publicacion, 
            barrio, latitud, longitud, direccion, id_usuario
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_publicacion, fecha_publicacion, precio_publicacion, tipo_publicacion, 
    barrio, latitud, longitud, direccion, id_usuario)
    
    id_publicacion += 1

# Confirmar los cambios
conn.commit()
conn.close()