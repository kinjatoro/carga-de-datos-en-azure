import pyodbc
from faker import Faker
import random
from config import server, database, username, password, driver
from datetime import datetime, timedelta

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
id_contrato = 1
fecha_firma_inicio = datetime(2023, 1, 1).date()  # Asegurarse de que sea un objeto date
fecha_firma_fin = datetime.today().date()         # Convertir a date

# Posibles estados de contrato
estados_contrato = ['Activo', 'Finalizado', 'Rescindido']

# Generar datos para 750 contratos de alquiler
for _ in range(750):
    # Buscar una publicación válida
    id_publicacion = random.randint(1, 750)
    while not publicacion_existe(cursor, id_publicacion):
        id_publicacion = random.randint(1, 750)

    # Buscar un locador válido
    id_usuario_locador = random.randint(1, 1300)
    while not usuario_existe(cursor, id_usuario_locador):
        id_usuario_locador = random.randint(1, 1300)

    # Buscar un locatario válido, asegurándose de que no sea el mismo que el locador
    id_usuario_locatario = random.randint(1, 1300)
    while id_usuario_locador == id_usuario_locatario or not usuario_existe(cursor, id_usuario_locatario):
        id_usuario_locatario = random.randint(1, 1300)

    # Buscar un abogado válido, asegurándose de que no sea el mismo que el locador o locatario
    id_usuario_abogado = random.randint(1, 1300)
    while id_usuario_abogado == id_usuario_locador or id_usuario_abogado == id_usuario_locatario or not usuario_existe(cursor, id_usuario_abogado):
        id_usuario_abogado = random.randint(1, 1300)

    # Generar fecha de firma entre el 1 de enero de 2023 y hoy
    fecha_firma = fake.date_between(start_date=fecha_firma_inicio, end_date=fecha_firma_fin)

    # Generar fecha de inicio entre 10 y 90 días después de la fecha de firma
    delta_inicio = random.randint(10, 90)
    fecha_inicio_contrato = fecha_firma + timedelta(days=delta_inicio)

    # Generar fecha de fin entre 6 meses y 3 años después de la fecha de inicio
    delta_fin_min = timedelta(days=180)  # 6 meses
    delta_fin_max = timedelta(days=1095) # 3 años
    fecha_fin_contrato = fecha_inicio_contrato + timedelta(days=random.randint(delta_fin_min.days, delta_fin_max.days))

    # Monto de la renta (entre 150,000 y 4,000,000)
    monto_renta = round(random.uniform(150000, 4000000), 2)

    # Estado del contrato
    estado_contrato = random.choice(estados_contrato)

    # Si el contrato está finalizado, asegurar que fecha_fin < hoy
    if estado_contrato == 'Finalizado':
        # Si fecha_fin_contrato >= hoy, ajustarla para que sea antes de hoy
        if fecha_fin_contrato >= datetime.today().date():
            # Calcular el máximo delta posible
            max_delta = (datetime.today().date() - fecha_inicio_contrato).days - 1
            if max_delta < 180:  # Asegurar al menos 6 meses
                # Si no es posible cumplir con los 6 meses, ajustar fecha_inicio_contrato
                fecha_inicio_contrato = datetime.today().date() - timedelta(days=180 + random.randint(0, 90))
                fecha_fin_contrato = fecha_inicio_contrato + timedelta(days=random.randint(180, 1095))
            else:
                # Asegurar que la fecha de fin no exceda el máximo permitido
                fecha_fin_contrato = fecha_inicio_contrato + timedelta(days=random.randint(180, min(1095, max_delta)))

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_contratos (
            id_contrato, id_publicacion, id_usuario_locador, id_usuario_locatario, id_usuario_abogado, 
            fecha_firma, fecha_inicio, fecha_fin, monto_renta, estado_contrato
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_contrato, id_publicacion, id_usuario_locador, id_usuario_locatario, id_usuario_abogado,
    fecha_firma, fecha_inicio_contrato, fecha_fin_contrato, monto_renta, estado_contrato)

    id_contrato += 1

# Confirmar los cambios
conn.commit()
conn.close()