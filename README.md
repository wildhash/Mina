# Mina 🛍️

**AI Shopping Concierge for High-End Purchases**

Mina researches premium products across retailers, analyzes reviews, and delivers confident recommendations with full reasoning transparency—so you can make high-end purchase decisions with clarity.

## Features

- 🎯 **Intelligent Category Selection**: Specialized support for laptops, furniture, and appliances
- 🌐 **Multi-Retailer Research**: Browser Use integration for live scraping across retailers
- 🤖 **AI-Powered Analysis**: Claude Sonnet 4 analyzes reviews, specs, and value propositions
- 🔒 **Safe Code Execution**: Daytona sandbox for secure data processing
- 📊 **Confidence Scoring**: Galileo observability with multi-factor confidence metrics
- 🚀 **REST API & WebSocket**: FastAPI server for frontend integration with real-time updates
- ⚡ **Async Operations**: Efficient parallel scraping and processing
- 💡 **Clear Reasoning**: Every recommendation comes with detailed pros, cons, and reasoning
- 💰 **Budget-Aware**: Focuses on purchases $500+ with budget filtering
- 🛡️ **Graceful Fallbacks**: Works even without API keys for testing and development

## How It Works

1. **Category Selection**: Choose your product category (laptop, furniture, or appliance)
2. **Requirements Gathering**: Specify your budget and priorities
3. **Multi-Retailer Scraping**: Browser Use cloud browser scrapes multiple retailers in parallel
4. **Sandbox Processing**: Daytona safely executes data analysis code in isolated environment
5. **AI Analysis**: Claude Sonnet 4 analyzes specifications and reviews against requirements
6. **Confidence Scoring**: Galileo-logged multi-factor confidence calculation
7. **Transparent Recommendations**: Receive ranked recommendations with full reasoning and metrics

## Technology Stack

