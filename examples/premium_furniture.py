"""
Example: Premium Furniture Investment

This example demonstrates using Mina to research high-end
office furniture with focus on long-term value.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mina_agent import MinaAgent


def premium_furniture_example():
    """Example of researching premium office furniture."""
    
    print("\n" + "="*70)
    print("EXAMPLE: Premium Office Furniture Investment")
    print("="*70)
    print("\nScenario: Remote worker investing in ergonomic office chair")
    print("Willing to spend up to $2,000 for quality and durability\n")
    
    # Initialize agent
    agent = MinaAgent()
    
    # Define requirements
    requirements = {
        "category": "furniture",
        "budget_max": 2000,
        "priorities": ["Durability", "Comfort", "Material Quality"],
        "specific_needs": "Work from home 8-10 hours daily, need excellent back support"
    }
    
    print("Requirements:")
    print(f"  • Budget: ${requirements['budget_max']:,}")
    print(f"  • Category: {requirements['category']}")
    print(f"  • Priorities: {', '.join(requirements['priorities'])}")
    print(f"  • Specific Needs: {requirements['specific_needs']}")
    print()
    
    # Run the workflow
    products = agent.browse_retailers(requirements)
    analyses = agent.analyze_with_claude(products, requirements)
    confidence_scores = agent.calculate_confidence_scores(products, analyses)
    recommendations = agent.generate_recommendations(products, analyses, confidence_scores)
    
    # Present results
    agent.present_recommendations(recommendations)
    
    print("\nKey Takeaway:")
    print("All recommended chairs come with 12-year warranties, demonstrating")
    print("manufacturer confidence in long-term durability and value.")
    print("="*70 + "\n")


if __name__ == "__main__":
    premium_furniture_example()
