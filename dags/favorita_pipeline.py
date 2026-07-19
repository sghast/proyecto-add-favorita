import sys
from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.load.load_data import load_all_data
from scripts.transform.consolidate_data import consolidate_data
from scripts.database.export_postgres import export_to_postgres
from scripts.database.export_reports import export_all_reports


def extraer_datos():
    datasets = load_all_data()

    print("Extrayendo datos de Favorita:")
    for name, df in datasets.items():
        print(f"- {name}: filas={df.height}, columnas={df.width}")

    return "Datos extraídos"


def transformar_datos():
    consolidated = consolidate_data()

    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    consolidated.write_parquet(output_dir / "favorita_consolidated.parquet")

    print(
        "Transformación completa: datos consolidados guardados en",
        output_dir / "favorita_consolidated.parquet",
    )
    print(f"Shape consolidado: filas={consolidated.height}, columnas={consolidated.width}")

    return "Datos transformados"


def cargar_datos():
    consolidated = consolidate_data()

    print("Cargando datos consolidados en PostgreSQL...")
    export_to_postgres(consolidated, table_name="favorita_consolidated")
    print("Carga a PostgreSQL completada.")

    return "Datos cargados"


def marcar_favorita():
    print("Generando y exportando reportes de EDA...")
    export_all_reports()
    print("Reportes exportados correctamente.")
    return "Reporte generado"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="favorita_pipeline",
    default_args=default_args,
    description="Pipeline de Airflow para procesar los datos de Favorita desde carga hasta reporte",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["favorita"],
) as dag:
    inicio = PythonOperator(
        task_id="inicio",
        python_callable=lambda: print("Inicio del DAG favorita_pipeline"),
    )

    extraer = PythonOperator(
        task_id="extraer_datos",
        python_callable=extraer_datos,
    )

    transformar = PythonOperator(
        task_id="transformar_datos",
        python_callable=transformar_datos,
    )

    cargar = PythonOperator(
        task_id="cargar_datos",
        python_callable=cargar_datos,
    )

    marcar = PythonOperator(
        task_id="marcar_favorita",
        python_callable=marcar_favorita,
    )

    fin = PythonOperator(
        task_id="fin",
        python_callable=lambda: print("DAG favorita_pipeline completado"),
    )

    inicio >> extraer >> transformar >> cargar >> marcar >> fin
