
#  | ===== EDA PROFUNDO 

import polars as pl
from scripts.transform.consolidate_data import consolidate_data
from pathlib import Path
from datetime import timedelta

# VENTAS GENERALES
# Distribución de ventas por familia de producto
def sales_by_family(df):
    return (
        df.group_by("family")
        .agg(pl.col("sales").sum().alias("total_sales"))
        .sort("total_sales", descending=True)
    )

# Ventas totales por tienda y ranking de las 10 tiendas con mayor y menor venta
def stores_ranking(df):
    store_sales = (
        df.group_by(["store_nbr", "city", "state"])
        .agg(pl.col("sales").sum().alias("total_sales"))
    )

    top_10 = (
        store_sales.sort("total_sales", descending=True)
        .head(10)
        .with_columns(pl.lit("top_10").alias("ranking"))
    )

    bottom_10 = (
        store_sales.sort("total_sales")
        .head(10)
        .with_columns(pl.lit("bottom_10").alias("ranking"))
    )

    return pl.concat([top_10, bottom_10], how="vertical_relaxed")

#Ventas promedio por ciudad y provincia
def sales_by_city(df):
    return (
        df.group_by("city")
        .agg(pl.col("sales").mean().alias("average_sales"))
        .sort("average_sales", descending=True)
    )

def sales_by_state(df):
    return (
        df.group_by("state")
        .agg(pl.col("sales").mean().alias("average_sales"))
        .sort("average_sales", descending=True)
    )

# Evolución temporal de ventas
def monthly_sales(df):
    return (
        df.with_columns(
            pl.col("date").dt.year().alias("year"),
            pl.col("date").dt.month().alias("month"),
        ).group_by(["year", "month"])
        .agg(pl.col("sales").sum().alias("total_sales"))
        .sort(["year", "month"])
    )

def yearly_sales(df):
    return (
        df.with_columns(pl.col("date").dt.year().alias("year"))
        .group_by("year")
        .agg(pl.col("sales").sum().alias("total_sales"))
        .sort("year")
    )

# ESTACIONALIDAD Y FERIADOS
# Impacto de feriados nacionales en el volumen de ventas
def holiday_sales(df):
    return (
        df.with_columns(
            pl.when(pl.col("type_right") == "Holiday")
            .then(pl.lit("Holiday"))
            .otherwise(pl.lit("Normal"))
            .alias("day_type")
        ).group_by("day_type")
        .agg(pl.col("sales").mean().alias("average_sales"))
        .sort("day_type")
    )

# Ventas en los tres días previos y posteriores a feriados nacionales por familia de producto
def holiday_sales_before_after(df):
    holiday_dates = (
        df.filter(pl.col("type_right") == "Holiday")
        .select("date")
        .unique()
        .to_series()
        .to_list()
    )

    before_dates = []
    after_dates = []

    for holiday in holiday_dates:
        before_dates.extend([
            holiday - timedelta(days=3),
            holiday - timedelta(days=2),
            holiday - timedelta(days=1)
        ])

        after_dates.extend([
            holiday + timedelta(days=1),
            holiday + timedelta(days=2),
            holiday + timedelta(days=3)
        ])

    return (
        df.with_columns(
            pl.when(pl.col("date").is_in(before_dates))
            .then(pl.lit("Antes"))
            .when(pl.col("type_right") == "Holiday")
            .then(pl.lit("Feriado"))
            .when(pl.col("date").is_in(after_dates))
            .then(pl.lit("Después"))
            .otherwise(None)
            .alias("period")
        ).filter(
            pl.col("period").is_not_null()
        ).group_by(["period", "family"])
        .agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort(["period", "average_sales"], descending=[False, True])
    )

