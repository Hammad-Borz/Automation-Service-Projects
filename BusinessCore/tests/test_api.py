from __future__ import annotations

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_workflow_process_endpoint():
    payload = {
        "request_id": "REQ-API-1",
        "customer": {"name": "API Customer", "email": "api@example.com", "phone": "+123", "company": "API Co"},
        "order": {"product": "API Package", "category": "software", "quantity": 2, "unit_price": 500, "source": "website"},
    }
    response = client.post("/api/v1/workflows/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["order_id"]


def test_customer_list_endpoint():
    response = client.get("/api/v1/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_orders_endpoint():
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_analytics_endpoint():
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_customers" in data
    assert "total_orders" in data


def test_reports_endpoint():
    response = client.post("/api/v1/reports/generate")
    assert response.status_code == 200
    data = response.json()
    assert "report_file" in data
