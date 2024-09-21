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
tipos_usuario = ['inquilino', 'propietario', 'abogado', 'empleado', 'mudanzas']
probabilidades = [75, 10, 5, 5, 5]

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

#Declaración de variables
id = 301
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.today()

for _ in range(1000):
    id_usuario = id
    nombre = fake.name()
    tipo_usuario = random.choices(tipos_usuario, weights=probabilidades)[0]
    fecha_registro = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)  

    cursor.execute("""
        INSERT INTO raw_usuarios (id_usuario, nombre, tipo_usuario, fecha_registro)
        VALUES (?, ?, ?, ?)
    """, id_usuario, nombre, tipo_usuario, fecha_registro)

    id+=1

# Confirmar los cambios
conn.commit()
conn.close()
