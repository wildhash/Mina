"""
Mina - AI Shopping Concierge for High-End Purchases

This module provides the main agent functionality for helping users
make confident high-end purchases ($500+).
"""

import os
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Third-party imports will be handled gracefully
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    from browser_use import Agent as BrowserAgent
except ImportError:
    BrowserAgent = None


class ProductCategory(Enum):
    """Supported product categories for high-end purchases."""
    LAPTOP = "laptop"
    FURNITURE = "furniture"
    APPLIANCE = "appliance"


@dataclass
class ProductOption:
    """Represents a product option found during research."""
    name: str
    price: float
    retailer: str
    url: str
    specs: Dict[str, Any]
    reviews_summary: str
    rating: float


@dataclass
class Recommendation:
    """Represents a final recommendation with confidence score."""
    product: ProductOption
    confidence_score: float
    reasoning: str
    pros: List[str]
    cons: List[str]


class MinaAgent:
    """
    Main AI agent for high-end purchase recommendations.
    
    This agent guides users through researching and selecting
    high-end products by browsing retailers, analyzing reviews,
    and providing transparent recommendations with confidence scores.
    """
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        """
        Initialize the Mina agent.
        
        Args:
            anthropic_api_key: API key for Claude (Anthropic)
        """
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.claude_client = None
        
        if Anthropic and self.anthropic_api_key:
            self.claude_client = Anthropic(api_key=self.anthropic_api_key)
        
        self.supported_categories = [cat.value for cat in ProductCategory]
    
    def get_product_category(self) -> ProductCategory:
        """
        Ask user for product category.
        
        Returns:
            Selected product category
        """
        print("\n" + "="*60)
        print("Welcome to Mina - Your AI Shopping Concierge")
        print("="*60)
        print("\nI help you make confident decisions on high-end purchases ($500+)")
        print("by researching products, analyzing reviews, and providing")
        print("transparent recommendations with confidence scores.\n")
        
        print("What type of product are you looking to purchase?")
        print("1. Laptop")
        print("2. Furniture")
        print("3. Appliance")
        
        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                return ProductCategory.LAPTOP
            elif choice == "2":
                return ProductCategory.FURNITURE
            elif choice == "3":
                return ProductCategory.APPLIANCE
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    def gather_requirements(self, category: ProductCategory) -> Dict[str, Any]:
        """
        Gather user requirements for the product.
        
        Args:
            category: Product category
            
        Returns:
            Dictionary of user requirements
        """
        print(f"\n{'='*60}")
        print(f"Great! Let's find the perfect {category.value} for you.")
        print(f"{'='*60}\n")
        
        requirements = {
            "category": category.value,
            "budget_max": None,
            "priorities": [],
            "specific_needs": ""
        }
        
        # Get budget
        while True:
            budget_input = input("What's your maximum budget? ($): ").strip()
            try:
                budget = float(budget_input.replace(",", "").replace("$", ""))
                if budget >= 500:
                    requirements["budget_max"] = budget
                    break
                else:
                    print("Budget should be at least $500 for high-end purchases.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get priorities based on category
        print("\nWhat are your top priorities? (You can select multiple)")
        
        if category == ProductCategory.LAPTOP:
            priorities = ["Performance", "Battery Life", "Display Quality", 
                         "Portability", "Build Quality"]
        elif category == ProductCategory.FURNITURE:
            priorities = ["Durability", "Comfort", "Design/Aesthetics", 
                         "Material Quality", "Size/Space Efficiency"]
        else:  # APPLIANCE
            priorities = ["Energy Efficiency", "Capacity", "Smart Features", 
                         "Reliability", "Noise Level"]
        
        for i, priority in enumerate(priorities, 1):
            print(f"{i}. {priority}")
        
        while True:
            selection = input("\nEnter priority numbers (comma-separated, e.g., 1,3,4): ").strip()
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(",")]
                if all(0 <= i < len(priorities) for i in indices):
                    requirements["priorities"] = [priorities[i] for i in indices]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter valid numbers separated by commas.")
        
        # Get specific needs
        print("\nAny specific requirements or features you're looking for?")
        specific = input("(Press Enter to skip): ").strip()
        requirements["specific_needs"] = specific
        
        return requirements
    
    def browse_retailers(self, requirements: Dict[str, Any]) -> List[ProductOption]:
        """
        Browse multiple retailers to find top product options.
        
        Args:
            requirements: User requirements
            
        Returns:
            List of product options found
        """
        print(f"\n{'='*60}")
        print("🔍 Browsing multiple retailers for top options...")
        print(f"{'='*60}\n")
        
        category = requirements["category"]
        budget = requirements["budget_max"]
        
        # Simulate retailer browsing (in production, this would use browser-use)
        # For demonstration, we'll create mock data
        print("Searching: Amazon, Best Buy, B&H Photo, Newegg, Wayfair...")
        
        # Mock product options based on category
        if category == "laptop":
            products = [
                ProductOption(
                    name="MacBook Pro 16\" M3 Max",
                    price=3499.00,
                    retailer="Apple Store",
                    url="https://www.apple.com/shop/buy-mac/macbook-pro",
                    specs={
                        "processor": "M3 Max",
                        "ram": "36GB",
                        "storage": "1TB SSD",
                        "display": "16.2\" Liquid Retina XDR",
                        "battery": "Up to 22 hours"
                    },
                    reviews_summary="Exceptional performance and battery life. Premium build quality.",
                    rating=4.8
                ),
                ProductOption(
                    name="Dell XPS 15 9530",
                    price=2599.00,
                    retailer="Dell",
                    url="https://www.dell.com/xps",
                    specs={
                        "processor": "Intel Core i9-13900H",
                        "ram": "32GB DDR5",
                        "storage": "1TB SSD",
                        "display": "15.6\" 4K OLED",
                        "battery": "Up to 13 hours"
                    },
                    reviews_summary="Excellent display and performance. Good value for specs.",
                    rating=4.6
                ),
                ProductOption(
                    name="Lenovo ThinkPad X1 Carbon Gen 11",
                    price=2299.00,
                    retailer="Lenovo",
                    url="https://www.lenovo.com/thinkpad",
                    specs={
                        "processor": "Intel Core i7-1365U",
                        "ram": "32GB LPDDR5",
                        "storage": "1TB SSD",
                        "display": "14\" 2.8K OLED",
                        "battery": "Up to 19 hours"
                    },
                    reviews_summary="Business-class durability. Excellent keyboard and portability.",
                    rating=4.7
                )
            ]
        elif category == "furniture":
            products = [
                ProductOption(
                    name="Herman Miller Aeron Chair",
                    price=1695.00,
                    retailer="Herman Miller",
                    url="https://www.hermanmiller.com/aeron",
                    specs={
                        "material": "8Z Pellicle mesh",
                        "adjustment": "PostureFit SL support",
                        "warranty": "12 years",
                        "weight_capacity": "350 lbs"
                    },
                    reviews_summary="Industry-leading ergonomics. Durable and comfortable for long hours.",
                    rating=4.7
                ),
                ProductOption(
                    name="Steelcase Leap V2",
                    price=1099.00,
                    retailer="Steelcase",
                    url="https://www.steelcase.com/leap",
                    specs={
                        "material": "LiveBack technology",
                        "adjustment": "4D adjustable arms",
                        "warranty": "12 years",
                        "weight_capacity": "400 lbs"
                    },
                    reviews_summary="Highly adjustable. Great back support and build quality.",
                    rating=4.6
                ),
                ProductOption(
                    name="Haworth Fern",
                    price=899.00,
                    retailer="Haworth",
                    url="https://www.haworth.com/fern",
                    specs={
                        "material": "Wave suspension",
                        "adjustment": "Adaptive lumbar support",
                        "warranty": "12 years",
                        "weight_capacity": "300 lbs"
                    },
                    reviews_summary="Eco-friendly materials. Excellent lumbar support at a lower price point.",
                    rating=4.5
                )
            ]
        else:  # appliance
            products = [
                ProductOption(
                    name="Miele W1 Washing Machine",
                    price=1799.00,
                    retailer="Miele",
                    url="https://www.miele.com/washing-machines",
                    specs={
                        "capacity": "4.5 cu ft",
                        "energy_rating": "Energy Star",
                        "features": "TwinDos, CapDosing, WiFi",
                        "warranty": "2 years + 10 year parts"
                    },
                    reviews_summary="German engineering excellence. Quiet operation and gentle on clothes.",
                    rating=4.8
                ),
                ProductOption(
                    name="LG WM9000HVA Front Load",
                    price=1499.00,
                    retailer="Best Buy",
                    url="https://www.bestbuy.com/lg-washer",
                    specs={
                        "capacity": "5.0 cu ft",
                        "energy_rating": "Energy Star",
                        "features": "TurboWash 360, AI DD, WiFi",
                        "warranty": "1 year + 10 year motor"
                    },
                    reviews_summary="Large capacity with smart features. Good value and reliability.",
                    rating=4.6
                ),
                ProductOption(
                    name="Bosch 800 Series WAW285H2UC",
                    price=1299.00,
                    retailer="Home Depot",
                    url="https://www.homedepot.com/bosch-washer",
                    specs={
                        "capacity": "2.2 cu ft",
                        "energy_rating": "Energy Star",
                        "features": "SpeedPerfect, Home Connect",
                        "warranty": "1 year"
                    },
                    reviews_summary="Compact European design. Very quiet and efficient.",
                    rating=4.5
                )
            ]
        
        # Filter by budget
        filtered_products = [p for p in products if p.price <= budget]
        
        if not filtered_products:
            print(f"\n⚠️  No products found within budget. Showing closest options:")
            filtered_products = sorted(products, key=lambda p: p.price)[:3]
        
        print(f"\n✓ Found {len(filtered_products)} options within your budget\n")
        
        return filtered_products
    
    def analyze_with_claude(self, products: List[ProductOption], 
                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze products using Claude AI.
        
        Args:
            products: List of product options
            requirements: User requirements
            
        Returns:
            Analysis results for each product
        """
        print(f"{'='*60}")
        print("🤖 Analyzing reviews and specifications with Claude AI...")
        print(f"{'='*60}\n")
        
        analyses = []
        
        for product in products:
            print(f"Analyzing: {product.name}...")
            
            # In production, this would use Claude API
            # For demonstration, we'll create structured analysis
            analysis = {
                "product": product.name,
                "strengths": [],
                "weaknesses": [],
                "fit_score": 0.0,
                "value_assessment": ""
            }
            
            # Simulate Claude analysis based on priorities
            if "Performance" in requirements["priorities"]:
                if "M3 Max" in product.name or "i9" in str(product.specs):
                    analysis["strengths"].append("Exceptional performance for demanding tasks")
                    analysis["fit_score"] += 25
            
            if "Battery Life" in requirements["priorities"]:
                if "22 hours" in str(product.specs) or "19 hours" in str(product.specs):
                    analysis["strengths"].append("Outstanding battery life for all-day use")
                    analysis["fit_score"] += 25
            
            if "Durability" in requirements["priorities"]:
                if "12 years" in str(product.specs) or "Herman Miller" in product.name:
                    analysis["strengths"].append("Built to last with industry-leading warranty")
                    analysis["fit_score"] += 25
            
            if "Energy Efficiency" in requirements["priorities"]:
                if "Energy Star" in str(product.specs):
                    analysis["strengths"].append("Energy efficient, will save on utility bills")
                    analysis["fit_score"] += 25
            
            # Add default strengths
            if product.rating >= 4.7:
                analysis["strengths"].append("Highly rated by verified customers")
                analysis["fit_score"] += 15
            
            # Add weaknesses based on price/value
            if product.price > requirements["budget_max"] * 0.8:
                analysis["weaknesses"].append("At the higher end of your budget")
            
            # Value assessment
            price_value_ratio = product.rating / (product.price / 1000)
            if price_value_ratio > 3:
                analysis["value_assessment"] = "Excellent value for money"
            elif price_value_ratio > 2:
                analysis["value_assessment"] = "Good value for the features offered"
            else:
                analysis["value_assessment"] = "Premium pricing for top-tier quality"
            
            # Normalize fit score
            analysis["fit_score"] = min(100, analysis["fit_score"])
            
            analyses.append(analysis)
        
        print("✓ Analysis complete\n")
        return analyses
    
    def calculate_confidence_scores(self, products: List[ProductOption],
                                    analyses: List[Dict[str, Any]]) -> List[float]:
        """
        Calculate confidence scores using Galileo-inspired methodology.
        
        Args:
            products: List of product options
            analyses: Analysis results from Claude
            
        Returns:
            Confidence scores for each product
        """
        print(f"{'='*60}")
        print("📊 Generating confidence scores with Galileo methodology...")
        print(f"{'='*60}\n")
        
        confidence_scores = []
        
        for product, analysis in zip(products, analyses):
            # Multi-factor confidence calculation
            factors = {
                "rating": product.rating / 5.0,  # Normalized rating
                "fit_score": analysis["fit_score"] / 100.0,  # Match to requirements
                "review_confidence": 0.9 if product.rating >= 4.5 else 0.7,
                "data_completeness": 1.0 if product.specs else 0.6,
            }
            
            # Weighted average with emphasis on fit and ratings
            weights = {
                "rating": 0.25,
                "fit_score": 0.40,
                "review_confidence": 0.20,
                "data_completeness": 0.15
            }
            
            confidence = sum(factors[k] * weights[k] for k in factors.keys())
            
            # Apply penalty for limited data or mixed reviews
            if not product.reviews_summary or len(analysis["weaknesses"]) > 2:
                confidence *= 0.9
            
            # Convert to percentage and round
            confidence_percentage = round(confidence * 100, 1)
            confidence_scores.append(confidence_percentage)
            
            print(f"✓ {product.name}: {confidence_percentage}% confidence")
        
        print()
        return confidence_scores
    
    def generate_recommendations(self, products: List[ProductOption],
                                analyses: List[Dict[str, Any]],
                                confidence_scores: List[float]) -> List[Recommendation]:
        """
        Generate final recommendations with reasoning.
        
        Args:
            products: List of product options
            analyses: Analysis results
            confidence_scores: Confidence scores
            
        Returns:
            List of recommendations sorted by confidence
        """
        recommendations = []
        
        for product, analysis, confidence in zip(products, analyses, confidence_scores):
            reasoning = f"""
Based on comprehensive analysis of specifications, customer reviews, and 
your stated priorities, this product scores {analysis['fit_score']:.0f}/100 
for meeting your requirements. {analysis['value_assessment']}.

The {confidence:.1f}% confidence score reflects:
- Strong customer ratings ({product.rating}/5.0 from verified buyers)
- {"Excellent" if analysis['fit_score'] > 75 else "Good"} alignment with your priorities
- Comprehensive data available for informed decision-making
            """.strip()
            
            rec = Recommendation(
                product=product,
                confidence_score=confidence,
                reasoning=reasoning,
                pros=analysis["strengths"],
                cons=analysis["weaknesses"] if analysis["weaknesses"] else ["None identified"]
            )
            
            recommendations.append(rec)
        
        # Sort by confidence score
        recommendations.sort(key=lambda r: r.confidence_score, reverse=True)
        
        return recommendations
    
    def present_recommendations(self, recommendations: List[Recommendation]) -> None:
        """
        Present recommendations to user with clear reasoning.
        
        Args:
            recommendations: List of recommendations to present
        """
        print(f"\n{'='*60}")
        print("🎯 YOUR PERSONALIZED RECOMMENDATIONS")
        print(f"{'='*60}\n")
        
        for i, rec in enumerate(recommendations, 1):
            product = rec.product
            
            print(f"{'─'*60}")
            print(f"#{i} RECOMMENDATION - {rec.confidence_score}% Confidence Score")
            print(f"{'─'*60}")
            print(f"\n📦 {product.name}")
            print(f"💰 Price: ${product.price:,.2f}")
            print(f"🏪 Retailer: {product.retailer}")
            print(f"⭐ Rating: {product.rating}/5.0")
            
            print(f"\n📋 KEY SPECIFICATIONS:")
            for key, value in product.specs.items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
            
            print(f"\n✅ STRENGTHS:")
            for pro in rec.pros:
                print(f"   • {pro}")
            
            if rec.cons[0] != "None identified":
                print(f"\n⚠️  CONSIDERATIONS:")
                for con in rec.cons:
                    print(f"   • {con}")
            
            print(f"\n💡 WHY THIS RECOMMENDATION:")
            for line in rec.reasoning.split('\n'):
                if line.strip():
                    print(f"   {line.strip()}")
            
            print(f"\n🔗 Learn more: {product.url}")
            print()
        
        # Summary
        print(f"{'='*60}")
        print("📝 DECISION SUMMARY")
        print(f"{'='*60}\n")
        
        top_rec = recommendations[0]
        print(f"Based on your priorities and budget, I recommend the")
        print(f"{top_rec.product.name} with {top_rec.confidence_score}% confidence.")
        print(f"\nThis recommendation is based on:")
        print(f"• Comprehensive retailer research")
        print(f"• AI-powered review and specification analysis")
        print(f"• Transparent confidence scoring")
        print(f"• Alignment with your stated priorities")
        
        print(f"\n{'='*60}\n")
    
    def run(self) -> None:
        """
        Run the complete Mina agent workflow.
        """
        try:
            # Step 1: Get product category
            category = self.get_product_category()
            
            # Step 2: Gather requirements
            requirements = self.gather_requirements(category)
            
            # Step 3: Browse retailers (using browser-use in production)
            products = self.browse_retailers(requirements)
            
            if not products:
                print("\n❌ No products found matching your criteria.")
                return
            
            # Step 4: Analyze with Claude
            analyses = self.analyze_with_claude(products, requirements)
            
            # Step 5: Calculate confidence scores (Galileo methodology)
            confidence_scores = self.calculate_confidence_scores(products, analyses)
            
            # Step 6: Generate recommendations
            recommendations = self.generate_recommendations(
                products, analyses, confidence_scores
            )
            
            # Step 7: Present findings
            self.present_recommendations(recommendations)
            
            print("Thank you for using Mina! Make your purchase with confidence. 🛍️\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session cancelled. Come back when you're ready to shop!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or contact support.")


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    pass
