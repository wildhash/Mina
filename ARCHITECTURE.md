# Mina Architecture

## System Overview

Mina is an AI-powered shopping concierge designed to help users make confident high-end purchase decisions ($500+). The system combines web automation, AI analysis, and transparent confidence scoring to provide comprehensive product recommendations.

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INPUT                           │
│  (Category, Budget, Priorities, Specific Requirements)       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       MINA AGENT                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Requirements Gathering                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  2. Multi-Retailer Research (Browser Use)            │   │
│  │     • Amazon, Best Buy, B&H Photo                    │   │
│  │     • Newegg, Wayfair, Direct Manufacturers          │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  3. AI Analysis (Claude)                             │   │
│  │     • Specification comparison                       │   │
│  │     • Review sentiment analysis                      │   │
│  │     • Value assessment                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  4. Confidence Scoring (Galileo Methodology)         │   │
│  │     • Multi-factor analysis                          │   │
│  │     • Weighted scoring                               │   │
│  │     • Uncertainty quantification                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  5. Recommendation Generation                        │   │
│  │     • Ranked by confidence                           │   │
│  │     • Detailed reasoning                             │   │
│  │     • Pros/cons analysis                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER RECOMMENDATIONS                      │
│  • Top 3 options with confidence scores                     │
│  • Detailed specifications                                  │
│  • Clear reasoning and transparency                         │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Core Agent (`mina_agent.py`)

**Class: `MinaAgent`**

The main orchestrator that coordinates all components.

**Key Methods:**
- `get_product_category()` - Interactive category selection
- `gather_requirements()` - Collect user preferences
- `browse_retailers()` - Multi-retailer product discovery
- `analyze_with_claude()` - AI-powered analysis
- `calculate_confidence_scores()` - Galileo-inspired scoring
- `generate_recommendations()` - Create final recommendations
- `present_recommendations()` - Display results to user

**Data Flow:**
```
Requirements → Products → Analysis → Confidence → Recommendations → Presentation
```

### 2. Data Models

**ProductCategory (Enum)**
```python
- LAPTOP
- FURNITURE  
- APPLIANCE
```

**ProductOption (Dataclass)**
```python
{
    name: str
    price: float
    retailer: str
    url: str
    specs: Dict[str, Any]
    reviews_summary: str
    rating: float
}
```

**Recommendation (Dataclass)**
```python
{
    product: ProductOption
    confidence_score: float
    reasoning: str
    pros: List[str]
    cons: List[str]
}
```

### 3. External Integrations

#### Browser Use Integration
```
Purpose: Automated web browsing for product discovery
Status: Framework ready, implementation pending
Location: browse_retailers() method
```

Currently uses mock data for demonstration. In production:
1. Initialize browser agent
2. Navigate to retailer websites
3. Search for products matching criteria
4. Extract product details (name, price, specs, reviews)
5. Aggregate results from multiple retailers

#### Claude (Anthropic) Integration
```
Purpose: AI-powered product analysis
Status: API ready, using rule-based fallback
Location: analyze_with_claude() method
```

Analyzes:
- Product specifications against user requirements
- Review sentiment and common themes
- Value proposition assessment
- Competitive positioning

#### Galileo.ai Methodology
```
Purpose: Transparent confidence scoring
Status: Implemented with custom algorithm
Location: calculate_confidence_scores() method
```

Multi-factor scoring:
- Customer ratings (25%)
- Requirements fit (40%)
- Review confidence (20%)
- Data completeness (15%)

## Workflow Details

### Phase 1: Requirements Gathering

1. **Category Selection**
   - Present 3 categories: Laptop, Furniture, Appliance
   - Each category has specialized priorities
   - Validate user input

2. **Budget Definition**
   - Minimum: $500 (high-end threshold)
   - User specifies maximum budget
   - Used for filtering results

3. **Priority Selection**
   - Category-specific priority options
   - Multiple selections allowed
   - Weights analysis and scoring

4. **Specific Requirements**
   - Free-text input for unique needs
   - Used in Claude analysis
   - Provides context for recommendations

### Phase 2: Multi-Retailer Research

Current Implementation (Mock):
- Predefined product database
- Filtered by category and budget
- Returns top options

Production Implementation:
```python
def browse_retailers(self, requirements):
    browser = BrowserAgent()
    results = []
    
    for retailer in self.enabled_retailers:
        # Navigate and search
        products = browser.search(
            site=retailer,
            category=requirements['category'],
            max_price=requirements['budget_max']
        )
        
        # Extract structured data
        for product in products:
            results.append(ProductOption(
                name=product.title,
                price=product.price,
                retailer=retailer,
                url=product.url,
                specs=product.specifications,
                reviews_summary=product.review_summary,
                rating=product.average_rating
            ))
    
    return self._deduplicate_and_rank(results)
```

### Phase 3: AI Analysis

**Input:**
- Product specifications
- Customer reviews
- User requirements

**Processing:**
- Match specs to priorities
- Analyze review sentiment
- Assess value proposition
- Identify strengths and weaknesses

**Output:**
```python
{
    "product": product_name,
    "strengths": [list of strengths],
    "weaknesses": [list of considerations],
    "fit_score": 0-100,
    "value_assessment": "description"
}
```

