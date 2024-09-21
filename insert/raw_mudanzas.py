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

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

#Declaración de variables
id_mudanza = 1
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 1000 mudanzas
for _ in range(250):
    # Fechas
    fecha_solicitud = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    fecha_realizacion = fake.date_between(start_date=fecha_solicitud, end_date=fecha_fin)
    
    # Costo aleatorio de la mudanza
    costo_mudanza = round(random.uniform(80000, 500000), 2)
    
    # Random randint para el id de usuario
    id_usuario = random.randint(1, 1300)

    # Barrios y coordenadas
    barrio_origen = random.choice(barrios_caba)
    barrio_destino = random.choice(barrios_caba)
    
    # Coordenadas aleatorias dentro de CABA
    latitud_origen, longitud_origen = generar_coordenadas()
    latitud_destino, longitud_destino = generar_coordenadas()

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_mudanzas (
            id_mudanza, fecha_solicitud, fecha_realizacion, costo_mudanza, 
            barrio_origen, barrio_destino, latitud_origen, longitud_origen, 
            latitud_destino, longitud_destino, id_usuario
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_mudanza, fecha_solicitud, fecha_realizacion, costo_mudanza, 
    barrio_origen, barrio_destino, latitud_origen, longitud_origen, 
    latitud_destino, longitud_destino, id_usuario)
    
    id_mudanza += 1

# Confirmar los cambios
conn.commit()
conn.close()