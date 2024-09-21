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

# Query para agrupar por barrio y calcular los totales y promedios de alquileres
cursor.execute("""
    SELECT 
        p.barrio AS barrio,
        COUNT(c.id_contrato) AS total_alquileres,
        AVG(c.monto_renta) AS renta_promedio,
        SUM(c.monto_renta) AS ingreso_total,
        MAX(c.monto_renta) AS renta_maxima,
        MIN(c.monto_renta) AS renta_minima
    FROM 
        raw_contratos c
    JOIN 
        raw_publicaciones p ON c.id_publicacion = p.id_publicacion
    GROUP BY 
        p.barrio
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_resumen_alquileres
for fila in resultados:
    barrio = fila[0]
    total_alquileres = fila[1]
    renta_promedio = fila[2]
    ingreso_total = fila[3]
    renta_maxima = fila[4]
    renta_minima = fila[5]

    cursor.execute("""
        INSERT INTO avg_resumen_alquileres (
            barrio, total_alquileres, renta_promedio, ingreso_total, renta_maxima, renta_minima
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, 
    barrio, total_alquileres, renta_promedio, ingreso_total, renta_maxima, renta_minima)

# Confirmar los cambios
conn.commit()
conn.close()