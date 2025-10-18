# Mina 🛍️

**AI Shopping Concierge for High-End Purchases**

Mina researches premium products across retailers, analyzes reviews, and delivers confident recommendations with full reasoning transparency—so you can make high-end purchase decisions with clarity.

## Features

- 🎯 **Intelligent Category Selection**: Specialized support for laptops, furniture, and appliances
- 🌐 **Multi-Retailer Research**: Automatically browses top retailers to find the best options
- 🤖 **AI-Powered Analysis**: Uses Claude to analyze reviews, specs, and value propositions
- 📊 **Confidence Scoring**: Galileo-inspired methodology provides transparent confidence scores
- 💡 **Clear Reasoning**: Every recommendation comes with detailed pros, cons, and reasoning
- 💰 **Budget-Aware**: Focuses on purchases $500+ with budget filtering

## How It Works

1. **Category Selection**: Choose your product category (laptop, furniture, or appliance)
2. **Requirements Gathering**: Specify your budget and priorities
3. **Multi-Retailer Browse**: Mina searches across multiple retailers using browser automation
4. **AI Analysis**: Claude analyzes specifications and reviews against your requirements
5. **Confidence Scoring**: Galileo methodology calculates confidence scores based on multiple factors
6. **Transparent Recommendations**: Receive ranked recommendations with full reasoning

## Technology Stack

- **Claude (Anthropic)**: AI-powered review and specification analysis
- **Browser Use**: Automated web browsing for retailer research
- **Galileo.ai**: Confidence score methodology for decision support
- **Python**: Core implementation language

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

4. Set up your API keys:
   - Get your Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
   - Add it to your `.env` file

## Usage

### Command Line Interface

Run Mina from the command line:

```bash
python mina_cli.py
```

The agent will guide you through:
1. Selecting a product category
2. Specifying your budget and priorities
3. Reviewing research results
4. Understanding recommendations with confidence scores

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

Mina uses a multi-factor approach inspired by Galileo.ai to calculate confidence scores:

- **Customer Ratings (25%)**: Verified buyer ratings and review sentiment
- **Requirements Fit (40%)**: How well the product matches your stated priorities
- **Review Confidence (20%)**: Volume and consistency of reviews
- **Data Completeness (15%)**: Availability of comprehensive specifications

Scores range from 0-100%, with higher scores indicating greater confidence in the recommendation.

## Development

### Project Structure

```
Mina/
├── mina_agent.py      # Core agent implementation
├── mina_cli.py        # Command-line interface
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

## Roadmap

- [ ] Live browser-use integration for real-time retailer scraping
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
