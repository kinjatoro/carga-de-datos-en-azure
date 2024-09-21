import pyodbc
from ..config import server, database, username, password, driver

# Función para establecer la conexión
def conectar_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Establecer la conexión
conn = conectar_db()
cursor = conn.cursor()

# Leer el archivo SQL
with open('crear-tablas-avg.sql', 'r', encoding='utf-8') as file:
    sql_commands = file.read()

# Ejecutar todos los comandos
cursor.execute(sql_commands)

# Confirmar los cambios
conn.commit()
conn.close()
