from __future__ import annotations

from src.core.workflow_engine import process_business_request


def test_successful_workflow():
    result = process_business_request({
        "request_id": "REQ-101",
        "customer": {"name": "Alice Smith", "email": "alice@example.com", "phone": "+111", "company": "Alpha"},
        "order": {"product": "ERP Kit", "category": "software", "quantity": 4, "unit_price": 1500, "source": "website"},
    })
    assert result["success"] is True
    assert result["customer_id"] is not None
    assert result["order_id"] is not None
    assert result["order_status"] in {"pending", "processing", "completed"}


def test_customer_creation_during_workflow():
    result = process_business_request({
        "request_id": "REQ-102",
        "customer": {"name": "Bob Jones", "email": "bob@example.com", "phone": "+222", "company": "Beta"},
        "order": {"product": "Cloud Setup", "category": "services", "quantity": 3, "unit_price": 500, "source": "sales"},
    })
    assert result["customer_id"] is not None
    assert result["created_task_ids"]


def test_existing_customer_workflow():
    first = process_business_request({
        "request_id": "REQ-103",
        "customer": {"name": "Carol Stone", "email": "carol@example.com", "phone": "+333", "company": "Gamma"},
        "order": {"product": "New Package", "category": "software", "quantity": 5, "unit_price": 1000, "source": "website"},
    })
    second = process_business_request({
        "request_id": "REQ-104",
        "customer": {"name": "Carol Stone", "email": "carol@example.com", "phone": "+333", "company": "Gamma"},
        "order": {"product": "Second Package", "category": "software", "quantity": 2, "unit_price": 1000, "source": "website"},
    })
    assert first["customer_id"] == second["customer_id"]
    assert second["success"] is True


def test_blocked_customer_workflow():
    result = process_business_request({
        "request_id": "REQ-105",
        "customer": {"name": "Blocked User", "email": "blocked@example.com", "phone": "+444", "company": "Blocked Inc"},
        "order": {"product": "Bad Order", "category": "software", "quantity": 2, "unit_price": 1000, "source": "website"},
    })
    assert result["success"] is False
    assert result["order_status"] == "cancelled"


def test_idempotent_repeated_request():
    payload = {
        "request_id": "REQ-106",
        "customer": {"name": "Repeat User", "email": "repeat@example.com", "phone": "+555", "company": "Repeat Corp"},
        "order": {"product": "Repeat Pack", "category": "software", "quantity": 3, "unit_price": 800, "source": "website"},
    }
    first = process_business_request(payload)
    second = process_business_request(payload)
    assert first["workflow_id"] == second["workflow_id"]
    assert second["success"] is True


def test_workflow_failure():
    result = process_business_request({
        "request_id": "REQ-107",
        "customer": {"name": "Bad Customer", "email": "bad@example.com", "phone": "+666", "company": "None"},
        "order": {"product": "Broken Order", "category": "software", "quantity": 0, "unit_price": 100, "source": "website"},
    })
    assert result["success"] is False
    assert result["errors"]
