import pyodbc

# Parámetros de conexión
server = 'analyticssmartmove.database.windows.net'
database = 'AnalyticsGroup3'
username = 'smartmove'
password = 'Sqlgrupo3'
driver = '{ODBC Driver 17 for SQL Server}'

# Establecer la conexión
conn = pyodbc.connect(
    f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
)
cursor = conn.cursor()

# -------------------------------------------
# FAKER

from faker import Faker
import random

fake = Faker('es_AR')
tipos_usuario = ['inquilino', 'propietario', 'empleado', 'notario', 'abogado']
estado = ["activo, inactivo"]

# Número de registros a insertar
numero_registros = 10

for _ in range(numero_registros):
    id_usuario = fake.uuid4()
    
    nombre = fake.name()
    email = fake.email()
    telefono = fake.phone_number()
    tipo_usuario = random.choice(tipos_usuario)
    estado = random.choice(tipos_usuario)

    cursor.execute("""
        INSERT INTO usuarios_usuario (id_usuario, nombre, email, telefono, tipo_usuario, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, id_usuario, nombre, email, telefono, tipo_usuario, estado)

# Confirmar los cambios
conn.commit()
conn.close()

