import pyodbc
from config import server, database, username, password, driver

# Función para establecer la conexión con la base de datos
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Query para contar las solicitudes de financiamiento por estado
cursor.execute("""
    SELECT 
        estado_solicitud, 
        COUNT(*) AS cantidad
    FROM 
        raw_financiamientos
    GROUP BY 
        estado_solicitud
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_financiamientos_estado
for fila in resultados:
    estado_solicitud = fila[0]
    cantidad = fila[1]

    cursor.execute("""
        INSERT INTO avg_financiamientos_estado (
            estado_solicitud, cantidad
        )
        VALUES (?, ?)
    """, 
    estado_solicitud, cantidad)

# Confirmar los cambios
conn.commit()
conn.close()