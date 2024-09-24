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

# Query para contar contratos activos por locador
cursor.execute("""
    SELECT 
        id_usuario_locador,
        COUNT(id_contrato) AS total_contratos_activos
    FROM 
        raw_contratos
    WHERE 
        estado_contrato = 'Activo'
    GROUP BY 
        id_usuario_locador
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_locadores_contratos_activos
for fila in resultados:
    id_usuario_locador = fila[0]
    total_contratos_activos = fila[1]

    cursor.execute("""
        INSERT INTO avg_locadores_contratos_activos (
            id_usuario_locador, total_contratos_activos
        )
        VALUES (?, ?)
    """, 
    id_usuario_locador, total_contratos_activos)

# Confirmar los cambios
conn.commit()
conn.close()