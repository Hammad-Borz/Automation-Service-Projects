import pytest

from src.data_validator import DataValidator
from src.exceptions import DataValidationError


def test_valid_data_passes(sample_frame) -> None:
    DataValidator(tuple(sample_frame.columns)).validate(sample_frame)


def test_missing_column_fails(sample_frame) -> None:
    with pytest.raises(DataValidationError, match="Missing required columns"):
        DataValidator(("order_id", "missing")).validate(sample_frame)


def test_negative_quantity_fails(sample_frame) -> None:
    sample_frame.loc[0, "quantity"] = -1
    with pytest.raises(DataValidationError, match="quantity"):
        DataValidator(tuple(sample_frame.columns)).validate(sample_frame)
