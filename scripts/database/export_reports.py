# | ========== Genera los reportes y los exporta a la base de datos ================ |

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.eda.eda_deep import generate_reports
from scripts.database.export_postgres import export_to_postgres

def export_all_reports():
    # generar todos los reportes del eda profundo y exportar a postgres

    print("\nGenerando reportes del EDA profundo...")

    reports = generate_reports()

    print(f"\nSe generaron {len(reports)} reportes\n")

    for table_name, dataframe in reports.items():

        print(f"Exportando '{table_name}'...")

        export_to_postgres(
            df=dataframe,
            table_name=table_name
        )

    print("\nTodos los reportes fueron exportados correctamente\n")

if __name__ == "__main__":
    export_all_reports()