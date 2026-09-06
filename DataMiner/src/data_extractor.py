"""Extract product-like records from controlled or compatible HTML."""

from __future__ import annotations

from typing import Any

from bs4 import BeautifulSoup, Tag


class DataExtractor:
    """Extract `.product-card` elements using documented CSS selectors."""

    CARD_SELECTOR = ".product-card"
    FIELD_SELECTORS = {
        "name": ".product-name",
        "price": ".product-price",
        "category": ".product-category",
        "availability": ".product-availability",
    }

    def extract(self, html: str) -> list[dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        records: list[dict[str, str]] = []
        for card in soup.select(self.CARD_SELECTOR):
            record = self._extract_card(card)
            if record is not None:
                records.append(record)
        return records

    def _extract_card(self, card: Tag) -> dict[str, str] | None:
        record: dict[str, str] = {}
        for field, selector in self.FIELD_SELECTORS.items():
            element = card.select_one(selector)
            if element is None:
                return None
            record[field] = element.get_text(" ", strip=True)
        return record
