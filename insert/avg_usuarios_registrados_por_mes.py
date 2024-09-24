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

# Query para contar usuarios registrados por mes y año
cursor.execute("""
    SELECT 
        YEAR(fecha_registro) AS anio,
        MONTH(fecha_registro) AS mes,
        COUNT(id_usuario) AS total_usuarios
    FROM 
        raw_usuarios
    WHERE 
        fecha_registro IS NOT NULL
    GROUP BY 
        YEAR(fecha_registro), MONTH(fecha_registro)
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_usuarios_registrados_por_mes
for fila in resultados:
    anio = fila[0]
    mes = fila[1]
    total_usuarios = fila[2]

    cursor.execute("""
        INSERT INTO avg_usuarios_registrados_por_mes (
            anio, mes, total_usuarios
        )
        VALUES (?, ?, ?)
    """, 
    anio, mes, total_usuarios)

# Confirmar los cambios
conn.commit()
conn.close()