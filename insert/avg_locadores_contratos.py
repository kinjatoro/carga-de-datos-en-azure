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

# Query para contar contratos por estado para cada locador
cursor.execute("""
    SELECT 
        id_usuario_locador,
        SUM(CASE WHEN estado_contrato = 'activo' THEN 1 ELSE 0 END) AS contratos_activos,
        SUM(CASE WHEN estado_contrato = 'finalizado' THEN 1 ELSE 0 END) AS contratos_finalizados,
        SUM(CASE WHEN estado_contrato = 'rescindido' THEN 1 ELSE 0 END) AS contratos_rescindidos
    FROM 
        raw_contratos
    GROUP BY 
        id_usuario_locador
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla resumen_locadores_contratos
for fila in resultados:
    id_usuario_locador = fila[0]
    contratos_activos = fila[1]
    contratos_finalizados = fila[2]
    contratos_rescindidos = fila[3]

    cursor.execute("""
        INSERT INTO avg_locadores_contratos (
            id_usuario_locador, contratos_activos, contratos_finalizados, contratos_rescindidos
        )
        VALUES (?, ?, ?, ?)
    """, 
    id_usuario_locador, contratos_activos, contratos_finalizados, contratos_rescindidos)

# Confirmar los cambios
conn.commit()
conn.close()