# PROMOCIONES
# Comparación de ventas con y sin promoción por familia de producto
def promotion_by_family(df):
    return (
        df.with_columns(
            pl.when(pl.col("onpromotion") > 0)
            .then(pl.lit("Con promoción"))
            .otherwise(pl.lit("Sin promoción"))
            .alias("promotion")
        ).group_by(["family", "promotion"])
        .agg(pl.col("sales").mean().alias("average_sales"))
        .sort(["family", "promotion"])
    )

# PETRÓLEO Y ECONOMÍA
# Correlación entre precio del petróleo y ventas totales mensuales
def oil_sales(df):
    return (
        df.with_columns(
            pl.col("date").dt.year().alias("year"),
            pl.col("date").dt.month().alias("month"),
        ).group_by(["year", "month"])
        .agg(
            pl.col("sales").sum().alias("total_sales"),
            pl.col("dcoilwtico").mean().alias("average_oil_price"),
        ).sort(["year", "month"])
    )

# Identificación del lag temporal entre caída del petróleo y caída en ventas (2015-2016)
def oil_lag(df):
    return (
        df.filter((pl.col("date").dt.year() >= 2015) & (pl.col("date").dt.year() <= 2016))
        .with_columns(
            pl.col("date").dt.year().alias("year"),
            pl.col("date").dt.month().alias("month"),
        ).group_by(["year", "month"])
        .agg(
            pl.col("sales").sum().alias("total_sales"),
            pl.col("dcoilwtico").mean().alias("average_oil_price"),
        ).sort(["year", "month"])
    )

# Ciudades que mostraron mayor sensibilidad a la caída del petróleo
def oil_city_sensitivity(df):
    return (
        df.group_by("city").agg(
            pl.col("sales").mean().alias("average_sales"),
            pl.col("dcoilwtico").mean().alias("average_oil_price"),
        ).sort("average_oil_price")
    )

# TRANSACCIONES
# Relación entre número de transacciones, volumen de ventas y ticket promedio por tienda
def sales_transactions_ticket(df):
    return (
        df.group_by(["store_nbr", "city"]).agg(
            pl.col("sales").sum().alias("total_sales"),
            pl.col("transactions").sum().alias("total_transactions"),
        ).with_columns(
            pl.when(pl.col("total_transactions") > 0)
            .then(
                pl.col("total_sales") /
                pl.col("total_transactions")
            ).otherwise(0)
            .alias("average_ticket")
        ).with_columns(
            pl.when(
                pl.col("average_ticket") >=
                pl.col("average_ticket").mean()
            ).then(pl.lit("ticket_alto"))
            .otherwise(pl.lit("ticket_bajo"))
            .alias("ticket_group")
        ).sort("total_sales", descending=True)
    )

# GENERACIÓN DE REPORTES
# Generar todos los reportes del EDA profundo
def generate_reports():
    df = consolidate_data()

    reports = {
        "sales_by_family": sales_by_family(df),
        "stores_ranking": stores_ranking(df),
        "sales_by_city": sales_by_city(df),
        "sales_by_state": sales_by_state(df),
        "monthly_sales": monthly_sales(df),
        "yearly_sales": yearly_sales(df),
        "holiday_sales": holiday_sales(df),
        "holiday_sales_before_after": holiday_sales_before_after(df),
        "promotion_by_family": promotion_by_family(df),
        "oil_sales": oil_sales(df),
        "oil_lag": oil_lag(df),
        "oil_city_sensitivity": oil_city_sensitivity(df),
        "sales_transactions_ticket": sales_transactions_ticket(df),
    }

    return reports

# Guardar los reportes generados en archivos csv
def save_reports(reports):
    Path("reports").mkdir(exist_ok=True)
    for name, dataframe in reports.items():
        dataframe.write_csv(f"reports/{name}.csv")
    print("Reportes guardados correctamente.")

if __name__ == "__main__":
    reports = generate_reports()
    save_reports(reports)
    print("\nReportes generados:\n")
    for name in reports:
        print(f"- {name}.csv")

    print(f"\n{len(reports)} reportes generados y guardados en /reports con éxito")
    print("\nEDA profundo completado correctamente\n")