### Phase 4: Confidence Scoring

**Calculation Method:**

```python
confidence = (
    (rating / 5.0) * 0.25 +           # Customer ratings
    (fit_score / 100.0) * 0.40 +      # Match to requirements
    review_confidence * 0.20 +         # Review quality
    data_completeness * 0.15           # Data availability
) * 100
```

**Adjustments:**
- Penalty for limited data
- Penalty for mixed reviews
- Boost for exceptional ratings

**Output:** 0-100% confidence score

### Phase 5: Recommendation Generation

**Ranking:**
1. Sort by confidence score (descending)
2. Present top N recommendations (default: 3)

**Content:**
- Product details and pricing
- Key specifications
- Strengths (pros)
- Considerations (cons)
- Detailed reasoning
- Confidence score explanation

### Phase 6: Presentation

**Format:**
```
┌─────────────────────────────────────────────┐
│  #1 RECOMMENDATION - 85.5% Confidence       │
├─────────────────────────────────────────────┤
│  📦 Product Name                            │
│  💰 Price: $X,XXX.XX                        │
│  🏪 Retailer: Store Name                    │
│  ⭐ Rating: X.X/5.0                         │
│                                             │
│  📋 KEY SPECIFICATIONS:                     │
│     • Spec 1                                │
│     • Spec 2                                │
│                                             │
│  ✅ STRENGTHS:                              │
│     • Strength 1                            │
│     • Strength 2                            │
│                                             │
│  ⚠️  CONSIDERATIONS:                        │
│     • Consideration 1                       │
│                                             │
│  💡 WHY THIS RECOMMENDATION:                │
│     Detailed reasoning...                   │
│                                             │
│  🔗 Learn more: URL                         │
└─────────────────────────────────────────────┘
```

## Configuration

### config.ini Structure

```ini
[agent]
min_price = 500
max_products = 5
verbose = false

[retailers]
enabled_retailers = Amazon, Best Buy, ...

[confidence_scoring]
rating_weight = 0.25
fit_score_weight = 0.40
review_confidence_weight = 0.20
data_completeness_weight = 0.15
min_confidence_threshold = 60.0

[analysis]
num_recommendations = 3

[output]
format = cli
use_colors = true
```

## Scalability Considerations

### Horizontal Scaling
- Parallel retailer searches
- Batch product analysis
- Distributed confidence scoring

### Caching Strategy
```
Product Data Cache:
- TTL: 24 hours
- Key: category + price_range + date
- Invalidation: manual or scheduled

Analysis Cache:
- TTL: 7 days  
- Key: product_id + requirements_hash
- Invalidation: on product update
```

### Rate Limiting
- Browser automation: 1 req/sec per retailer
- Claude API: Per Anthropic limits
- Galileo API: Per service limits

## Security Considerations

### API Keys
- Store in environment variables
- Never commit to repository
- Rotate regularly
- Use different keys per environment

### User Privacy
- Don't log search queries
- Don't store personal preferences
- Anonymize analytics data
- GDPR compliance for EU users

### Data Validation
- Sanitize user inputs
- Validate product data
- Check price bounds
- Verify URLs

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Edge case coverage

### Integration Tests
- API connectivity
- Browser automation
- End-to-end workflow

### Performance Tests
- Response time < 30s per category
- Handle 100+ products
- Parallel processing

## Future Enhancements

1. **Price Tracking**
   - Historical price data
   - Deal alerts
   - Best time to buy

2. **Comparison View**
   - Side-by-side comparison
   - Feature matrix
   - Price-performance charts

3. **User Accounts**
   - Save preferences
   - Track recommendations
   - Purchase history

4. **Mobile App**
   - iOS/Android apps
   - Push notifications
   - Barcode scanning

5. **Social Features**
   - Share recommendations
   - Community reviews
   - Expert opinions

6. **Expanded Categories**
   - TVs and displays
   - Cameras and lenses
   - Watches and jewelry
   - Home audio systems

## Monitoring and Observability

### Metrics
- Request volume
- Response times
- Success rates
- Error rates
- API usage

### Logging
```python
logger.info("User started session", extra={
    "category": category,
    "budget": budget,
    "timestamp": timestamp
})

logger.warning("Low confidence score", extra={
    "product": product_name,
    "score": confidence,
    "reason": reason
})

logger.error("API failure", extra={
    "service": "Claude",
    "error": error_message,
    "retry_count": retries
})
```

### Alerts
- API failures
- High error rates
- Slow response times
- Quota exhaustion

## Development Environment

### Daytona.io Setup
```yaml
name: mina-agent
image: python:3.11
ports:
  - 8000
env:
  - ANTHROPIC_API_KEY
setup:
  - pip install -r requirements.txt
  - playwright install chromium
```

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
python test_mina.py

# Run demo
python demo.py

# Run CLI
python mina_cli.py
```

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "mina_cli.py"]
```

### Cloud Deployment
- AWS Lambda (serverless)
- Google Cloud Run
- Azure Container Instances
- Heroku

## License

MIT License - See LICENSE file

## Contributing

See CONTRIBUTING.md for guidelines

## Support

- Documentation: README.md, INTEGRATION.md
- Issues: GitHub Issues  
- For questions or feedback, please open a GitHub issue
