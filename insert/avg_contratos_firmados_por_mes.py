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

# Query para contar contratos firmados por mes y año
cursor.execute("""
    SELECT 
        YEAR(fecha_firma) AS anio,
        MONTH(fecha_firma) AS mes,
        COUNT(id_contrato) AS total_contratos
    FROM 
        raw_contratos
    WHERE 
        fecha_firma IS NOT NULL
    GROUP BY 
        YEAR(fecha_firma), MONTH(fecha_firma)
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_contratos_firmados_por_mes
for fila in resultados:
    anio = fila[0]
    mes = fila[1]
    total_contratos = fila[2]

    cursor.execute("""
        INSERT INTO avg_contratos_firmados_por_mes (
            anio, mes, total_contratos
        )
        VALUES (?, ?, ?)
    """, 
    anio, mes, total_contratos)

# Confirmar los cambios
conn.commit()
conn.close()