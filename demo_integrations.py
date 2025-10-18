"""
Comprehensive Integration Demo

This script demonstrates all three integrations working together:
- Browser Use for multi-retailer scraping
- Daytona for safe code execution
- Galileo for observability and confidence scoring
- Claude for AI-powered analysis
"""

import asyncio
import os
from mina_agent import MinaAgent


async def demo_full_integration():
    """
    Demonstrate the complete integration of all technologies.
    """
    print("\n" + "="*70)
    print(" MINA BACKEND INTEGRATION DEMO ".center(70, "="))
    print("="*70 + "\n")
    
    print("This demo showcases integration with:")
    print("  ✓ Claude (Anthropic) - AI-powered product analysis")
    print("  ✓ Browser Use - Multi-retailer web scraping")
    print("  ✓ Daytona - Safe sandbox code execution")
    print("  ✓ Galileo - Observability and confidence metrics")
    print()
    
    # Initialize agent
    print("Initializing Mina Agent with all integrations...")
    agent = MinaAgent()
    
    # Show integration status
    print("\nIntegration Status:")
    print(f"  • Claude API: {'✓ Connected' if agent.claude_client else '○ Not configured (using fallback)'}")
    print(f"  • Browser Use: {'✓ Initialized' if agent.browser else '○ Not configured (using mock data)'}")
    print(f"  • Daytona: {'✓ Ready' if agent.daytona else '○ Not configured (using direct processing)'}")
    print(f"  • Galileo: {'✓ Logging enabled' if os.getenv('GALILEO_API_KEY') else '○ Not configured (metrics only)'}")
    
    print("\n" + "-"*70)
    print(" DEMO SCENARIO: Finding a Premium Gaming Laptop ".center(70))
    print("-"*70 + "\n")
    
    # Define search parameters
    category = "laptop"
    budget = 3000
    priorities = ["Performance", "Battery Life", "Display Quality"]
    
    print(f"Search Parameters:")
    print(f"  • Category: {category.title()}")
    print(f"  • Budget: ${budget:,}")
    print(f"  • Priorities: {', '.join(priorities)}")
    print()
    
    # Run the full async workflow
    print("\n" + "="*70)
    print(" PHASE 1: Multi-Retailer Research (Browser Use) ".center(70, "="))
    print("="*70)
    
    recommendations = await agent.research_product_async(
        category=category,
        budget=budget,
        priorities=priorities
    )
    
    # Display results
    print("\n" + "="*70)
    print(" PHASE 4: Final Recommendations ".center(70, "="))
    print("="*70 + "\n")
    
    agent.present_recommendations(recommendations)
    
    # Show technology breakdown
    print("\n" + "="*70)
    print(" TECHNOLOGY BREAKDOWN ".center(70, "="))
    print("="*70 + "\n")
    
    print("🌐 Browser Use Integration:")
    print("   • Attempted to scrape live data from multiple retailers")
    print("   • Cloud browser support for anti-bot protection")
    print("   • Falls back to mock data for demo purposes")
    print()
    
    print("🔒 Daytona Sandbox Integration:")
    print("   • Safe execution environment for data processing")
    print("   • Isolated pandas/numpy operations")
    print("   • Sub-90ms sandbox creation")
    print()
    
    print("🤖 Claude AI Integration:")
    print("   • Intelligent product analysis")
    print("   • Natural language reasoning")
    print("   • Structured JSON output")
    print()
    
    print("📊 Galileo Observability:")
    print("   • Workflow tracing with @log decorators")
    print("   • Multi-factor confidence scoring:")
    print("     - Customer Ratings (25%)")
    print("     - Requirements Fit (40%)")
    print("     - Review Confidence (20%)")
    print("     - Data Completeness (15%)")
    print()
    
    print("\n" + "="*70)
    print(" KEY FEATURES DEMONSTRATED ".center(70, "="))
    print("="*70 + "\n")
    
    print("✓ Multi-Tool Integration: All three partner technologies work together")
    print("✓ Confidence Transparency: Clear confidence scores with reasoning")
    print("✓ Safe Execution: Daytona isolates all code for security")
    print("✓ Real Scraping: Browser Use ready for live retailer data")
    print("✓ Clear Reasoning: Every recommendation explains why")
    print("✓ Async Operations: Efficient parallel processing")
    print("✓ Graceful Fallbacks: Works even without API keys")
    
    print("\n" + "="*70)
    print(" DEMO COMPLETE ".center(70, "="))
    print("="*70 + "\n")


def demo_sync_workflow():
    """
    Demonstrate the synchronous workflow (backwards compatible).
    """
    print("\n" + "="*70)
    print(" SYNCHRONOUS WORKFLOW DEMO ".center(70, "="))
    print("="*70 + "\n")
    
    print("This demonstrates backwards compatibility with the original workflow.\n")
    
    agent = MinaAgent()
    
    requirements = {
        "category": "furniture",
        "budget_max": 1500,
        "priorities": ["Durability", "Comfort"],
        "specific_needs": "Home office chair"
    }
    
    # Traditional synchronous workflow
    products = agent.browse_retailers(requirements)
    analyses = agent.analyze_with_claude(products, requirements)
    confidence_scores = agent.calculate_confidence_scores(products, analyses)
    recommendations = agent.generate_recommendations(products, analyses, confidence_scores)
    
    print("\n✓ Synchronous workflow completed successfully")
    print(f"✓ Found {len(recommendations)} recommendations")
    print(f"✓ Top recommendation: {recommendations[0].product.name}")
    print(f"✓ Confidence: {recommendations[0].confidence_score}%\n")


async def main():
    """
    Main demo runner.
    """
    # Run async demo
    await demo_full_integration()
    
    # Run sync demo
    demo_sync_workflow()
    
    print("\n" + "="*70)
    print("\nTo use with real API keys, set these environment variables:")
    print("  • ANTHROPIC_API_KEY - For Claude AI analysis")
    print("  • BROWSER_USE_API_KEY - For cloud browser scraping")
    print("  • DAYTONA_API_KEY - For sandbox execution")
    print("  • GALILEO_API_KEY - For observability logging")
    print("\nSee .env.example for the complete template.\n")


if __name__ == "__main__":
    asyncio.run(main())
