import polars as pl
from scripts.transform.consolidate_data import consolidate_data
from pathlib import Path

# ventas por familia de producto
def sales_by_family(df):
    return (
        df.group_by("family").agg(
            pl.col("sales").sum().alias("total_sales")
        ).sort("total_sales", descending=True)
    )

# top 10 tiendas con mayor venta
def top_10_stores(df):
    return (
        df.group_by(["store_nbr", "city", "state"]).agg(
            pl.col("sales").sum().alias("total_sales")
        ).sort("total_sales", descending=True).head(10)
    )

# bottom (peores) 10 tiendas con menor venta
def bottom_10_stores(df):
    return (
        df.group_by(["store_nbr", "city", "state"]).agg(
            pl.col("sales").sum().alias("total_sales")
        ).sort("total_sales").head(10)
    )

# ventas promedio por ciudad
def sales_by_city(df):
    return (
        df.group_by("city").agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort("average_sales", descending=True)
    )

# ventas promedio por provincia
def sales_by_state(df):
    return (
        df.group_by("state").agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort("average_sales", descending=True)
    )


# evolución mensual de ventas
def monthly_sales(df):
    return (
        df.with_columns(
            pl.col("date").dt.year().alias("year"),
            pl.col("date").dt.month().alias("month")
        ).group_by(["year", "month"]).agg(
            pl.col("sales").sum().alias("total_sales")
        ).sort(["year", "month"])
    )

# evolución anual de ventas
def yearly_sales(df):
    return (
        df.with_columns(
            pl.col("date").dt.year().alias("year")
        ).group_by("year").agg(
            pl.col("sales").sum().alias("total_sales")
        ).sort("year")
    )

# impacto de feriados nacionales
def holiday_sales(df):
    return (
        df.group_by("type_right").agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort("average_sales", descending=True)
    )

# ventas antes y después de los feriados
def holiday_sales_before_after(df):
    return (
        df.filter(
            pl.col("type_right").is_not_null()
        ).group_by("family").agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort("average_sales", descending=True)
    )

# comparación de ventas con y sin promoción
def promotion_sales(df):
    return (
        df.group_by("onpromotion").agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort("onpromotion")
    )

# efecto de las promociones por familia
def promotion_by_family(df):
    return (
        df.group_by(["family", "onpromotion"]).agg(
            pl.col("sales").mean().alias("average_sales")
        ).sort(["family", "onpromotion"])
    )

# ventas mensuales y precio del petróleo
def oil_sales(df):
    return (
        df.with_columns(
            pl.col("date").dt.year().alias("year"),
            pl.col("date").dt.month().alias("month")
        ).group_by(["year", "month"]).agg(
            pl.col("sales").sum().alias("total_sales"),
            pl.col("dcoilwtico").mean().alias("average_oil_price")
        ).sort(["year", "month"])
    )

# relación entre ventas y transacciones por tienda
def sales_transactions(df):
    return (
        df.group_by(["store_nbr", "city"]).agg(
            pl.col("sales").sum().alias("total_sales"),
            pl.col("transactions").sum().alias("total_transactions")
        ).sort("total_sales", descending=True)
    )

# ticket promedio por tienda
def average_ticket(df):
    return (
        df.group_by(["store_nbr", "city"]).agg(
            pl.col("sales").sum().alias("total_sales"),
            pl.col("transactions").sum().alias("total_transactions")
        ).with_columns(
            (
                pl.col("total_sales") /
                pl.col("total_transactions")
            ).alias("average_ticket")
        ).sort("average_ticket", descending=True)
    )

# ejecución del EDA profundo con sus funciones y generación de reportes
def generate_reports():
    df = consolidate_data()
    reports = {
        "sales_by_family": sales_by_family(df),
        "top_10_stores": top_10_stores(df),
        "bottom_10_stores": bottom_10_stores(df),
        "sales_by_city": sales_by_city(df),
        "sales_by_state": sales_by_state(df),
        "monthly_sales": monthly_sales(df),
        "yearly_sales": yearly_sales(df),
        "holiday_sales": holiday_sales(df),
        "holiday_sales_before_after": holiday_sales_before_after(df),
        "promotion_sales": promotion_sales(df),
        "promotion_by_family": promotion_by_family(df),
        "oil_sales": oil_sales(df),
        "sales_transactions": sales_transactions(df),
        "average_ticket": average_ticket(df)
    }

    return reports

# guardar reportes en csv
def save_reports(reports):
    Path("reports").mkdir(exist_ok=True)
    for name, dataframe in reports.items():
        dataframe.write_csv(
            f"reports/{name}.csv"
        )
    print("Reportes guardados correctamente.")

# ejecución del script
if __name__ == "__main__":
    reports = generate_reports()
    save_reports(reports)
    for name in reports:
        print(f"{name}.csv generado")
    print(f"\n{len(reports)} reportes generados y guardados en /reports con éxito")
    print("\nEDA profundo completado correctamente\n")