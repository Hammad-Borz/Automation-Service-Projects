from data_cleaner import DataCleaner


def test_cleans_whitespace_price_category_and_availability():
    result = DataCleaner().clean_record({"name": "  Blue   Widget ", "price": " USD 1,250.50 ", "category": " home goods ", "availability": " available "})
    assert result == {"name": "Blue Widget", "price": 1250.5, "category": "Home Goods", "availability": "In Stock"}


def test_bad_prices_are_retained_as_cleaning_failures():
    record = {"name": "Widget", "price": "free", "category": "Tools", "availability": "In Stock"}
    batch = DataCleaner().clean_records([record])
    assert batch.cleaned_records == []
    assert batch.failed_records[0]["record"] == record
    assert "cannot be converted" in batch.failed_records[0]["error"]
