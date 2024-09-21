import pyodbc
from faker import Faker
import random
from config import server, database, username, password, driver

# Función para establecer la conexión
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# -------------------------------------------

# Inicializar Faker
fake = Faker('es_AR')
tipos_usuario = ['inquilino', 'propietario', 'empleado', 'notario', 'abogado']
numero_registros = 10

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

for _ in range(numero_registros):
    id_usuario = fake.uuid4()
    nombre = fake.name()
    email = fake.email()
    telefono = fake.phone_number()
    tipo_usuario = random.choice(tipos_usuario)
    estado = random.choice(['activo', 'inactivo'])  # Asegúrate de usar una lista aquí

    cursor.execute("""
        INSERT INTO usuarios_usuario (id_usuario, nombre, email, telefono, tipo_usuario, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, id_usuario, nombre, email, telefono, tipo_usuario, estado)

# Confirmar los cambios
conn.commit()
conn.close()
