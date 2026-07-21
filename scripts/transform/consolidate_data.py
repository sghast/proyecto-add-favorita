
# | ========= Se realiza Joins de todos los Datasets ============= | 
# En este caso de hace left join para que todos los datos estén en el dataset train


import polars as pl
from scripts.cleaning.clean_data import clean_all_data

def consolidate_data():
    # carga de los datasets limpios
    datasets = clean_all_data()
    
    train = datasets["train"]
    stores = datasets["stores"]
    transactions = datasets["transactions"]
    oil = datasets["oil"]
    holidays = datasets["holidays_events"]

    # joins
    df = train.join(
        stores,
        on="store_nbr",
        how="left"
    )

    df = df.join(
        transactions,
        on=["store_nbr", "date"],
        how="left"
    )

    df = df.join(
        oil,
        on="date",
        how="left"
    )

    df = df.join(
        holidays,
        on="date",
        how="left"
    )

    return df


if __name__ == "__main__":
    df = consolidate_data()
    print(df.shape)
    print(df.head())