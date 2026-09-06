import pytest

from src.result_validator import ResultValidationError, validate_analysis


def test_validates_complete_analysis() -> None:
    analysis = validate_analysis({"summary": "Summary", "key_points": ["Point"], "action_items": ["Do it"], "document_category": "Invoice"})
    assert analysis.key_points == ["Point"]


@pytest.mark.parametrize("raw", ["not json", {"summary": "", "key_points": [], "document_category": ""}])
def test_rejects_invalid_analysis(raw: object) -> None:
    with pytest.raises(ResultValidationError):
        validate_analysis(raw)  # type: ignore[arg-type]
