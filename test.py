import pyodbc
import random
from config import server, database, username, password, driver
from decimal import Decimal  # Importar Decimal

# Función para establecer la conexión con la base de datos
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Función para generar la ganancia
def generar_ganancia(precio):
    probabilidad = random.random()
    if probabilidad < 0.6:
        return Decimal(0)  # 60% probabilidad de que sea 0
    else:
        return round(precio * Decimal(0.5), 2)  # Convertir 0.5 a Decimal y redondear a 2 decimales

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Obtener todas las publicaciones
cursor.execute("SELECT id_publicacion, precio_publicacion FROM raw_publicaciones")
publicaciones = cursor.fetchall()

# Actualizar cada registro con la ganancia generada
for publicacion in publicaciones:
    id_publicacion = publicacion[0]
    precio_publicacion = publicacion[1]
    ganancia_generada = generar_ganancia(precio_publicacion)

    # Actualizar la fila con el valor de ganancia_generada
    cursor.execute("""
        UPDATE raw_publicaciones
        SET ganancia_generada = ?
        WHERE id_publicacion = ?
    """, ganancia_generada, id_publicacion)

# Confirmar los cambios
conn.commit()
conn.close()

print("Ganancias generadas y actualizadas correctamente.")