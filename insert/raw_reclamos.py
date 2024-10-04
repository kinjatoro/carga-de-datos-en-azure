import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta
from config import server, database, username, password, driver

# Función para establecer la conexión con la base de datos
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Función para verificar si el id de usuario existe
def usuario_existe(cursor, id_usuario):
    cursor.execute("SELECT COUNT(1) FROM raw_usuarios WHERE id_usuario = ?", id_usuario)
    return cursor.fetchone()[0] > 0

# Inicializar Faker
fake = Faker('es_AR')

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Posibles estados de reclamo y sus categorías
estados_reclamo = ['Abierto', 'En Proceso', 'Resuelto', 'Cerrado']
categorias_reclamo = ['Problemas Técnicos', 'Cobros Incorrectos', 'Servicio Deficiente', 'Otros']

# Definir límites de fechas para "Abierto" y "En Proceso" (máximo 4 meses atrás)
fecha_actual = datetime.today().date()
limite_fecha_abierto_proceso = fecha_actual - timedelta(days=120)

# Generar datos para 1000 reclamos
id_reclamo = 1
for _ in range(126):
    # Buscar un usuario válido
    id_usuario = random.randint(1, 1300)
    while not usuario_existe(cursor, id_usuario):
        id_usuario = random.randint(1, 1300)

    # Seleccionar un estado de reclamo
    estado_reclamo = random.choice(estados_reclamo)

    # Generar la fecha del reclamo según el estado
    if estado_reclamo in ['Abierto', 'En Proceso']:
        # Máximo 4 meses de antigüedad
        fecha_reclamo = fake.date_between(start_date=limite_fecha_abierto_proceso, end_date=fecha_actual)
    else:
        # Para "Resuelto" y "Cerrado", generar sin restricciones de fecha
        fecha_reclamo = fake.date_between(start_date=datetime(2020, 1, 1).date(), end_date=fecha_actual)

    # Seleccionar una categoría de reclamo
    categoria_reclamo = random.choice(categorias_reclamo)

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_reclamos (id_reclamo, fecha_reclamo, estado, id_usuario, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, id_reclamo, fecha_reclamo, estado_reclamo, id_usuario, categoria_reclamo)

    id_reclamo += 1

# Confirmar los cambios
conn.commit()
conn.close()