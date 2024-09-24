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

# Query para contar los contratos en cada estado agrupados por año
cursor.execute("""
    SELECT 
        YEAR(fecha_firma) AS anio,
        SUM(CASE WHEN estado_contrato = 'Activo' THEN 1 ELSE 0 END) AS total_activos,
        SUM(CASE WHEN estado_contrato = 'Finalizado' THEN 1 ELSE 0 END) AS total_finalizados,
        SUM(CASE WHEN estado_contrato = 'Rescindido' THEN 1 ELSE 0 END) AS total_rescindidos
    FROM 
        raw_contratos
    WHERE 
        fecha_firma IS NOT NULL
    GROUP BY 
        YEAR(fecha_firma)
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_contratos_por_anio
for fila in resultados:
    anio = fila[0]
    total_activos = fila[1]
    total_finalizados = fila[2]
    total_rescindidos = fila[3]

    cursor.execute("""
        INSERT INTO avg_contratos_por_anio (
            anio, total_activos, total_finalizados, total_rescindidos
        )
        VALUES (?, ?, ?, ?)
    """, 
    anio, total_activos, total_finalizados, total_rescindidos)

# Confirmar los cambios
conn.commit()
conn.close()