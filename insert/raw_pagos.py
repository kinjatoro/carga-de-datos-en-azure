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

# Función para verificar si el id de usuario existe
def usuario_existe(cursor, id_usuario):
    cursor.execute("SELECT COUNT(1) FROM raw_usuarios WHERE id_usuario = ?", id_usuario)
    return cursor.fetchone()[0] > 0

# Función para verificar si el id de publicación existe
def publicacion_existe(cursor, id_publicacion):
    cursor.execute("SELECT COUNT(1) FROM raw_publicaciones WHERE id_publicacion = ?", id_publicacion)
    return cursor.fetchone()[0] > 0

# Inicializar Faker
fake = Faker('es_AR')

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Declaración de variables
id_pago = 1
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 500 pagos
for _ in range(500):
    # Fecha del pago
    fecha_pago = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)

    # Monto del pago (entre 100,000 y 1,500,000)
    monto_pago = round(random.uniform(100000, 1500000), 2)
    
    # Buscar una publicación válida
    id_publicacion = random.randint(1, 750)
    while not publicacion_existe(cursor, id_publicacion):
        id_publicacion = random.randint(1, 750)
    
    # Buscar un usuario válido
    id_usuario = random.randint(1, 1300)
    while not usuario_existe(cursor, id_usuario):
        id_usuario = random.randint(1, 1300)

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_pagos (
            id_pago, fecha, monto, id_publicacion, id_usuario
        )
        VALUES (?, ?, ?, ?, ?)
    """, 
    id_pago, fecha_pago, monto_pago, id_publicacion, id_usuario)
    
    id_pago += 1

# Confirmar los cambios
conn.commit()
conn.close()