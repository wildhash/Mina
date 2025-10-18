"""
Example: Budget-Conscious Laptop Shopping

This example shows how to use Mina to find a high-end laptop
while staying within a specific budget.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mina_agent import MinaAgent


def budget_laptop_example():
    """Example of finding a laptop within a specific budget."""
    
    print("\n" + "="*70)
    print("EXAMPLE: Budget-Conscious Laptop Shopping")
    print("="*70)
    print("\nScenario: User wants a high-performance laptop for under $2,500")
    print("Priorities: Performance and Battery Life\n")
    
    # Initialize agent
    agent = MinaAgent()
    
    # Define requirements
    requirements = {
        "category": "laptop",
        "budget_max": 2500,
        "priorities": ["Performance", "Battery Life"],
        "specific_needs": "Need it for video editing and long flights"
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
    print(f"Mina found {len(recommendations)} options within the $2,500 budget,")
    print("ranking them by confidence score to help make an informed decision.")
    print("="*70 + "\n")


if __name__ == "__main__":
    budget_laptop_example()
