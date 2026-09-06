"""Normalization of validated product records."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


class CleaningError(ValueError):
    """A record could not be safely cleaned."""


@dataclass(frozen=True)
class CleaningBatch:
    cleaned_records: list[dict[str, Any]]
    failed_records: list[dict[str, Any]]


class DataCleaner:
    """Clean whitespace, price, category, and availability values."""

    AVAILABILITY_MAP = {
        "in stock": "In Stock",
        "available": "In Stock",
        "out of stock": "Out of Stock",
        "unavailable": "Out of Stock",
        "pre-order": "Pre-Order",
        "preorder": "Pre-Order",
    }

    @staticmethod
    def _whitespace(value: Any) -> str:
        return " ".join(str(value).split())

    def clean_record(self, record: dict[str, Any]) -> dict[str, Any]:
        try:
            raw_price = self._whitespace(record["price"])
            price_text = re.sub(r"[^0-9,.-]", "", raw_price).replace(",", "")
            if not price_text or price_text in {".", "-", "-."}:
                raise CleaningError(f"Price cannot be converted to a number: {raw_price!r}.")
            price = float(price_text)
            return {
                "name": self._whitespace(record["name"]),
                "price": price,
                "category": self._whitespace(record["category"]).title(),
                "availability": self.AVAILABILITY_MAP.get(self._whitespace(record["availability"]).casefold(), self._whitespace(record["availability"]).title()),
            }
        except KeyError as exc:
            raise CleaningError(f"Cannot clean record; missing field: {exc.args[0]}.") from exc

    def clean_records(self, records: list[dict[str, Any]]) -> CleaningBatch:
        cleaned: list[dict[str, Any]] = []
        failed: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            try:
                cleaned.append(self.clean_record(record))
            except CleaningError as exc:
                failed.append({"index": index, "record": record, "error": str(exc)})
        return CleaningBatch(cleaned, failed)
