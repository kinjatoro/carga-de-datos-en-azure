import pyodbc
from config import server, database, username, password, driver
from datetime import datetime
import math

# Función para establecer la conexión con la base de datos
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Función para calcular la distancia utilizando la fórmula del Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c  # Distancia en km
    return distance

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Query para obtener las mudanzas y calcular la distancia
cursor.execute("""
    SELECT 
        YEAR(fecha_realizacion) AS anio,
        MONTH(fecha_realizacion) AS mes,
        latitud_origen,
        longitud_origen,
        latitud_destino,
        longitud_destino
    FROM 
        raw_mudanzas
    WHERE 
        fecha_realizacion IS NOT NULL
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Diccionario para almacenar las distancias por mes/año
distancias_por_mes = {}

# Calcular la distancia para cada mudanza
for fila in resultados:
    anio = fila[0]
    mes = fila[1]
    latitud_origen = fila[2]
    longitud_origen = fila[3]
    latitud_destino = fila[4]
    longitud_destino = fila[5]

    # Calcular la distancia usando la función Haversine
    distancia = haversine(latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    
    # Crear una clave para el año y mes
    key = (anio, mes)

    # Sumar la distancia y contar las mudanzas
    if key not in distancias_por_mes:
        distancias_por_mes[key] = {'total_distancia': 0, 'count': 0}
    
    distancias_por_mes[key]['total_distancia'] += distancia
    distancias_por_mes[key]['count'] += 1

# Insertar los resultados en la tabla avg_distancia_mudanza_por_mes
for key, value in distancias_por_mes.items():
    anio, mes = key
    distancia_promedio = value['total_distancia'] / value['count'] if value['count'] > 0 else 0
    mudanzas_realizadas = value['count']

    cursor.execute("""
        INSERT INTO avg_distancia_mudanza_por_mes (
            anio, mes, distancia_promedio, mudanzas_realizadas
        )
        VALUES (?, ?, ?, ?)
    """, 
    anio, mes, distancia_promedio, mudanzas_realizadas)

# Confirmar los cambios
conn.commit()
conn.close()