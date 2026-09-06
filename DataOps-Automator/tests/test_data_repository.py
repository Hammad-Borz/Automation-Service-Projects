def test_insert_and_count(repository, processed_frame) -> None:
    assert repository.insert_sales_data(processed_frame) == 3
    assert repository.count_sales_records() == 3
    assert len(repository.fetch_all_sales()) == 3


def test_duplicate_order_id_is_updated(repository, processed_frame) -> None:
    repository.insert_sales_data(processed_frame)
    updated = processed_frame.copy()
    updated.loc[0, "quantity"] = 5
    updated.loc[0, "revenue"] = 500.0
    repository.insert_sales_data(updated.iloc[[0]])
    assert repository.count_sales_records() == 3
    saved = repository.fetch_all_sales()
    assert saved.loc[saved["order_id"] == "A-1", "quantity"].iloc[0] == 5
    assert saved.loc[saved["order_id"] == "A-1", "revenue"].iloc[0] == 500.0
