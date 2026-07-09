# Se importa la librería create_engine de SQLAlchemy para establecer la conexión con la BDD
from sqlalchemy import create_engine

'''
Conexión con la BDD Global de la VM
User: admin
Password: suave
Base de datos: favorita_db
'''
engine = create_engine(
    "postgresql+psycopg2://admin:suave@localhost:5432/favorita_db"
    # "tipo_de_bd+driver://usuario:contraseña@host:puerto/nombre_de_la_BDD"
)

# Prueba de conexión con la BDD
try:
    with engine.connect() as conn:
        print("Conexion exitosa con PostgreSQL")
except Exception as e:
    print(f"Error: {e}")