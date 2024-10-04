import pyodbc
from faker import Faker
import random
from config import server, database, username, password, driver
from datetime import datetime
import requests
import time

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
longitud_max = -58.42

# Función para generar coordenadas aleatorias dentro de CABA
def generar_coordenadas():
    latitud = round(random.uniform(latitud_min, latitud_max), 6)
    longitud = round(random.uniform(longitud_min, longitud_max), 6)
    return latitud, longitud

# Función para obtener dirección real usando Nominatim y extraer el barrio
def obtener_direccion_y_barrio(latitud, longitud, reintentos=3):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}&zoom=18&addressdetails=1'
    for _ in range(reintentos):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                direccion = data.get('display_name', 'Desconocida')
                barrio = data['address'].get('suburb') or data['address'].get('neighbourhood') or 'Desconocido'
                return direccion, barrio
        except Exception as e:
            print(f"Error: {e}, reintentando...")
    return 'Desconocida', 'Desconocido'

# Función para generar cantidad de habitaciones
def generar_habitaciones():
    prob = random.random()
    if prob < 0.5:
        return 1  # 50% de probabilidades de ser 1 ambiente
    elif prob < 0.8:
        return 2  # 30% para 2 ambientes
    elif prob < 0.95:
        return 3  # 15% para 3 ambientes
    else:
        return 4  # 5% para 4 o más ambientes

# Función para generar superficie en m2
def generar_superficie(habitaciones):
    if habitaciones == 1:
        return random.randint(30, 50)
    elif habitaciones == 2:
        return random.randint(50, 80)
    elif habitaciones == 3:
        return random.randint(80, 120)
    else:
        return random.randint(120, 200)

# Función para generar un precio en función de los metros cuadrados
def generar_precio(superficie):
    precio_base_por_m2 = 6000
    variabilidad = random.uniform(-1000, 2000)
    precio_por_m2 = precio_base_por_m2 + variabilidad
    return round(precio_por_m2 * superficie, 2)

# Función para generar el tipo de propiedad
def generar_tipo(superficie):
    return "Departamento" if superficie < 100 else "Casa"

# Función para generar el estado de la publicación
def generar_estado():
    return 'Activo' if random.random() < 0.8 else 'Inactivo'

# Función para generar ganancia
def generar_ganancia(precio):
    probabilidad = random.random()
    return 0 if probabilidad < 0.6 else round(precio * 0.5, 2)

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Declaración de variables
id_publicacion = 603
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 400 publicaciones
for _ in range(5):
    fecha_publicacion = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    latitud, longitud = generar_coordenadas()
    direccion, barrio = obtener_direccion_y_barrio(latitud, longitud)

    habitaciones = generar_habitaciones()
    superficie_total_m2 = generar_superficie(habitaciones)
    precio_publicacion = generar_precio(superficie_total_m2)
    tipo = generar_tipo(superficie_total_m2)
    estado = generar_estado()
    id_usuario = random.randint(1, 10)  # Por ejemplo, id de usuario aleatorio
    ganancia_generada = generar_ganancia(precio_publicacion)

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_publicaciones (
            id_publicacion, fecha_publicacion, precio_publicacion, direccion, 
            habitaciones, barrio, latitud, longitud, estado, id_usuario, 
            tipo, superficie_total_m2, ganancia_generada
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_publicacion, fecha_publicacion, precio_publicacion, direccion, 
    habitaciones, barrio, latitud, longitud, estado, id_usuario, 
    tipo, superficie_total_m2, ganancia_generada)
    
    id_publicacion += 1

# Confirmar los cambios
conn.commit()
conn.close()

print("Datos insertados exitosamente.")