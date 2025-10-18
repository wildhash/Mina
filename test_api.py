"""
Tests for Mina API Server

Basic tests for the FastAPI server endpoints.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi.testclient import TestClient
    from api_server import app
    from mina_agent import MinaAgent
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not installed. Install with: pip install -r requirements.txt")


# Create a test client with lifespan context
def get_test_client():
    """Get a test client with proper initialization."""
    client = TestClient(app)
    # Manually initialize the agent since TestClient doesn't trigger lifespan
    if not hasattr(app.state, 'agent'):
        app.state.agent = MinaAgent()
    return client


def test_fastapi_available():
    """Test that FastAPI is available."""
    assert FASTAPI_AVAILABLE, "FastAPI must be installed to run API tests"


def test_root_endpoint():
    """Test root endpoint."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    response = client.get("/api/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "integrations" in data
    assert "claude" in data["integrations"]
    assert "browser_use" in data["integrations"]
    assert "daytona" in data["integrations"]


def test_search_endpoint_valid():
    """Test search endpoint with valid data."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    
    search_data = {
        "category": "laptop",
        "budget_max": 3000,
        "priorities": ["Performance", "Battery Life"],
        "specific_needs": "For software development"
    }
    
    response = client.post("/api/search", json=search_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "total_products_analyzed" in data
    assert "search_time_seconds" in data
    assert len(data["recommendations"]) > 0
    
    # Check recommendation structure
    rec = data["recommendations"][0]
    assert "product" in rec
    assert "confidence_score" in rec
    assert "reasoning" in rec
    assert "pros" in rec
    assert "cons" in rec
    
    # Check product structure
    product = rec["product"]
    assert "name" in product
    assert "price" in product
    assert "retailer" in product
    assert "url" in product
    assert "specs" in product
    assert "reviews_summary" in product
    assert "rating" in product


def test_search_endpoint_invalid_category():
    """Test search endpoint with invalid category."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    
    search_data = {
        "category": "invalid_category",
        "budget_max": 3000,
        "priorities": ["Performance"],
        "specific_needs": ""
    }
    
    response = client.post("/api/search", json=search_data)
    
    assert response.status_code == 400


def test_search_endpoint_low_budget():
    """Test search endpoint with budget below minimum."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    
    search_data = {
        "category": "laptop",
        "budget_max": 100,  # Below $500 minimum
        "priorities": ["Performance"],
        "specific_needs": ""
    }
    
    response = client.post("/api/search", json=search_data)
    
    # Should fail validation
    assert response.status_code == 422


def test_search_endpoint_furniture():
    """Test search endpoint with furniture category."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    
    search_data = {
        "category": "furniture",
        "budget_max": 2000,
        "priorities": ["Durability", "Comfort"],
        "specific_needs": "Ergonomic office chair"
    }
    
    response = client.post("/api/search", json=search_data)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) > 0


def test_search_endpoint_appliance():
    """Test search endpoint with appliance category."""
    if not FASTAPI_AVAILABLE:
        print("Skipping test - FastAPI not available")
        return
    
    client = get_test_client()
    
    search_data = {
        "category": "appliance",
        "budget_max": 1500,
        "priorities": ["Energy Efficiency", "Capacity"],
        "specific_needs": ""
    }
    
    response = client.post("/api/search", json=search_data)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) > 0


if __name__ == "__main__":
    # Run tests
    print("Running Mina API Server Tests...\n")
    
    tests = [
        ("FastAPI Available", test_fastapi_available),
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_check),
        ("Search - Valid Request", test_search_endpoint_valid),
        ("Search - Invalid Category", test_search_endpoint_invalid_category),
        ("Search - Low Budget", test_search_endpoint_low_budget),
        ("Search - Furniture Category", test_search_endpoint_furniture),
        ("Search - Appliance Category", test_search_endpoint_appliance),
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            if FASTAPI_AVAILABLE:
                print(f"✓ {test_name}")
                passed += 1
            else:
                print(f"⊘ {test_name} (skipped - FastAPI not available)")
                skipped += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    if skipped > 0:
        print(f"Tests skipped: {skipped}/{len(tests)} (install FastAPI to run)")
    print(f"{'='*50}\n")
    
    sys.exit(0 if failed == 0 else 1)
