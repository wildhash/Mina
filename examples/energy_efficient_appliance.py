"""
Example: Energy-Efficient Appliance Selection

This example shows how Mina helps choose appliances with
focus on long-term efficiency and cost savings.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mina_agent import MinaAgent


def energy_efficient_appliance_example():
    """Example of finding an energy-efficient washing machine."""
    
    print("\n" + "="*70)
    print("EXAMPLE: Energy-Efficient Appliance Selection")
    print("="*70)
    print("\nScenario: Upgrading to premium washing machine")
    print("Focus on energy efficiency and long-term reliability\n")
    
    # Initialize agent
    agent = MinaAgent()
    
    # Define requirements
    requirements = {
        "category": "appliance",
        "budget_max": 2000,
        "priorities": ["Energy Efficiency", "Reliability", "Capacity"],
        "specific_needs": "Large family, multiple loads per week, want to reduce utility bills"
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
    print("All recommended machines are Energy Star certified, potentially")
    print("saving hundreds of dollars in utility costs over their lifetime.")
    print("="*70 + "\n")


if __name__ == "__main__":
    energy_efficient_appliance_example()
