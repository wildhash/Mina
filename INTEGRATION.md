# Mina Integration Guide

This guide explains how to integrate Mina with external services for production use.

## Table of Contents

1. [Claude (Anthropic) Integration](#claude-integration)
2. [Browser Use Integration](#browser-use-integration)
3. [Galileo.ai Integration](#galileo-integration)
4. [Daytona.io Development](#daytona-development)

---

## Claude Integration

Mina uses Claude for intelligent analysis of product specifications and reviews.

### Setup

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)

2. Add to your `.env` file:
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Implementation

The agent automatically detects the API key and uses Claude for analysis:

```python
from mina_agent import MinaAgent

# Automatically loads from environment
agent = MinaAgent()

# Or pass explicitly
agent = MinaAgent(anthropic_api_key="sk-ant-xxxxx")
```

### Advanced Usage

To customize Claude's analysis behavior, modify the `analyze_with_claude()` method:

```python
def analyze_with_claude(self, products, requirements):
    if self.claude_client:
        # Use Claude API for real analysis
        response = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Analyze these products: {products}"
            }]
        )
        # Process response
    else:
        # Fallback to rule-based analysis
        pass
```

---

## Browser Use Integration

Browser Use enables automated web browsing for real-time product research.

### Setup

1. Install browser-use:
```bash
pip install browser-use playwright
playwright install chromium
```

2. Update `browse_retailers()` method in `mina_agent.py`:

```python
from browser_use import Agent as BrowserAgent

def browse_retailers(self, requirements):
    browser_agent = BrowserAgent()
    
    retailers = [
        "https://www.amazon.com",
        "https://www.bestbuy.com",
        "https://www.bhphotovideo.com"
    ]
    
    products = []
    
    for retailer in retailers:
        # Use browser agent to search and extract product data
        results = browser_agent.browse(
            url=retailer,
            search_query=f"{requirements['category']} under ${requirements['budget_max']}"
        )
        
        products.extend(self._parse_retailer_results(results))
    
    return products
```

### Browser Configuration

Configure browser behavior in `config.ini`:

```ini
[browser]
headless = true
timeout = 30
user_agent = Mozilla/5.0...
```

### Retailer-Specific Scrapers

Create custom parsers for each retailer:

```python
def _parse_amazon_results(self, html):
    """Parse Amazon product listings."""
    # Implementation
    pass

def _parse_bestbuy_results(self, html):
    """Parse Best Buy product listings."""
    # Implementation
    pass
```

---

## Galileo.ai Integration

Galileo provides confidence scoring and uncertainty quantification.

### Concept

Mina uses Galileo-inspired methodology for confidence scores:

1. **Multi-Factor Analysis**: Rating, fit score, review confidence, data completeness
2. **Weighted Scoring**: Configurable weights for each factor
3. **Uncertainty Quantification**: Transparent confidence percentages
4. **Explainability**: Clear reasoning for each score

### Configuration

Adjust scoring weights in `config.ini`:

```ini
[confidence_scoring]
rating_weight = 0.25
fit_score_weight = 0.40
review_confidence_weight = 0.20
data_completeness_weight = 0.15
```

### Custom Scoring Logic

Extend the confidence calculation:

```python
def calculate_confidence_scores(self, products, analyses):
    confidence_scores = []
    
    for product, analysis in zip(products, analyses):
        # Base factors
        factors = {
            "rating": product.rating / 5.0,
            "fit_score": analysis["fit_score"] / 100.0,
            "review_confidence": self._calculate_review_confidence(product),
            "data_completeness": self._calculate_data_completeness(product)
        }
        
        # Add custom factors
        if hasattr(product, 'warranty_years'):
            factors["warranty"] = min(product.warranty_years / 12.0, 1.0)
        
        # Calculate weighted score
        confidence = self._weighted_average(factors)
        confidence_scores.append(confidence * 100)
    
    return confidence_scores
```

### Galileo API Integration (Future)

If using Galileo's actual API:

```python
import galileo

def calculate_confidence_scores(self, products, analyses):
    galileo_client = galileo.Client(api_key=os.getenv("GALILEO_API_KEY"))
    
    scores = []
    for product, analysis in zip(products, analyses):
        score = galileo_client.evaluate(
            data=product,
            analysis=analysis,
            model="confidence-v1"
        )
        scores.append(score.confidence * 100)
    
    return scores
```

---

## Daytona.io Development

Daytona provides standardized development environments.

### Setup

1. Install Daytona CLI:
```bash
curl -sf https://download.daytona.io/daytona/install.sh | sh
```

2. Create workspace:
```bash
daytona create https://github.com/wildhash/Mina
```

### Workspace Configuration

Create `.daytona/config.yaml`:

```yaml
name: mina-agent
image: python:3.11
ports:
  - 8000
env:
  - ANTHROPIC_API_KEY
  - GALILEO_API_KEY
setup:
  - pip install -r requirements.txt
  - playwright install chromium
```

### Development Workflow

```bash
# Start workspace
daytona code

# Run tests
daytona exec pytest

# Run demo
daytona exec python demo.py
```

---

## Production Deployment

### Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y chromium
RUN playwright install chromium

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "mina_cli.py"]
```

### Environment Variables

Required for production:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
BROWSER_USE_HEADLESS=true
GALILEO_API_KEY=galileo_xxxxx  # Optional
```

### Monitoring

Add logging and monitoring:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('mina')

# In your code
logger.info(f"Analyzing product: {product.name}")
logger.warning(f"No products found within budget")
logger.error(f"API error: {error}")
```

---

## Testing

### Integration Tests

Test external service integrations:

```python
def test_claude_integration():
    """Test Claude API integration."""
    agent = MinaAgent(anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))
    assert agent.claude_client is not None

def test_browser_use():
    """Test browser automation."""
    # Implementation
    pass
```

### Mocking External Services

For CI/CD without API keys:

```python
from unittest.mock import Mock, patch

@patch('mina_agent.Anthropic')
def test_agent_without_api_key(mock_anthropic):
    mock_anthropic.return_value = Mock()
    agent = MinaAgent()
    # Test logic
```

---

## Best Practices

1. **API Rate Limiting**: Implement rate limiting for external APIs
2. **Caching**: Cache product data to reduce API calls
3. **Error Handling**: Graceful degradation when services are unavailable
4. **Privacy**: Don't log sensitive user data or API keys
5. **Testing**: Test with and without external service access

---

## Support

For integration issues:
- Documentation: [Mina Docs](https://github.com/wildhash/Mina)
- Issues: [GitHub Issues](https://github.com/wildhash/Mina/issues)
- For questions or feedback, please open a GitHub issue
