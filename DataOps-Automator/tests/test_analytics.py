from src.analytics import Analytics


def test_sql_analytics_kpis_and_groupings(repository, processed_frame) -> None:
    repository.insert_sales_data(processed_frame)
    result = Analytics(repository.database).calculate()
    assert result.kpis == {"total_revenue": 600.0, "total_orders": 3, "average_order_value": 200.0, "total_quantity_sold": 6}
    assert result.by_region.iloc[0]["region"] == "North"
    assert result.by_product.iloc[0]["product"] == "Suite"
    assert result.top_products.iloc[0]["revenue"] == 450.0
