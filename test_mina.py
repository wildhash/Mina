"""
Tests for Mina Agent

Basic unit tests for the Mina shopping concierge agent.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mina_agent import MinaAgent, ProductCategory, ProductOption, Recommendation


def test_agent_initialization():
    """Test that agent can be initialized."""
    agent = MinaAgent()
    assert agent is not None
    assert agent.supported_categories == ['laptop', 'furniture', 'appliance']


def test_product_categories():
    """Test product category enum."""
    assert ProductCategory.LAPTOP.value == "laptop"
    assert ProductCategory.FURNITURE.value == "furniture"
    assert ProductCategory.APPLIANCE.value == "appliance"


def test_browse_retailers():
    """Test retailer browsing functionality."""
    agent = MinaAgent()
    
    requirements = {
        "category": "laptop",
        "budget_max": 3000,
        "priorities": ["Performance", "Battery Life"],
        "specific_needs": "For software development"
    }
    
    products = agent.browse_retailers(requirements)
    
    assert len(products) > 0
    assert all(isinstance(p, ProductOption) for p in products)
    assert all(p.price <= 3000 for p in products)


def test_analyze_with_claude():
    """Test Claude analysis functionality."""
    agent = MinaAgent()
    
    products = [
        ProductOption(
            name="Test Laptop",
            price=2000,
            retailer="Test Store",
            url="http://test.com",
            specs={"processor": "Test CPU", "ram": "16GB"},
            reviews_summary="Great laptop",
            rating=4.5
        )
    ]
    
    requirements = {
        "category": "laptop",
        "budget_max": 3000,
        "priorities": ["Performance"],
        "specific_needs": ""
    }
    
    analyses = agent.analyze_with_claude(products, requirements)
    
    assert len(analyses) == 1
    assert "strengths" in analyses[0]
    assert "weaknesses" in analyses[0]
    assert "fit_score" in analyses[0]


def test_confidence_scores():
    """Test confidence score calculation."""
    agent = MinaAgent()
    
    products = [
        ProductOption(
            name="Test Product",
            price=1500,
            retailer="Test Store",
            url="http://test.com",
            specs={"feature": "test"},
            reviews_summary="Good product",
            rating=4.5
        )
    ]
    
    analyses = [{
        "product": "Test Product",
        "strengths": ["Good performance"],
        "weaknesses": [],
        "fit_score": 80.0,
        "value_assessment": "Good value"
    }]
    
    scores = agent.calculate_confidence_scores(products, analyses)
    
    assert len(scores) == 1
    assert 0 <= scores[0] <= 100


def test_generate_recommendations():
    """Test recommendation generation."""
    agent = MinaAgent()
    
    products = [
        ProductOption(
            name="Test Product",
            price=1500,
            retailer="Test Store",
            url="http://test.com",
            specs={"feature": "test"},
            reviews_summary="Good product",
            rating=4.5
        )
    ]
    
    analyses = [{
        "product": "Test Product",
        "strengths": ["Good performance", "Great value"],
        "weaknesses": ["Limited availability"],
        "fit_score": 85.0,
        "value_assessment": "Excellent value"
    }]
    
    confidence_scores = [87.5]
    
    recommendations = agent.generate_recommendations(products, analyses, confidence_scores)
    
    assert len(recommendations) == 1
    assert isinstance(recommendations[0], Recommendation)
    assert recommendations[0].confidence_score == 87.5
    assert len(recommendations[0].pros) > 0


if __name__ == "__main__":
    # Run tests
    print("Running Mina Agent Tests...\n")
    
    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("Product Categories", test_product_categories),
        ("Browse Retailers", test_browse_retailers),
        ("Claude Analysis", test_analyze_with_claude),
        ("Confidence Scores", test_confidence_scores),
        ("Generate Recommendations", test_generate_recommendations),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}\n")
    
    sys.exit(0 if failed == 0 else 1)
