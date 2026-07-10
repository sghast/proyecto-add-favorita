import polars as pl
from scripts.transform.consolidate_data import consolidate_data

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