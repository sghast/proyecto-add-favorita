
# ==== CONEXIÓN CON POSTGRE =======

import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def _normalize_value(value):
    # Si es un tipo de NumPy, extrae el tipo nativo de Python (.item())
    if isinstance(value, np.generic):
        return value.item()
    # Si es un valor nulo de Pandas/NumPy, envíalo como None para que Postgres lo guarde como NULL
    if pd.isna(value):
        return None
    return value


def export_to_postgres(df, table_name, schema="public"):
    print(f"Iniciando exportación de la tabla '{schema}.{table_name}'...")

    if hasattr(df, "to_pandas"):
        pandas_df = df.to_pandas()
    else:
        pandas_df = df

    # Parámetros estables con timeout de seguridad
    conn_params = {
        "host": "localhost",
        "database": "favorita_db",
        "user": "admin",
        "password": "suave",
        "port": 5432,
        "options": "-c statement_timeout=10000"  # Evita bloqueos infinitos
    }

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        table_path = f"{schema}.{table_name}"
        
        #limpiamos la tabla existente manteniendo su estructura intacta
        print(f"Limpiando datos antiguos de {table_path}...")
        cursor.execute(f"SET lock_timeout = '5s';") 
        cursor.execute(f"TRUNCATE TABLE {table_path} RESTART IDENTITY CASCADE;")

        #Mapeamos las columnas existentes
        columns = [f'"{c}"' for c in pandas_df.columns]
        query = f'INSERT INTO {table_path} ({", ".join(columns)}) VALUES %s'
        
        #aplicamos tu función de normalización fila por fila
        print(f"Normalizando y preparando {len(pandas_df)} filas...")
        values = [
            tuple(_normalize_value(x) for x in row)
            for row in pandas_df.to_numpy(dtype=object)
        ]
        
        print(f"Insertando datos de forma masiva...")
        execute_values(cursor, query, values)
        
        conn.commit()
        print(f"Tabla '{schema}.{table_name}' exportada con éxito")

    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"Error durante la exportación: {e}")
        raise e
        
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()