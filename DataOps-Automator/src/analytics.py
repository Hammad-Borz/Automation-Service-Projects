"""SQL-backed business analytics."""

import pandas as pd

from .database_manager import DatabaseManager
from .models import AnalyticsResult


class Analytics:
    """Execute aggregate queries against the sales table."""

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def calculate(self) -> AnalyticsResult:
        with self.database.connection() as connection:
            kpi_row = connection.execute("""
                SELECT COALESCE(SUM(revenue), 0) AS total_revenue,
                       COUNT(DISTINCT order_id) AS total_orders,
                       COALESCE(AVG(revenue), 0) AS average_order_value,
                       COALESCE(SUM(quantity), 0) AS total_quantity_sold
                FROM sales
            """).fetchone()
            kpis = dict(kpi_row)
            kpis["total_revenue"] = round(float(kpis["total_revenue"]), 2)
            kpis["average_order_value"] = round(float(kpis["average_order_value"]), 2)
            queries = {
                "by_region": "SELECT region, SUM(revenue) AS revenue, COUNT(*) AS orders, SUM(quantity) AS quantity FROM sales GROUP BY region ORDER BY revenue DESC",
                "by_product": "SELECT product, SUM(revenue) AS revenue, COUNT(*) AS orders, SUM(quantity) AS quantity FROM sales GROUP BY product ORDER BY revenue DESC",
                "by_category": "SELECT category, SUM(revenue) AS revenue, COUNT(*) AS orders, SUM(quantity) AS quantity FROM sales GROUP BY category ORDER BY revenue DESC",
                "monthly": "SELECT month, SUM(revenue) AS revenue, COUNT(*) AS orders, SUM(quantity) AS quantity FROM sales GROUP BY month ORDER BY month",
                "top_products": "SELECT product, SUM(revenue) AS revenue, COUNT(*) AS orders, SUM(quantity) AS quantity FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 5",
            }
            tables = {name: pd.read_sql_query(query, connection) for name, query in queries.items()}
        return AnalyticsResult(kpis, tables["by_region"], tables["by_product"], tables["by_category"], tables["monthly"], tables["top_products"])
