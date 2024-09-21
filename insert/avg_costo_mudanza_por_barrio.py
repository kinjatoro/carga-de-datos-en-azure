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

# Query para agrupar por barrio y calcular el costo promedio de mudanzas y el número de mudanzas realizadas
cursor.execute("""
    SELECT 
        barrio_origen AS barrio, 
        AVG(costo_mudanza) AS costo_promedio_mudanza, 
        COUNT(id_mudanza) AS mudanzas_realizadas
    FROM 
        raw_mudanzas
    GROUP BY 
        barrio_origen
""")

# Obtener los resultados del SELECT
resultados = cursor.fetchall()

# Insertar los resultados en la tabla avg_costo_mudanza_por_barrio
for fila in resultados:
    barrio = fila[0]
    costo_promedio_mudanza = fila[1]
    mudanzas_realizadas = fila[2]

    cursor.execute("""
        INSERT INTO avg_costo_mudanza_por_barrio (
            barrio, costo_promedio_mudanza, mudanzas_realizadas
        )
        VALUES (?, ?, ?)
    """, 
    barrio, costo_promedio_mudanza, mudanzas_realizadas)

# Confirmar los cambios
conn.commit()
conn.close()