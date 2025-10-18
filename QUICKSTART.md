# Quick Start Guide

Get Mina up and running in minutes!

## 🚀 5-Minute Setup (Without API Keys)

Perfect for testing and development:

```bash
# Clone the repository
git clone https://github.com/wildhash/Mina.git
cd Mina

# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_integrations.py
```

That's it! Mina will run using mock data and fallback mechanisms.

---

## 🔑 Production Setup (With API Keys)

For real web scraping and AI analysis:

### Step 1: Get API Keys

| Service | Purpose | Free Credits | Get Key |
|---------|---------|--------------|---------|
| **Anthropic** | Claude AI analysis | Usage-based | [console.anthropic.com](https://console.anthropic.com/) |
| **Browser Use** | Web scraping | $10 free | [cloud.browser-use.com](https://cloud.browser-use.com/) |
| **Daytona** | Sandbox execution | $200 free | [daytona.io](https://www.daytona.io/) |
| **Galileo** | Observability | Contact sales | [galileo.ai](https://www.galileo.ai/) |

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your preferred editor
```

Your `.env` should look like:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
BROWSER_USE_API_KEY=your-key-here
DAYTONA_API_KEY=your-key-here
GALILEO_API_KEY=your-key-here
GALILEO_PROJECT=Mina-Shopping-Agent
GALILEO_LOG_STREAM=main
```

### Step 3: Run Mina

```bash
# Run interactive CLI
python mina_cli.py

# Or run the integration demo
python demo_integrations.py
```

---

## 📝 Usage Examples

### Interactive CLI

```bash
python mina_cli.py
```

Follow the prompts to:
1. Select a product category (laptop, furniture, appliance)
2. Enter your budget
3. Choose your priorities
4. Get personalized recommendations with confidence scores

### Programmatic Usage (Sync)

```python
from mina_agent import MinaAgent

# Initialize agent
agent = MinaAgent()

# Define requirements
requirements = {
    "category": "laptop",
    "budget_max": 3000,
    "priorities": ["Performance", "Battery Life"],
    "specific_needs": "For software development"
}

# Get recommendations
products = agent.browse_retailers(requirements)
analyses = agent.analyze_with_claude(products, requirements)
confidence_scores = agent.calculate_confidence_scores(products, analyses)
recommendations = agent.generate_recommendations(products, analyses, confidence_scores)

# Display results
agent.present_recommendations(recommendations)
```

### Programmatic Usage (Async)

```python
import asyncio
from mina_agent import MinaAgent

async def find_laptop():
    agent = MinaAgent()
    
    # Use async workflow for better performance
    recommendations = await agent.research_product_async(
        category="laptop",
        budget=3000,
        priorities=["Performance", "Battery Life", "Display Quality"]
    )
    
    # Show results
    agent.present_recommendations(recommendations)

# Run async function
asyncio.run(find_laptop())
```

---

## 🧪 Testing Your Setup

### Run All Tests

```bash
# Core functionality tests
python test_mina.py

# Integration tests
python test_integrations.py

# Or use pytest for both
pytest
```

Expected output:
```
Tests passed: 6/6
Integration Tests passed: 7/7
```

### Verify Each Integration

```python
from mina_agent import MinaAgent

agent = MinaAgent()

# Check what's configured
print("Integration Status:")
print(f"  Claude: {'✓' if agent.claude_client else '○'}")
print(f"  Browser Use: {'✓' if agent.browser else '○'}")
print(f"  Daytona: {'✓' if agent.daytona else '○'}")
```

---

## 🎯 Common Use Cases

### Use Case 1: Find a Premium Laptop

```python
import asyncio
from mina_agent import MinaAgent

async def main():
    agent = MinaAgent()
    
    recommendations = await agent.research_product_async(
        category="laptop",
        budget=3500,
        priorities=["Performance", "Display Quality", "Build Quality"]
    )
    
    # Top recommendation
    top = recommendations[0]
    print(f"Recommended: {top.product.name}")
    print(f"Price: ${top.product.price:,.2f}")
    print(f"Confidence: {top.confidence_score}%")

asyncio.run(main())
```

### Use Case 2: Research Office Furniture

```python
import asyncio
from mina_agent import MinaAgent

async def main():
    agent = MinaAgent()
    
    recommendations = await agent.research_product_async(
        category="furniture",
        budget=2000,
        priorities=["Durability", "Comfort", "Material Quality"]
    )
    
    # Show all recommendations
    agent.present_recommendations(recommendations)

asyncio.run(main())
```

### Use Case 3: Compare Appliances

```python
import asyncio
from mina_agent import MinaAgent

async def main():
    agent = MinaAgent()
    
    recommendations = await agent.research_product_async(
        category="appliance",
        budget=2500,
        priorities=["Energy Efficiency", "Reliability", "Capacity"]
    )
    
    # Compare top 3
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"\n#{i} - {rec.product.name}")
        print(f"  Confidence: {rec.confidence_score}%")
        print(f"  Price: ${rec.product.price:,.2f}")
        print(f"  Key Strengths: {', '.join(rec.pros[:2])}")

asyncio.run(main())
```

---

## 🐛 Troubleshooting

### "No module named 'mina_agent'"

Make sure you're in the Mina directory:
```bash
cd /path/to/Mina
python your_script.py
```

### "ImportError: cannot import name 'Anthropic'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### Agent uses fallback mode instead of real APIs

Check your `.env` file:
```bash
# Make sure keys are set (no quotes needed)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Not:
ANTHROPIC_API_KEY="sk-ant-xxxxx"  # ❌
ANTHROPIC_API_KEY=your-key-here    # ❌
```

### Tests fail with asyncio errors

Make sure you're using Python 3.8+:
```bash
python --version  # Should be 3.8 or higher
```

---

## 📚 Next Steps

Once you're up and running:

1. **Read the Full Documentation**: Check `README.md` for detailed features
2. **Explore Integration Guide**: See `BACKEND_INTEGRATIONS.md` for deep dives
3. **Try Examples**: Run scripts in the `examples/` directory
4. **Customize**: Modify priorities and categories for your needs
5. **Share Feedback**: Open an issue on GitHub with suggestions

---

## 💡 Tips for Best Results

1. **Be Specific with Priorities**: The more specific your priorities, the better the recommendations
2. **Realistic Budgets**: Set budgets that match actual product prices in your category
3. **Use Async**: For production use, prefer the async workflow for better performance
4. **Check Confidence Scores**: Higher scores (>80%) indicate more reliable recommendations
5. **Review Multiple Options**: Don't just pick #1, compare the top 3 recommendations

---

## 🆘 Getting Help

- **Documentation**: Check `README.md` and `BACKEND_INTEGRATIONS.md`
- **Examples**: See working code in `demo_integrations.py`
- **Tests**: Look at `test_mina.py` and `test_integrations.py` for usage patterns
- **Issues**: Open an issue on [GitHub](https://github.com/wildhash/Mina/issues)

---

Happy shopping with Mina! 🛍️
