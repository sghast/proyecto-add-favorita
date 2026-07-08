import polars as pl
from scripts.load.load_data import load_all_data

def clean_all_data():
    datasets = load_all_data()

    train = datasets["train"].unique()
    train = train.with_columns(
        pl.col("date").str.to_date()
    )

    stores = datasets["stores"].unique()

    transactions = datasets["transactions"].unique()
    transactions = transactions.with_columns(
        pl.col("date").str.to_date()
    )

    oil = datasets["oil"].unique()
    oil = oil.with_columns(
        pl.col("date").str.to_date(),
        pl.col("dcoilwtico").interpolate()
    )

    holidays = datasets["holidays"].unique()
    holidays = holidays.with_columns(
        pl.col("date").str.to_date()
    )

    return {
        "train": train,
        "stores": stores,
        "transactions": transactions,
        "oil": oil,
        "holidays_events": holidays
    }
if __name__ == "__main__":
    datasets = clean_all_data()
    for name, df in datasets.items():
        print(name, df.shape)