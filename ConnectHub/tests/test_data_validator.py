from data_validator import DataValidator


def test_validates_valid_records_and_reports_invalid_ones():
    records = [
        {"id": 1, "name": "Ada", "email": "ada@example.com"},
        {"id": 2, "name": "Missing Email"},
        "not-a-dictionary",
    ]

    result = DataValidator().validate_records(records)

    assert result.valid_records == [records[0]]
    assert len(result.invalid_records) == 2
    assert "Missing required field: email." in result.invalid_records[0]["errors"]
    assert result.invalid_records[1]["errors"] == ["Record must be a dictionary."]


def test_rejects_non_list_source_data():
    result = DataValidator().validate_records({"id": 1})

    assert result.valid_records == []
    assert result.invalid_records[0]["errors"] == ["Source data must be a list of dictionaries."]


def test_rejects_malformed_email():
    result = DataValidator().validate_record({"id": 1, "name": "Ada", "email": "not-an-email"})

    assert not result.is_valid
    assert "Email must be a valid email address." in result.errors
