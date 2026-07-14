# Se importa la librería create_engine de SQLAlchemy para establecer la conexión con la BDD
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

'''
Conexión con la BDD Global de la VM
User: admin
Password: suave
Base de datos: favorita_db
'''
database_url = URL.create(
    "postgresql+psycopg2",
    username="admin",
    password="suave",
    host="localhost",
    port=5432,
    database="favorita_db"
)

engine = create_engine(database_url, future=True)

# Prueba de conexión con la BDD
try:
    with engine.connect() as conn:
        print("Conexion exitosa con PostgreSQL")
except Exception as e:
    print(f"Error: {e}")