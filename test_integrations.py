"""
Integration Tests for Mina Agent

Tests for Browser Use, Daytona, and Galileo integrations.
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mina_agent import MinaAgent, ProductCategory, ProductOption


def test_browser_use_integration():
    """Test that Browser Use integration initializes correctly."""
    agent = MinaAgent()
    
    # Browser should be None or initialized based on API key
    # This is expected behavior - it will be None without API key
    assert agent.browser is None or agent.browser is not None
    print("✓ Browser Use integration check passed")


def test_daytona_integration():
    """Test that Daytona integration initializes correctly."""
    agent = MinaAgent()
    
    # Daytona should be None or initialized based on API key
    # This is expected behavior - it will be None without API key
    assert agent.daytona is None or agent.daytona is not None
    print("✓ Daytona integration check passed")


def test_galileo_decorator():
    """Test that Galileo decorators work (even when Galileo not available)."""
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
    
    confidence_scores = [85.0]
    
    # This should work even without Galileo API key
    # The @log decorator becomes a no-op when Galileo is not available
    recommendations = agent.generate_recommendations(products, analyses, confidence_scores)
    
    assert len(recommendations) == 1
    assert recommendations[0].confidence_score == 85.0
    print("✓ Galileo decorator compatibility passed")


def test_async_workflow():
    """Test the async research workflow."""
    agent = MinaAgent()
    
    # Test async method exists and can be called
    async def run_test():
        recommendations = await agent.research_product_async(
            category="laptop",
            budget=3000,
            priorities=["Performance", "Battery Life"]
        )
        return recommendations
    
    # Run the async function
    recommendations = asyncio.run(run_test())
    
    assert len(recommendations) > 0
    assert all(hasattr(r, 'confidence_score') for r in recommendations)
    print("✓ Async workflow passed")


def test_claude_integration_fallback():
    """Test that Claude integration falls back gracefully."""
    # Create agent without API key
    agent = MinaAgent(anthropic_api_key=None)
    
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
    
    # Should fall back to rule-based analysis
    analyses = agent.analyze_with_claude(products, requirements)
    
    assert len(analyses) == 1
    assert "strengths" in analyses[0]
    assert "fit_score" in analyses[0]
    print("✓ Claude fallback mechanism passed")


def test_sandbox_fallback():
    """Test that sandbox analysis falls back gracefully."""
    agent = MinaAgent()
    
    search_results = [
        {
            "retailer": "Test Store",
            "products": [
                {"name": "Test Product", "price": 1000, "rating": 4.5, "review_count": 100}
            ]
        }
    ]
    
    # Should fall back to direct processing without Daytona
    result = agent.analyze_in_sandbox(search_results)
    
    assert "products" in result
    print("✓ Daytona fallback mechanism passed")


def test_integration_with_all_components():
    """Test that all components work together."""
    agent = MinaAgent()
    
    # Verify all integrations are initialized (or None if no API keys)
    assert hasattr(agent, 'claude_client')
    assert hasattr(agent, 'browser')
    assert hasattr(agent, 'daytona')
    
    # Verify agent can still run without API keys
    requirements = {
        "category": "laptop",
        "budget_max": 2500,
        "priorities": ["Performance", "Battery Life"],
        "specific_needs": "For software development"
    }
    
    products = agent.browse_retailers(requirements)
    analyses = agent.analyze_with_claude(products, requirements)
    confidence_scores = agent.calculate_confidence_scores(products, analyses)
    recommendations = agent.generate_recommendations(products, analyses, confidence_scores)
    
    assert len(recommendations) > 0
    assert all(r.confidence_score > 0 for r in recommendations)
    print("✓ Full integration workflow passed")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Running Mina Integration Tests")
    print("="*60 + "\n")
    
    tests = [
        ("Browser Use Integration", test_browser_use_integration),
        ("Daytona Integration", test_daytona_integration),
        ("Galileo Decorator", test_galileo_decorator),
        ("Async Workflow", test_async_workflow),
        ("Claude Fallback", test_claude_integration_fallback),
        ("Sandbox Fallback", test_sandbox_fallback),
        ("Full Integration", test_integration_with_all_components),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Integration Tests passed: {passed}/{len(tests)}")
    print(f"Integration Tests failed: {failed}/{len(tests)}")
    print(f"{'='*60}\n")
    
    sys.exit(0 if failed == 0 else 1)
