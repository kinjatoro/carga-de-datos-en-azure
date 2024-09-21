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

    # Monto del pago (entre 100,000 y 15,000,000)
    monto_pago = round(random.uniform(100000, 15000000), 2)
    
    # Random randint para id_publicacion (de 1 a 750)
    id_publicacion = random.randint(1, 750)
    
    # Random randint para id_usuario (de 1 a 1300)
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