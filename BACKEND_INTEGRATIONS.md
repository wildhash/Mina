# Backend Integration Guide

This guide provides detailed information about the three core backend integrations in Mina:

1. **Browser Use** - Multi-retailer web scraping
2. **Daytona** - Safe sandbox code execution
3. **Galileo** - Observability and confidence metrics

---

## 🌐 Browser Use Integration

### Overview

Browser Use provides cloud-based browser automation for scraping product data from retailers. It includes anti-bot protection and supports both local and cloud browsers.

### Setup

1. Get your API key from [cloud.browser-use.com](https://cloud.browser-use.com/) ($10 free credits)

2. Add to `.env`:
```bash
BROWSER_USE_API_KEY=your-key-here
```

3. The integration automatically detects and uses cloud browser when API key is present:
```python
agent = MinaAgent()
# agent.browser will use cloud mode if BROWSER_USE_API_KEY is set
```

### Key Capabilities

- **Cloud Browser**: Bypass anti-bot detection on major retailers
- **Async Operations**: Parallel scraping of multiple sites
- **Dynamic Content**: Handle JavaScript-rendered pages
- **Form Filling**: Automated search and filter interactions

### Usage Example

```python
async def scrape_retailers():
    agent = MinaAgent()
    
    requirements = {
        "category": "laptop",
        "budget_max": 3000,
        "priorities": ["Performance", "Battery Life"]
    }
    
    # Uses Browser Use internally
    products = await agent.scrape_retailers_async(requirements)
    return products
```

### Implementation Details

The `scrape_retailers_async` method in `mina_agent.py`:

```python
async def scrape_retailers_async(self, requirements: Dict[str, Any]) -> List[ProductOption]:
    """Use Browser Use to scrape multiple retailers asynchronously."""
    
    retailers = [
        ("Best Buy", "https://bestbuy.com"),
        ("Amazon", "https://amazon.com"),
    ]
    
    for name, url in retailers:
        agent = BrowserAgent(
            task=f"Find {category} products under ${budget}",
            browser=self.browser  # Cloud browser if API key present
        )
        result = await agent.run()
```

### Fallback Behavior

If Browser Use is not configured:
- Falls back to mock product data
- Agent still functions for testing/development
- Can be configured later without code changes

### Best Practices

1. **Use Cloud Browser in Production**: Avoids anti-bot detection
2. **Implement Rate Limiting**: Respect retailer policies
3. **Cache Results**: Reduce redundant scraping
4. **Error Handling**: Graceful degradation on scraping failures

---

## 🔒 Daytona Integration

### Overview

Daytona provides secure sandbox environments for executing data processing code. All code runs in isolated containers with sub-90ms creation time.

### Setup

1. Get your API key from [daytona.io](https://www.daytona.io/) ($200 free compute credits)

2. Add to `.env`:
```bash
DAYTONA_API_KEY=your-key-here
```

3. Install the package:
```bash
pip install daytona
```

### Key Capabilities

- **Fast Sandbox Creation**: Sub-90ms environment provisioning
- **File Operations**: Upload/download data to/from sandbox
- **Process Execution**: Run Python, pandas, numpy safely
- **Stateful Environments**: Long-running analysis tasks
- **Automatic Cleanup**: Removes sandbox after use

### Usage Example

```python
def process_data_safely():
    agent = MinaAgent()
    
    search_results = [
        {
            "retailer": "Best Buy",
            "products": [
                {"name": "Laptop A", "price": 1500, "rating": 4.5}
            ]
        }
    ]
    
    # Processes in isolated sandbox
    analyzed = agent.analyze_in_sandbox(search_results)
    return analyzed
```

### Implementation Details

The `analyze_in_sandbox` method in `mina_agent.py`:

```python
def analyze_in_sandbox(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Use Daytona sandbox for safe data processing."""
    
    # Create sandbox
    params = CreateSandboxParams(language="python")
    sandbox = self.daytona.create(params)
    
    # Upload data
    data_json = json.dumps(search_results)
    sandbox.fs.upload_file("/home/daytona/products.json", data_json.encode())
    
    # Run analysis code
    analysis_code = '''
import json
import pandas as pd

with open("/home/daytona/products.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df.to_json())
'''
    
    response = sandbox.process.code_run(analysis_code)
    
    # Clean up
    self.daytona.remove(sandbox)
    
    return json.loads(response.result)
```

### Fallback Behavior

If Daytona is not configured:
- Falls back to direct processing (no sandbox)
- Still performs all data operations
- Useful for development without API key

### Best Practices

1. **Always Clean Up**: Call `daytona.remove(sandbox)` in finally blocks
2. **Limit Sandbox Lifetime**: Don't keep sandboxes running unnecessarily
3. **Handle Errors**: Check `response.exit_code` before using results
4. **Use for Untrusted Code**: Never run user code directly

---

## 📊 Galileo Integration

### Overview

Galileo provides observability and evaluation for AI agents. It traces workflow execution and calculates confidence metrics.

### Setup

1. Get your API key from [galileo.ai](https://www.galileo.ai/)

2. Add to `.env`:
```bash
GALILEO_API_KEY=your-key-here
GALILEO_PROJECT=Mina-Shopping-Agent
GALILEO_LOG_STREAM=main
```

3. Install the package:
```bash
pip install galileo-sdk[openai]
```

### Key Capabilities

- **Workflow Tracing**: Automatic span creation for operations
- **LLM Logging**: Track all Claude API calls
- **Confidence Metrics**: Multi-factor confidence scoring
- **Real-time Monitoring**: Live dashboard of agent activity
- **Hallucination Detection**: Identify unreliable outputs

### Usage Example

```python
from galileo import log

@log(span_type="workflow")
def analyze_products(products):
    """This function is automatically traced by Galileo."""
    # Your analysis code
    return results

@log(span_type="llm")
def call_claude(prompt):
    """LLM calls are logged with input/output."""
    response = claude.messages.create(...)
    return response
```

### Implementation Details

Galileo context is initialized in `MinaAgent.__init__`:

```python
if GALILEO_AVAILABLE:
    galileo_api_key = os.getenv("GALILEO_API_KEY")
    if galileo_api_key:
        galileo_context.init(
            project=os.getenv("GALILEO_PROJECT", "Mina-Shopping-Agent"),
            log_stream=os.getenv("GALILEO_LOG_STREAM", "main")
        )
```

Key methods use `@log` decorators:

```python
@log(span_type="llm")
def analyze_with_claude(self, products, requirements):
    """Automatically logged to Galileo."""
    # Claude API calls here

@log(span_type="workflow")
def generate_recommendations(self, products, analyses, confidence_scores):
    """Workflow step logged with full context."""
    # Recommendation generation
```

### Confidence Score Methodology

Mina calculates confidence scores using multiple factors:

1. **Customer Ratings (25%)**: Normalized rating (0-5 → 0-1)
2. **Requirements Fit (40%)**: How well product matches priorities
3. **Review Confidence (20%)**: Based on review volume and consistency
4. **Data Completeness (15%)**: Availability of specifications

Implementation in `calculate_confidence_scores`:

```python
factors = {
    "rating": product.rating / 5.0,
    "fit_score": analysis["fit_score"] / 100.0,
    "review_confidence": 0.9 if product.rating >= 4.5 else 0.7,
    "data_completeness": 1.0 if product.specs else 0.6,
}

weights = {
    "rating": 0.25,
    "fit_score": 0.40,
    "review_confidence": 0.20,
    "data_completeness": 0.15
}

confidence = sum(factors[k] * weights[k] for k in factors.keys())
```

### Fallback Behavior

If Galileo is not configured:
- `@log` decorators become no-ops
- Functions execute normally without tracing
- Confidence scores still calculated locally
- No impact on functionality

### Best Practices

1. **Meaningful Span Names**: Use descriptive names for workflow steps
2. **Add Metadata**: Include confidence scores and metrics in spans
3. **Monitor Dashboard**: Regularly check Galileo console for issues
4. **Use Appropriate Span Types**: `workflow`, `llm`, `tool`, etc.

---

## 🔄 Integration Workflow

All three integrations work together in the async workflow:

```python
@log(span_type="workflow")
async def research_product_async(self, category, budget, priorities):
    """Complete workflow with all integrations."""
    
    # Step 1: Browser Use scraping
    search_results = await self.scrape_retailers_async(requirements)
    
    # Step 2: Daytona sandbox processing
    analyzed_data = self.analyze_in_sandbox(search_results)
    
    # Step 3: Claude analysis (Galileo logged)
    analyses = self.analyze_with_claude(products, requirements)
    
    # Step 4: Confidence scoring (Galileo logged)
    confidence_scores = self.calculate_confidence_scores(products, analyses)
    
    # Step 5: Generate recommendations (Galileo logged)
    recommendations = self.generate_recommendations(
        products, analyses, confidence_scores
    )
    
    return recommendations
```

### Flow Diagram

```
User Input
    ↓
┌─────────────────────────────────────────┐
│  Browser Use Cloud Scraping             │
│  - Best Buy, Amazon, B&H Photo          │
│  - Anti-bot protection                  │
│  - Parallel async operations            │
└─────────────────────────────────────────┘
    ↓ Raw product data
┌─────────────────────────────────────────┐
│  Daytona Sandbox Processing             │
│  - Safe pandas/numpy execution          │
│  - Data cleaning and aggregation        │
│  - Isolated environment                 │
└─────────────────────────────────────────┘
    ↓ Structured data
┌─────────────────────────────────────────┐
│  Claude AI Analysis (Galileo Logged)    │
│  - Spec analysis                        │
│  - Requirements matching                │
│  - Pros/cons identification             │
└─────────────────────────────────────────┘
    ↓ Analysis results
┌─────────────────────────────────────────┐
│  Confidence Scoring (Galileo Logged)    │
│  - Multi-factor calculation             │
│  - Transparent methodology              │
│  - Weighted scoring                     │
└─────────────────────────────────────────┘
    ↓ Recommendations
User Output
```

---

## 🧪 Testing Integrations

### Unit Tests

Test each integration independently:

```bash
python test_integrations.py
```

Tests include:
- Browser Use initialization
- Daytona sandbox creation and cleanup
- Galileo decorator compatibility
- Async workflow execution
- Fallback mechanisms

### Manual Testing

Test with API keys:

```bash
# Set environment variables
export ANTHROPIC_API_KEY=sk-ant-xxx
export BROWSER_USE_API_KEY=your-key
export DAYTONA_API_KEY=your-key
export GALILEO_API_KEY=your-key

# Run demo
python demo_integrations.py
```

Test without API keys (fallback mode):

```bash
# No environment variables set
python demo_integrations.py
```

### Integration Checklist

- [ ] Browser Use scrapes at least one retailer
- [ ] Daytona sandbox creates and executes code
- [ ] Galileo logs appear in console
- [ ] Claude API returns valid analysis
- [ ] Confidence scores calculated correctly
- [ ] Fallbacks work when API keys missing
- [ ] Async workflow completes successfully

---

## 🚨 Troubleshooting

### Browser Use Issues

**Problem**: Scraping fails with timeout
- **Solution**: Increase timeout in BrowserAgent configuration
- **Solution**: Use cloud browser mode (set BROWSER_USE_API_KEY)

**Problem**: Anti-bot detection
- **Solution**: Always use cloud browser in production
- **Solution**: Add delays between requests

### Daytona Issues

**Problem**: Sandbox creation fails
- **Solution**: Check DAYTONA_API_KEY is valid
- **Solution**: Verify daytona package installed

**Problem**: Code execution timeout
- **Solution**: Simplify analysis code
- **Solution**: Process data in smaller batches

### Galileo Issues

**Problem**: No traces appear in dashboard
- **Solution**: Verify GALILEO_API_KEY is set
- **Solution**: Check project and stream names match
- **Solution**: Ensure galileo_context.init() is called

**Problem**: @log decorator not working
- **Solution**: Check galileo-sdk is installed
- **Solution**: Verify GALILEO_AVAILABLE flag is True

---

## 📚 Additional Resources

- [Browser Use Documentation](https://browser-use.com/docs)
- [Daytona Documentation](https://www.daytona.io/docs)
- [Galileo Documentation](https://docs.galileo.ai/)
- [Claude API Reference](https://docs.anthropic.com/)

---

## 🤝 Contributing

To add new integrations:

1. Add package to `requirements.txt`
2. Add graceful import in `mina_agent.py`
3. Initialize in `MinaAgent.__init__`
4. Add fallback behavior
5. Write integration tests
6. Update this documentation
