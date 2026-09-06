"""Validated domain models used across DocuMind."""

from pydantic import BaseModel, Field, field_validator


class DocumentAnalysis(BaseModel):
    """Structured analysis returned by the AI provider."""

    summary: str = Field(min_length=1, description="Concise document summary")
    key_points: list[str] = Field(min_length=1, description="Important document points")
    action_items: list[str] = Field(default_factory=list, description="Recommended actions")
    document_category: str = Field(min_length=1, description="Document classification")

    @field_validator("summary", "document_category")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("key_points", "action_items")
    @classmethod
    def items_must_not_be_blank(cls, value: list[str]) -> list[str]:
        cleaned = [item.strip() for item in value if isinstance(item, str) and item.strip()]
        if len(cleaned) != len(value):
            raise ValueError("items must be non-blank strings")
        return cleaned
