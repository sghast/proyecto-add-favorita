from sqlalchemy import create_engine
import pandas as pd

# conexión a la base de datos
engine = create_engine(
     "postgresql+psycopg2://admin:suave@localhost:5432/favorita_db"
)


def export_to_postgres(df, table_name, schema="public"):
    print(f"Iniciando exportación de la tabla '{schema}.{table_name}'...")

    try:
        # aceptar tanto DataFrames de polars como de pandas
        if hasattr(df, "to_pandas"):
            pandas_df = df.to_pandas()
        else:
            pandas_df = df

        # exportar el DataFrame a la base de datos
        pandas_df.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists="replace",
            index=False
        )

        print(f"Tabla '{schema}.{table_name}' exportada con éxito")
    except Exception as e:
        print(f"Error al exportar la tabla '{schema}.{table_name}': {e}")
        raise