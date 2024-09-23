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

# Query para contar mudanzas por barrio de origen
cursor.execute("""
    SELECT 
        barrio_origen AS barrio,
        COUNT(id_mudanza) AS total_mudanzas
    FROM 
        raw_mudanzas
    WHERE 
        barrio_origen IS NOT NULL
    GROUP BY 
        barrio_origen
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_mudanzas_por_barrio_origen
for fila in resultados:
    barrio_origen = fila[0]
    total_mudanzas = fila[1]

    cursor.execute("""
        INSERT INTO avg_mudanzas_por_barrio_origen (
            barrio_origen, total_mudanzas
        )
        VALUES (?, ?)
    """, 
    barrio_origen, total_mudanzas)

# Confirmar los cambios
conn.commit()
conn.close()