from scripts.load.load_data import load_all_data
import json
from pathlib import Path

datasets = load_all_data()

report = {}

for name, df in datasets.items():

    info = {
        "filas": df.height,
        "columnas": df.width,
        "nulos": int(df.null_count().sum_horizontal().item()),
        "duplicados": int(df.is_duplicated().sum()),
        "tipos_datos": {
            col: str(dtype)
            for col, dtype in df.schema.items()
        }
    }

    if "date" in df.columns:
        info["fecha_min"] = str(df["date"].min())
        info["fecha_max"] = str(df["date"].max())

    report[name] = info

Path("reports").mkdir(exist_ok=True)

with open("reports/eda_initial.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=4, ensure_ascii=False)

print("EDA inicial completado (generado con éxito). Reporte guardado en reports/eda_initial.json.")