import pytest

from src.data_validator import DataValidator
from src.exceptions import DataValidationError


REQUIRED_COLUMNS = (
    "order_id", "order_date", "customer", "region", "product",
    "category", "quantity", "unit_price",
)


def test_valid_data_passes(raw_frame) -> None:
    DataValidator(REQUIRED_COLUMNS).validate(raw_frame)


def test_missing_required_column_fails(raw_frame) -> None:
    with pytest.raises(DataValidationError, match="Missing required columns"):
        DataValidator(("order_id", "missing")).validate(raw_frame)


def test_invalid_quantity_fails(raw_frame) -> None:
    raw_frame.loc[0, "quantity"] = 0
    with pytest.raises(DataValidationError, match="quantity"):
        DataValidator(REQUIRED_COLUMNS).validate(raw_frame)


def test_invalid_price_fails(raw_frame) -> None:
    raw_frame["unit_price"] = raw_frame["unit_price"].astype(object)
    raw_frame.loc[0, "unit_price"] = "not-a-number"
    with pytest.raises(DataValidationError, match="unit_price"):
        DataValidator(REQUIRED_COLUMNS).validate(raw_frame)