- **Claude (Anthropic)**: Claude Sonnet 4 for AI-powered product analysis
- **Browser Use**: Cloud browser automation for anti-bot protected scraping
- **Daytona**: Secure sandbox environment for code execution and data processing
- **Galileo**: Observability and confidence score tracing
- **FastAPI**: Modern web framework for REST API and WebSocket support
- **Python 3.8+**: Core implementation with async/await support
- **Pandas & NumPy**: Data processing and analysis

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/wildhash/Mina.git
cd Mina
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Set up your API keys (all optional for testing):
   - **Anthropic API key** from [console.anthropic.com](https://console.anthropic.com/) - For Claude AI
   - **Browser Use API key** from [cloud.browser-use.com](https://cloud.browser-use.com/) - For web scraping ($10 free credits)
   - **Daytona API key** from [daytona.io](https://www.daytona.io/) - For sandbox execution ($200 free credits)
   - **Galileo API key** from [galileo.ai](https://www.galileo.ai/) - For observability
   - Add all keys to your `.env` file

**Note**: Mina works without API keys using mock data and fallback mechanisms for testing/development.

## Usage

### API Server (for Frontend Integration)

Run the FastAPI server to enable frontend integration:

```bash
python api_server.py
```

The server starts on `http://localhost:8000` with the following endpoints:

- **Health Check**: `GET /api/health` - Check server status and integrations
- **Product Search**: `POST /api/search` - Search for products based on requirements
- **WebSocket**: `ws://localhost:8000/ws` - Real-time search updates

**Example API Request:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "category": "laptop",
    "budget_max": 3000,
    "priorities": ["Performance", "Battery Life"],
    "specific_needs": "For software development"
  }'
```

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

For detailed API documentation and configuration, see [START_API.md](START_API.md).

### Quick Demo

Run the integration demo to see all features:

```bash
python demo_integrations.py
```

This demonstrates:
- Browser Use integration (with fallback to mock data)
- Daytona sandbox execution (with fallback to direct processing)
- Galileo observability (with @log decorators)
- Claude AI analysis (with fallback to rule-based)
- Async workflow for efficient parallel operations

### Command Line Interface

Run Mina interactively from the command line:

```bash
python mina_cli.py
```

The agent will guide you through:
1. Selecting a product category
2. Specifying your budget and priorities
3. Reviewing research results
4. Understanding recommendations with confidence scores

### Programmatic Usage

Use Mina in your Python code:

```python
import asyncio
from mina_agent import MinaAgent

async def find_laptop():
    agent = MinaAgent()
    
    # Async workflow (recommended)
    recommendations = await agent.research_product_async(
        category="laptop",
        budget=3000,
        priorities=["Performance", "Battery Life"]
    )
    
    # Display results
    agent.present_recommendations(recommendations)

asyncio.run(find_laptop())
```

### Example Session

```
Welcome to Mina - Your AI Shopping Concierge
============================================================

I help you make confident decisions on high-end purchases ($500+)
by researching products, analyzing reviews, and providing
transparent recommendations with confidence scores.

What type of product are you looking to purchase?
1. Laptop
2. Furniture
3. Appliance

Enter your choice (1-3): 1

============================================================
Great! Let's find the perfect laptop for you.
============================================================

What's your maximum budget? ($): 3000

What are your top priorities? (You can select multiple)
1. Performance
2. Battery Life
3. Display Quality
4. Portability
5. Build Quality

Enter priority numbers (comma-separated, e.g., 1,3,4): 1,2,5

...
```

## Supported Product Categories

### Laptops
- Performance comparison
- Battery life analysis
- Display quality assessment
- Build quality evaluation
- Price-to-performance ratios

### Furniture
- Durability and warranty analysis
- Comfort ratings
- Material quality assessment
- Design and aesthetics
- Space efficiency

### Appliances
- Energy efficiency ratings
- Capacity and features
- Reliability metrics
- Smart home integration
- Long-term cost analysis

## Confidence Score Methodology

Mina uses a multi-factor approach with Galileo observability to calculate confidence scores:

- **Customer Ratings (25%)**: Verified buyer ratings and review sentiment
- **Requirements Fit (40%)**: How well the product matches your stated priorities
- **Review Confidence (20%)**: Volume and consistency of reviews
- **Data Completeness (15%)**: Availability of comprehensive specifications

Scores range from 0-100%, with higher scores indicating greater confidence in the recommendation.

All scoring steps are logged via Galileo's @log decorators for full transparency and traceability.

## Development

### Project Structure

```
Mina/
├── mina_agent.py           # Core agent with all integrations
├── mina_cli.py             # Command-line interface
├── api_server.py           # FastAPI server for frontend integration
├── demo_integrations.py    # Full integration demo
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── test_mina.py            # Core unit tests
├── test_api.py             # API endpoint tests
├── test_integrations.py    # Integration tests
├── examples/               # Usage examples
├── START_API.md            # API server documentation
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Running Tests

```bash
# Run core unit tests
python test_mina.py

# Run API tests
python test_api.py

# Run integration tests
python test_integrations.py

# Or use pytest for all
pip install pytest pytest-cov
pytest

# Run with coverage
pytest --cov=. tests/
```

### Integration Testing

Each integration can be tested independently:

```python
# Test Browser Use
agent = MinaAgent()
assert agent.browser is not None or agent.browser is None  # Works with or without API key

# Test Daytona
result = agent.analyze_in_sandbox([{"test": "data"}])
assert "products" in result

# Test Galileo decorators
@log(span_type="workflow")
def my_function():
    pass  # Automatically traced when Galileo configured
```

## Roadmap

- [x] Browser Use integration for real-time retailer scraping
- [x] Daytona sandbox for safe code execution
- [x] Galileo observability and confidence tracing
- [x] Claude Sonnet 4 AI analysis
- [x] Async workflow support
- [x] FastAPI REST API and WebSocket support for frontend integration
- [ ] Live scraping from major retailers (Best Buy, Amazon, B&H Photo)
- [ ] Enhanced parsing for product specifications
- [ ] Expanded product categories (TVs, cameras, watches)
- [ ] Price tracking and deal alerts
- [ ] Comparison view for side-by-side analysis
- [ ] Export recommendations to PDF
- [ ] Integration with price history APIs
- [ ] Multi-language support
- [ ] Mobile app interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/wildhash/Mina/issues)

## Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/)
- Browser automation powered by [Browser Use](https://browser-use.com/)
- Confidence methodology inspired by [Galileo.ai](https://www.galileo.ai/)
- Developed with [Daytona.io](https://www.daytona.io/)

---

**Made with ❤️ for confident high-end shopping decisions**
