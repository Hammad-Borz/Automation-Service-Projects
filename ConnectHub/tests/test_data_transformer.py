import pytest

from data_transformer import DataTransformer, TransformationError


def test_transforms_source_record_to_destination_schema():
    record = {"id": 42, "name": "Ada Lovelace", "email": "ada@example.com"}

    assert DataTransformer().transform(record) == {
        "external_id": 42,
        "full_name": "Ada Lovelace",
        "contact_email": "ada@example.com",
    }


def test_missing_field_cannot_be_transformed():
    with pytest.raises(TransformationError, match="email"):
        DataTransformer().transform({"id": 1, "name": "Ada"})
