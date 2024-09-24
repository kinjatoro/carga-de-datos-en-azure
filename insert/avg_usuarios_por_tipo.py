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

# Query para contar usuarios por tipo de usuario
cursor.execute("""
    SELECT 
        tipo_usuario,
        COUNT(id_usuario) AS total_usuarios
    FROM 
        raw_usuarios
    WHERE 
        tipo_usuario IS NOT NULL
    GROUP BY 
        tipo_usuario
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_usuarios_por_tipo
for fila in resultados:
    tipo_usuario = fila[0]
    total_usuarios = fila[1]

    cursor.execute("""
        INSERT INTO avg_usuarios_por_tipo (
            tipo_usuario, total_usuarios
        )
        VALUES (?, ?)
    """, 
    tipo_usuario, total_usuarios)

# Confirmar los cambios
conn.commit()
conn.close()