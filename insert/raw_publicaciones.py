import pyodbc
from faker import Faker
import random
from config import server, database, username, password, driver
from datetime import datetime

# Función para establecer la conexión con la base de datos
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Inicializar Faker
fake = Faker('es_AR')

# Lista de barrios de CABA
barrios_caba = [
    'Palermo', 'Recoleta', 'Belgrano', 'Caballito', 'San Telmo', 'Villa Urquiza', 
    'Villa Crespo', 'Almagro', 'Balvanera', 'Boedo', 'Colegiales', 'Nuñez', 'Retiro',
    'Villa Devoto', 'Villa Lugano', 'Villa Pueyrredón', 'Villa del Parque', 'Barracas',
    'La Boca', 'Mataderos', 'Parque Chacabuco', 'Parque Patricios', 'Paternal',
    'Puerto Madero', 'Saavedra', 'San Cristóbal', 'Villa Luro', 'Liniers', 'Flores', 'Floresta'
]

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

# Tipos de publicación y probabilidades correspondientes
tipos_publicacion = ['Venta', 'Alquiler', 'Alquiler temporal (por día)']
probabilidades_publicacion = [30, 60, 10]  # Probabilidades para Venta (30%), Alquiler (60%), Alquiler temporal (10%)

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Declaración de variables
id_publicacion = 251
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 250 publicaciones
for _ in range(500):
    # Fecha de publicación
    fecha_publicacion = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    
    # Seleccionar el tipo de publicación aleatoriamente con las probabilidades
    tipo_publicacion = random.choices(tipos_publicacion, weights=probabilidades_publicacion, k=1)[0]
    
    # Definir el precio en función del tipo de publicación
    if tipo_publicacion == 'Venta':
        # Ajustar el rango para que no exceda el máximo permitido por DECIMAL(10,2)
        precio_publicacion = round(random.uniform(36000000, 99999999.99), 2)
    elif tipo_publicacion == 'Alquiler':
        precio_publicacion = round(random.uniform(150000, 4000000), 2)
    else:  # 'Alquiler temporal (por día)'
        precio_publicacion = round(random.uniform(40000, 150000), 2)

    # Random randint para el id de usuario
    id_usuario = random.randint(1, 1300)

    # Barrio y coordenadas
    barrio = random.choice(barrios_caba)
    latitud, longitud = generar_coordenadas()

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_publicaciones (
            id_publicacion, fecha_publicacion, precio_publicacion, tipo_publicacion, 
            barrio, latitud, longitud, id_usuario
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_publicacion, fecha_publicacion, precio_publicacion, tipo_publicacion, 
    barrio, latitud, longitud, id_usuario)
    
    id_publicacion += 1

# Confirmar los cambios
conn.commit()
conn.close()