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
id_contrato = 251
fecha_inicio_rango = datetime(2023, 1, 1)
fecha_fin_rango = datetime(2026, 12, 31)

# Posibles estados de contrato
estados_contrato = ['Activo', 'Finalizado', 'Rescindido']

# Generar datos para 250 contratos de alquiler
for _ in range(750):
    # Selección aleatoria de id_publicacion entre las publicaciones de alquiler (de 1 a 750)
    id_publicacion = random.randint(1, 750)

    # Random randint para el locador y locatario (asegurando que no sean la misma persona)
    id_usuario_locador = random.randint(1, 1300)
    id_usuario_locatario = random.randint(1, 1300)
    
    while id_usuario_locador == id_usuario_locatario:
        id_usuario_locatario = random.randint(1, 1300)

    # Fechas del contrato
    fecha_firma = fake.date_between(start_date=fecha_inicio_rango, end_date=fecha_fin_rango)
    fecha_inicio_contrato = fake.date_between(start_date=fecha_firma, end_date=fecha_firma)
    fecha_fin_contrato = fake.date_between(start_date=fecha_inicio_contrato, end_date=fecha_fin_rango)

    # Monto de la renta (entre 150,000 y 4,000,000)
    monto_renta = round(random.uniform(150000, 4000000), 2)

    # Estado del contrato
    estado_contrato = random.choice(estados_contrato)

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_contratos (
            id_contrato, id_publicacion, id_usuario_locador, id_usuario_locatario, 
            fecha_firma, fecha_inicio, fecha_fin, monto_renta, estado_contrato
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_contrato, id_publicacion, id_usuario_locador, id_usuario_locatario, 
    fecha_firma, fecha_inicio_contrato, fecha_fin_contrato, monto_renta, estado_contrato)

    id_contrato += 1

# Confirmar los cambios
conn.commit()
conn.close()