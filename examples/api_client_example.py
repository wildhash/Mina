"""
Example: Using the Mina API with Python

This example demonstrates how to interact with the Mina API server
using Python's requests library.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"


def check_health():
    """Check if the API server is healthy."""
    print("Checking API health...")
    response = requests.get(f"{BASE_URL}/api/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API Status: {data['status']}")
        print(f"✓ Version: {data['version']}")
        print(f"✓ Integrations:")
        for integration, available in data['integrations'].items():
            status = "✓" if available else "✗"
            print(f"  {status} {integration.replace('_', ' ').title()}")
        return True
    else:
        print(f"✗ API Health Check Failed: {response.status_code}")
        return False


def search_laptop():
    """Search for a laptop."""
    print("\n" + "="*60)
    print("Searching for laptops...")
    print("="*60)
    
    search_request = {
        "category": "laptop",
        "budget_max": 3000,
        "priorities": ["Performance", "Battery Life", "Display Quality"],
        "specific_needs": "For software development and machine learning"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/search",
        json=search_request,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Found {data['total_products_analyzed']} products")
        print(f"✓ Search completed in {data['search_time_seconds']} seconds\n")
        
        print("="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        
        for i, rec in enumerate(data['recommendations'], 1):
            product = rec['product']
            print(f"\n#{i} - {product['name']}")
            print(f"   Price: ${product['price']:,.2f}")
            print(f"   Retailer: {product['retailer']}")
            print(f"   Rating: {product['rating']}/5.0")
            print(f"   Confidence: {rec['confidence_score']:.1f}%")
            
            print(f"\n   Strengths:")
            for pro in rec['pros'][:3]:  # Show top 3 pros
                print(f"   • {pro}")
            
            if rec['cons'][0] != "None identified":
                print(f"\n   Considerations:")
                for con in rec['cons'][:2]:  # Show top 2 cons
                    print(f"   • {con}")
            
            print(f"\n   URL: {product['url']}")
            print()
        
        return data
    else:
        print(f"✗ Search Failed: {response.status_code}")
        print(f"   Error: {response.json().get('detail', 'Unknown error')}")
        return None


def search_furniture():
    """Search for furniture."""
    print("\n" + "="*60)
    print("Searching for furniture...")
    print("="*60)
    
    search_request = {
        "category": "furniture",
        "budget_max": 1500,
        "priorities": ["Durability", "Comfort", "Design/Aesthetics"],
        "specific_needs": "Ergonomic office chair for long hours"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/search",
        json=search_request,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Found {data['total_products_analyzed']} products")
        print(f"✓ Search completed in {data['search_time_seconds']} seconds")
        
        # Show top recommendation
        if data['recommendations']:
            rec = data['recommendations'][0]
            product = rec['product']
            print(f"\n🎯 Top Recommendation: {product['name']}")
            print(f"   Confidence: {rec['confidence_score']:.1f}%")
            print(f"   Price: ${product['price']:,.2f}")
        
        return data
    else:
        print(f"✗ Search Failed: {response.status_code}")
        return None


def search_appliance():
    """Search for an appliance."""
    print("\n" + "="*60)
    print("Searching for appliances...")
    print("="*60)
    
    search_request = {
        "category": "appliance",
        "budget_max": 1800,
        "priorities": ["Energy Efficiency", "Capacity", "Reliability"],
        "specific_needs": "Energy-efficient washing machine"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/search",
        json=search_request,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Found {data['total_products_analyzed']} products")
        print(f"✓ Search completed in {data['search_time_seconds']} seconds")
        
        # Show top recommendation
        if data['recommendations']:
            rec = data['recommendations'][0]
            product = rec['product']
            print(f"\n🎯 Top Recommendation: {product['name']}")
            print(f"   Confidence: {rec['confidence_score']:.1f}%")
            print(f"   Price: ${product['price']:,.2f}")
        
        return data
    else:
        print(f"✗ Search Failed: {response.status_code}")
        return None


def main():
    """Main function to run examples."""
    print("="*60)
    print("Mina API Client Example")
    print("="*60)
    
    # Check API health
    if not check_health():
        print("\n❌ API server is not available.")
        print("Please start the server with: python api_server.py")
        return
    
    # Run searches
    try:
        # Example 1: Detailed laptop search
        search_laptop()
        
        # Example 2: Furniture search
        search_furniture()
        
        # Example 3: Appliance search
        search_appliance()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API server.")
        print("Please start the server with: python api_server.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
