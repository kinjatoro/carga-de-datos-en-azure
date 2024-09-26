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

# Función para generar un precio sesgado hacia los valores más bajos
def generar_precio_alquiler():
    # Rango ajustado
    precio_base = 150000
    precio_max = 4000000
    # Generamos un número aleatorio con más sesgo hacia los valores bajos
    # random.random() ** 4 hace que el sesgo hacia valores bajos sea más pronunciado
    factor = random.random() ** 4  
    precio = round(precio_base + (precio_max - precio_base) * factor, 2)
    return precio

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Declaración de variables
id_publicacion = 1
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 1500 publicaciones
for _ in range(1500):
    # Fecha de publicación
    fecha_publicacion = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    
    # Tipo de publicación: será siempre 'Alquiler'
    tipo_publicacion = 'Alquiler'
    
    # Generar precio con sesgo más fuerte hacia valores más bajos
    precio_publicacion = generar_precio_alquiler()

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