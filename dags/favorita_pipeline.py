import sys
from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(_file_).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.load.load_data import load_all_data
from scripts.eda.eda_initial import generate_eda_initial
from scripts.cleaning.clean_data import clean_all_data
from scripts.transform.consolidate_data import consolidate_data
from scripts.eda.eda_deep import generate_reports
from scripts.database.export_postgres import export_to_postgres
from scripts.database.export_reports import export_all_reports

# carga de datos
def extraer_datos():
    datasets = load_all_data()
    print("\n========== CARGA DE DATOS ==========\n")
    print("Extrayendo datos de Favorita:")
    for name, df in datasets.items():
        print(f"- {name}: filas={df.height}, columnas={df.width}")
    return "Datos extraídos"

# eda inicial
def eda_inicial():
    print("\n========== EDA INICIAL ==========\n")
    generate_eda_initial()
    print("EDA inicial generado correctamente.")
    return "EDA inicial completado"

# limpieza de datos
def limpiar_datos():
    datasets = clean_all_data()
    print("\n========== LIMPIEZA ==========\n")
    for name, df in datasets.items():
        print(f"{name}: {df.shape}")
    return "Datos limpios"

# consolidación de datos
def consolidar():
    consolidated = consolidate_data()
    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    consolidated.write_parquet(
        output_dir / "favorita_consolidated.parquet"
    )
    print("\n========== CONSOLIDACIÓN ==========\n")
    print(f"Shape: {consolidated.shape}")
    return "Datos consolidados"

# eda profundo
def eda_profundo():
    reports = generate_reports()
    print("\n========== EDA PROFUNDO ==========\n")
    print(f"Se generaron {len(reports)} reportes.")
    return "EDA profundo completado"

# exportación a postgresql
def exportar_postgres():
    consolidated = consolidate_data()
    print("\n========== EXPORTACIÓN ==========\n")
    export_to_postgres(
        consolidated,
        table_name="favorita_consolidated"
    )
    export_all_reports()
    print("Datos y reportes exportados correctamente.")
    return "Exportación finalizada"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="favorita_pipeline",
    description="Pipeline ETL Proyecto Favorita",
    default_args=default_args,
    start_date=datetime(2026, 6, 25),
    schedule=None,
    catchup=False,
    tags=["favorita"]
) as dag:
    inicio = PythonOperator(
        task_id="inicio",
        python_callable=lambda: print("Inicio del pipeline")
    )
    extraer = PythonOperator(
        task_id="extraer_datos",
        python_callable=extraer_datos
    )
    eda = PythonOperator(
        task_id="eda_inicial",
        python_callable=eda_inicial
    )
    limpiar = PythonOperator(
        task_id="limpiar_datos",
        python_callable=limpiar_datos
    )
    consolidar_task = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar
    )
    eda_profundo_task = PythonOperator(
        task_id="eda_profundo",
        python_callable=eda_profundo
    )
    exportar = PythonOperator(
        task_id="exportar_postgres",
        python_callable=exportar_postgres
    )
    fin = PythonOperator(
        task_id="fin",
        python_callable=lambda: print("DAG favorita_pipeline completado")
    )

    inicio >> extraer >> eda >> limpiar >> consolidar_task >> eda_profundo_task >> exportar >> fin