import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# conexión a la base de datos
database_url = URL.create(
    "postgresql+psycopg2",
    username="admin",
    password="suave",
    host="localhost",
    port=5432,
    database="favorita_db"
)

engine = create_engine(database_url, future=True)


def export_to_postgres(df, table_name, schema="public"):
    print(f"Iniciando exportación de la tabla '{schema}.{table_name}'...")

    if hasattr(df, "to_pandas"):
        pandas_df = df.to_pandas()
    else:
        pandas_df = df

    pandas_df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False
    )

    print(f"Tabla '{schema}.{table_name}' exportada con éxito")