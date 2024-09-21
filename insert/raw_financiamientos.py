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

# Lista de posibles estados de la solicitud
estados_solicitud = ['Pendiente', 'Aprobado', 'Rechazado']

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Declaración de variables
id_financiamiento = 1
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

# Generar datos para 250 financiamientos
for _ in range(250):
    # Fecha de solicitud
    fecha_solicitud = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    
    # Monto solicitado
    monto_solicitado = round(random.uniform(50000, 1000000), 2)  # Monto solicitado entre 50k y 1 millón
    
    # Estado de la solicitud
    estado_solicitud = random.choice(estados_solicitud)

    # Lógica para el monto aprobado
    if estado_solicitud == 'Aprobado':
        monto_aprobado = round(random.uniform(0, monto_solicitado), 2)  # Monto aprobado <= monto solicitado
    else:
        monto_aprobado = 0  # Si está Pendiente o Rechazado, monto aprobado es 0

    # Random randint para el id de usuario
    id_usuario = random.randint(1, 1300)

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_financiamientos (
            id_financiamiento, fecha_solicitud, monto_solicitado, monto_aprobado, 
            estado_solicitud, id_usuario
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, 
    id_financiamiento, fecha_solicitud, monto_solicitado, monto_aprobado, 
    estado_solicitud, id_usuario)
    
    id_financiamiento += 1

# Confirmar los cambios
conn.commit()
conn.close()