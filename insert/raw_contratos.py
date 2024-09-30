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
estados_contrato = ['Asignado', 'Pendiente', 'Activo', 'Finalizado', 'Rescindido', 'Rechazado']
tipos_contrato = ['Alquiler', 'Mudanza', 'Guardado muebles']

# Generar datos para 750 contratos de alquiler
for _ in range(1000):
    # Buscar una publicación válida
    id_publicacion = random.randint(1, 750)
    while not publicacion_existe(cursor, id_publicacion):
        id_publicacion = random.randint(1, 750)

    # Buscar un locador válido
    id_usuario_locador_o_mudanza = random.randint(1, 1300)
    while not usuario_existe(cursor, id_usuario_locador_o_mudanza):
        id_usuario_locador_o_mudanza = random.randint(1, 1300)

    # Buscar un locatario válido, asegurándose de que no sea el mismo que el locador
    id_usuario_locatario = random.randint(1, 1300)
    while id_usuario_locador_o_mudanza == id_usuario_locatario or not usuario_existe(cursor, id_usuario_locatario):
        id_usuario_locatario = random.randint(1, 1300)

    # Buscar un escribano válido, asegurándose de que no sea el mismo que el locador o locatario
    id_usuario_escribano = random.randint(1, 1300)
    while id_usuario_escribano == id_usuario_locador_o_mudanza or id_usuario_escribano == id_usuario_locatario or not usuario_existe(cursor, id_usuario_escribano):
        id_usuario_escribano = random.randint(1, 1300)

    # Generar el tipo de contrato según las probabilidades (80% Alquiler, 10% Mudanza, 10% Guardado muebles)
    prob_tipo_contrato = random.random()
    if prob_tipo_contrato < 0.8:
        tipo_contrato = 'Alquiler'
    elif prob_tipo_contrato < 0.9:
        tipo_contrato = 'Mudanza'
    else:
        tipo_contrato = 'Guardado muebles'

    # Generar estado del contrato de acuerdo a la lógica explicada
    prob_estado = random.random()  # Para definir probabilidades
    if prob_estado < 0.2:  # 20% probabilidad de ser "Asignado"
        estado_contrato = 'Asignado'
        fecha_firma = None  # No hay fecha de firma porque falta
    elif prob_estado < 0.4:  # 20% probabilidad de ser "Pendiente"
        estado_contrato = 'Pendiente'
        fecha_firma = None  # No hay firma del escribano todavía
    elif prob_estado < 0.6:  # 20% probabilidad de ser "Activo"
        estado_contrato = 'Activo'
        fecha_firma = fake.date_between(start_date=fecha_firma_inicio, end_date=fecha_firma_fin)
    elif prob_estado < 0.75:  # 15% probabilidad de ser "Finalizado"
        estado_contrato = 'Finalizado'
        fecha_firma = fake.date_between(start_date=fecha_firma_inicio, end_date=fecha_firma_fin)
    elif prob_estado < 0.85:  # 10% probabilidad de ser "Rescindido"
        estado_contrato = 'Rescindido'
        fecha_firma = fake.date_between(start_date=fecha_firma_inicio, end_date=fecha_firma_fin)
    else:  # 15% probabilidad de ser "Rechazado"
        estado_contrato = 'Rechazado'
        fecha_firma = None  # No hubo firma porque fue rechazado

    # Generar fecha de inicio entre 10 y 90 días después de la fecha de firma (si está firmada)
    if fecha_firma:
        delta_inicio = random.randint(10, 90)
        fecha_inicio_contrato = fecha_firma + timedelta(days=delta_inicio)
    else:
        fecha_inicio_contrato = None

    # Generar fecha de fin entre 6 meses y 3 años después de la fecha de inicio (si aplica)
    if fecha_inicio_contrato:
        delta_fin_min = timedelta(days=180)  # 6 meses
        delta_fin_max = timedelta(days=1095) # 3 años
        fecha_fin_contrato = fecha_inicio_contrato + timedelta(days=random.randint(delta_fin_min.days, delta_fin_max.days))
    else:
        fecha_fin_contrato = None

    # Generar montos de alquiler, mudanza o guardado de muebles con rangos más frecuentes y consistentes
    if tipo_contrato == 'Alquiler':
        if random.random() < 0.7:  # 70% probabilidad de estar entre 150,000 y 600,000 (rangos más comunes)
            monto_renta = round(random.uniform(150000, 600000), 2)
        else:  # 30% probabilidad de montos más altos
            monto_renta = round(random.uniform(600001, 4000000), 2)
    elif tipo_contrato == 'Mudanza':
        monto_renta = round(random.uniform(50000, 300000), 2)  # Montos más bajos para mudanzas
    else:  # Guardado de muebles
        monto_renta = round(random.uniform(80000, 500000), 2)  # Rango moderado para guardado de muebles

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO raw_contratos (
            id_contrato, id_publicacion, id_usuario_locador_o_mudanza, id_usuario_locatario, id_usuario_escribano, 
            tipo_contrato, fecha_firma, fecha_inicio, fecha_fin, monto, estado_contrato
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    id_contrato, id_publicacion, id_usuario_locador_o_mudanza, id_usuario_locatario, id_usuario_escribano,
    tipo_contrato, fecha_firma, fecha_inicio_contrato, fecha_fin_contrato, monto_renta, estado_contrato)

    id_contrato += 1

# Confirmar los cambios
conn.commit()
conn.close()