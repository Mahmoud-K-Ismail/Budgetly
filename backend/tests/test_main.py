import pytest
from fastapi.testclient import TestClient
from datetime import date
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "NYUAD Smart Budgeting Assistant" in data["message"]

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_user():
    """Test user creation"""
    user_data = {
        "stipend": 2000.0,
        "savings_goal": 300.0,
        "budget_cycle_start": "2025-01-01"
    }
    
    response = client.post("/api/user", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["stipend"] == 2000.0
    assert data["savings_goal"] == 300.0
    assert "id" in data

def test_create_expense():
    """Test expense creation"""
    # First create a user
    user_data = {
        "stipend": 2000.0,
        "savings_goal": 300.0,
        "budget_cycle_start": "2025-01-01"
    }
    user_response = client.post("/api/user", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create expense
    expense_data = {
        "user_id": user_id,
        "amount": 25.50,
        "category": "food",
        "description": "Lunch at cafeteria",
        "date": "2025-01-15"
    }
    
    response = client.post("/api/expenses", json=expense_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 25.50
    assert data["category"] == "food"
    assert data["user_id"] == user_id

def test_get_budget_summary():
    """Test budget summary endpoint"""
    # First create a user
    user_data = {
        "stipend": 2000.0,
        "savings_goal": 300.0,
        "budget_cycle_start": "2025-01-01"
    }
    user_response = client.post("/api/user", json=user_data)
    user_id = user_response.json()["id"]
    
    # Add some expenses
    expenses = [
        {"user_id": user_id, "amount": 25.50, "category": "food", "description": "Lunch", "date": "2025-01-15"},
        {"user_id": user_id, "amount": 15.00, "category": "transport", "description": "Bus fare", "date": "2025-01-15"}
    ]
    
    for expense in expenses:
        client.post("/api/expenses", json=expense)
    
    # Get budget summary
    response = client.get(f"/api/summary/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "stipend" in data
    assert "remaining_budget" in data
    assert "expenses_by_category" in data

def test_get_recommendations():
    """Test recommendations endpoint"""
    # First create a user
    user_data = {
        "stipend": 2000.0,
        "savings_goal": 300.0,
        "budget_cycle_start": "2025-01-01"
    }
    user_response = client.post("/api/user", json=user_data)
    user_id = user_response.json()["id"]
    
    # Get recommendations
    response = client.get(f"/api/recommendations/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_expense_categories():
    """Test getting expense categories"""
    response = client.get("/api/expenses/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_invalid_user_id():
    """Test handling of invalid user ID"""
    response = client.get("/api/user/99999")
    assert response.status_code == 404
    
    response = client.get("/api/summary/99999")
    assert response.status_code == 404

def test_invalid_expense_data():
    """Test handling of invalid expense data"""
    expense_data = {
        "user_id": 1,
        "amount": -10,  # Invalid negative amount
        "category": "food",
        "date": "2025-01-15"
    }
    
    response = client.post("/api/expenses", json=expense_data)
    assert response.status_code == 422  # Validation error 