from __future__ import annotations

import pytest

from src.core.validation import BusinessRequestInput, CustomerInput, OrderInput, validate_request_id


def test_valid_customer():
    customer = CustomerInput(name="Jane Doe", email="jane@example.com", phone="+123456789", company="Acme")
    assert customer.email == "jane@example.com"


def test_invalid_email():
    with pytest.raises(ValueError):
        CustomerInput(name="Jane Doe", email="bad-email", phone="+123456789", company="Acme")


def test_empty_name():
    with pytest.raises(ValueError):
        CustomerInput(name="", email="jane@example.com", phone="+123456789", company="Acme")


def test_negative_quantity():
    with pytest.raises(ValueError):
        OrderInput(product="Widget", category="software", quantity=-1, unit_price=10, source="website")


def test_negative_price():
    with pytest.raises(ValueError):
        OrderInput(product="Widget", category="software", quantity=2, unit_price=-10, source="website")


def test_valid_request_id():
    assert validate_request_id("REQ-1001") == "REQ-1001"


def test_invalid_request_id():
    with pytest.raises(ValueError):
        validate_request_id("bad")


def test_business_request_initialization():
    payload = BusinessRequestInput(
        request_id="REQ-2001",
        customer={"name": "John Smith", "email": "john@example.com", "phone": "+123456789", "company": "Example Corp"},
        order={"product": "Automation Package", "category": "software", "quantity": 5, "unit_price": 1500, "source": "website"},
    )
    assert payload.order.quantity == 5
    assert payload.customer.email == "john@example.com"
