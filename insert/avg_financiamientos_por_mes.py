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

# Query para contar las solicitudes de financiamiento agrupadas por mes y año
cursor.execute("""
    SELECT 
        YEAR(fecha_solicitud) AS anio,
        MONTH(fecha_solicitud) AS mes,
        COUNT(*) AS cantidad_total,
        SUM(CASE WHEN estado_solicitud = 'aprobado' THEN 1 ELSE 0 END) AS cantidad_aprobados,
        SUM(CASE WHEN estado_solicitud = 'pendiente' THEN 1 ELSE 0 END) AS cantidad_pendientes,
        SUM(CASE WHEN estado_solicitud = 'rechazado' THEN 1 ELSE 0 END) AS cantidad_rechazados
    FROM 
        raw_financiamientos
    GROUP BY 
        YEAR(fecha_solicitud), MONTH(fecha_solicitud)
    ORDER BY 
        anio, mes
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_financiamientos_por_mes
for fila in resultados:
    anio = fila[0]
    mes = fila[1]
    cantidad_total = fila[2]
    cantidad_aprobados = fila[3]
    cantidad_pendientes = fila[4]
    cantidad_rechazados = fila[5]

    cursor.execute("""
        INSERT INTO avg_financiamientos_por_mes (
            anio, mes, cantidad_total, cantidad_aprobados, cantidad_pendientes, cantidad_rechazados
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, 
    anio, mes, cantidad_total, cantidad_aprobados, cantidad_pendientes, cantidad_rechazados)

# Confirmar los cambios
conn.commit()
conn.close()