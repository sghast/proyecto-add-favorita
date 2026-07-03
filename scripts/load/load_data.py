# scripts/load/load_data.py

import polars as pl
from pathlib import Path

DATA_PATH = Path("data")

def load_csv(filename: str) -> pl.DataFrame:
    file_path = DATA_PATH / filename
    if not file_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {file_path}"
        )
    return pl.read_csv(file_path)

def load_all_data() -> dict:

    datasets = {
        "train": load_csv("train.csv"),
        "stores": load_csv("stores.csv"),
        "transactions": load_csv("transactions.csv"),
        "oil": load_csv("oil.csv"),
        "holidays": load_csv("holidays_events.csv")
    }

    return datasets

def print_summary(datasets: dict) -> None:

    print("\n========== DATASETS CARGADOS ==========\n")
    for name, df in datasets.items():
        print(f"{name.upper()}")
        print(f"Filas: {df.height}")
        print(f"Columnas: {df.width}")
        print(f"Shape: {df.shape}")
        print("-" * 40)

if __name__ == "__main__":
    try:
        datasets = load_all_data()
        print_summary(datasets)

        print("\nCarga completada correctamente.")
    except Exception as e:
        print(f"\nError: {e}")