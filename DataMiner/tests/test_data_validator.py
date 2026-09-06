from data_validator import DataValidator


def test_valid_and_invalid_records_are_separated():
    records = [
        {"name": "Widget", "price": "$12", "category": "Tools", "availability": "In Stock"},
        {"name": "Broken", "price": "", "category": "Tools", "availability": "In Stock"},
        "not a record",
    ]
    result = DataValidator().validate_records(records)
    assert result.valid_records == [records[0]]
    assert len(result.invalid_records) == 2
    assert "Required field cannot be empty: price." in result.invalid_records[0]["errors"]


def test_missing_required_field_is_reported():
    result = DataValidator().validate_record({"name": "Widget"})
    assert not result.is_valid
    assert "Missing required field: price." in result.errors
