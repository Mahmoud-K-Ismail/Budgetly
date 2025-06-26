#!/usr/bin/env python3
"""
Simple test script to verify the NYUAD Budgetly API is working
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🧪 Testing NYUAD Budgetly API...")
    
    # Test health check
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on http://localhost:8000")
        return
    
    # Test user creation
    print("\n👤 Testing user creation...")
    user_data = {
        "stipend": 2000.0,
        "savings_goal": 300.0,
        "budget_cycle_start": "2025-01-01"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/user", json=user_data)
        if response.status_code == 201:
            user = response.json()
            user_id = user["id"]
            print(f"✅ User created with ID: {user_id}")
        else:
            print(f"❌ User creation failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return
    
    # Test expense creation
    print("\n💰 Testing expense creation...")
    expense_data = {
        "user_id": user_id,
        "amount": 25.50,
        "category": "food",
        "description": "Lunch at cafeteria",
        "expense_date": "2025-01-15"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data)
        if response.status_code == 201:
            expense = response.json()
            print(f"✅ Expense created with ID: {expense['id']}")
        else:
            print(f"❌ Expense creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Expense creation error: {e}")
    
    # Test budget summary
    print("\n📊 Testing budget summary...")
    try:
        response = requests.get(f"{BASE_URL}/summary/{user_id}")
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Budget summary retrieved")
            print(f"   - Stipend: ${summary['stipend']}")
            print(f"   - Total Expenses: ${summary['total_expenses']}")
            print(f"   - Remaining Budget: ${summary['remaining_budget']}")
        else:
            print(f"❌ Budget summary failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Budget summary error: {e}")
    
    # Test recommendations
    print("\n💡 Testing recommendations...")
    try:
        response = requests.get(f"{BASE_URL}/recommendations/{user_id}")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ Retrieved {len(recommendations)} recommendations")
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"   {i}. {rec['message']}")
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Recommendations error: {e}")
    
    # Test expense history
    print("\n📝 Testing expense history...")
    try:
        response = requests.get(f"{BASE_URL}/expenses?user_id={user_id}")
        if response.status_code == 200:
            expenses = response.json()
            print(f"✅ Retrieved {len(expenses)} expenses")
        else:
            print(f"❌ Expense history failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Expense history error: {e}")
    
    print("\n🎉 API test completed!")

if __name__ == "__main__":
    test_api() 