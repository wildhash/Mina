#!/usr/bin/env python3
"""
Mina Agent Demo

Demonstrates the Mina shopping concierge with automated inputs
for testing and demonstration purposes.
"""

import sys
import os
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mina_agent import MinaAgent


def run_demo():
    """Run a demonstration of the Mina agent with simulated inputs."""
    
    print("="*70)
    print("MINA AGENT DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows how Mina helps users make confident high-end purchases.")
    print("We'll simulate a user shopping for a high-end laptop.\n")
    
    input("Press Enter to start the demonstration...")
    print("\n")
    
    # Initialize agent
    agent = MinaAgent()
    
    # Simulate the workflow programmatically
    print("="*60)
    print("Step 1: Product Category Selection")
    print("="*60)
    print("User selects: Laptop\n")
    
    category_map = {
        "laptop": agent.browse_retailers.__self__.ProductCategory.LAPTOP if hasattr(agent, 'ProductCategory') else "laptop"
    }
    
    # Simulate requirements
    print("="*60)
    print("Step 2: Requirements Gathering")
    print("="*60)
    print("User inputs:")
    print("  - Budget: $3,000")
    print("  - Priorities: Performance, Battery Life, Build Quality")
    print("  - Specific needs: For software development and travel")
    print()
    
    requirements = {
        "category": "laptop",
        "budget_max": 3000,
        "priorities": ["Performance", "Battery Life", "Build Quality"],
        "specific_needs": "For software development and travel"
    }
    
    # Browse retailers
    print("="*60)
    print("Step 3: Multi-Retailer Research")
    print("="*60)
    products = agent.browse_retailers(requirements)
    print(f"Found {len(products)} products within budget\n")
    
    # Analyze with Claude
    print("="*60)
    print("Step 4: AI-Powered Analysis")
    print("="*60)
    analyses = agent.analyze_with_claude(products, requirements)
    print("Completed detailed analysis of all products\n")
    
    # Calculate confidence scores
    print("="*60)
    print("Step 5: Confidence Score Generation")
    print("="*60)
    confidence_scores = agent.calculate_confidence_scores(products, analyses)
    print("Generated confidence scores using Galileo methodology\n")
    
    # Generate recommendations
    print("="*60)
    print("Step 6: Generate Recommendations")
    print("="*60)
    recommendations = agent.generate_recommendations(
        products, analyses, confidence_scores
    )
    print(f"Created {len(recommendations)} personalized recommendations\n")
    
    # Present findings
    print("="*60)
    print("Step 7: Present Findings")
    print("="*60)
    agent.present_recommendations(recommendations)
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nKey Features Demonstrated:")
    print("✓ Intelligent product category selection")
    print("✓ Budget-aware filtering")
    print("✓ Multi-retailer research simulation")
    print("✓ AI-powered specification and review analysis")
    print("✓ Transparent confidence scoring")
    print("✓ Clear reasoning for each recommendation")
    print("✓ Comprehensive product comparison")
    print("\nMina helps users make confident decisions on high-end purchases")
    print("by providing transparent, AI-powered recommendations.\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
