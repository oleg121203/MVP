import pytest
from fastapi.testclient import TestClient
from src.ventai.backend.main import app

client = TestClient(app)

def test_add_price_data():
    """Test adding price data"""
    response = client.post(
        "/api/v1/pricing/prices",
        params={"supplier_id": "supplier1", "product_id": "product1", "price": 100.0}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_price_trends():
    """Test getting price trends"""
    # First add some data
    client.post(
        "/api/v1/pricing/prices",
        params={"supplier_id": "supplier1", "product_id": "product1", "price": 100.0}
    )
    
    response = client.get("/api/v1/pricing/trends/product1")
    assert response.status_code == 200
    assert "current_price" in response.json()

def test_get_recommendations():
    """Test getting recommendations"""
    # Add sufficient price data points for trend analysis
    for i in range(10):
        client.post(
            "/api/v1/pricing/prices",
            params={"supplier_id": "supplier1", "product_id": "product1", "price": 120.0 + i}
        )
        client.post(
            "/api/v1/pricing/prices",
            params={"supplier_id": "supplier2", "product_id": "product1", "price": 100.0}
        )
    
    response = client.get("/api/v1/pricing/recommendations", params={"product_ids": "product1"})
    assert response.status_code == 200
    result = response.json()
    assert "product1" in result
    assert isinstance(result["product1"]["recommendation"], str)
    assert isinstance(result["product1"].get("potential_savings"), (float, type(None)))
