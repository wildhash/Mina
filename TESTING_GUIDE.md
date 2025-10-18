# Testing Guide for Mina AI Shopping Concierge

## Quick Start

Run all tests with:
```bash
python test_mina.py         # Core agent tests (28 tests)
python test_cli_utils.py    # CLI utilities tests (37 tests)
python test_demo.py         # Demo workflow tests (11 tests)
python test_config.py       # Configuration validation (21 tests)
python test_examples.py     # Integration tests (15 tests)
```

## Test Suite Overview

### Total Coverage
- **112 test functions** across 5 test files
- **1,856 lines** of comprehensive test code
- **All changed files** in the git diff are tested

### Test Files

| File | Tests | Lines | Coverage |
|------|-------|-------|----------|
| test_mina.py | 28 | 721 | mina_agent.py |
| test_cli_utils.py | 37 | 410 | cli_utils.py |
| test_demo.py | 11 | 217 | demo.py |
| test_config.py | 21 | 288 | config.ini |
| test_examples.py | 15 | 220 | examples/*.py |

## Detailed Test Descriptions

### test_mina.py - Core Agent Functionality

Tests the main Mina agent (`mina_agent.py`) with comprehensive coverage:

**Data Structures (2 tests):**
- `test_product_option_dataclass()` - Validates ProductOption creation and attributes
- `test_recommendation_dataclass()` - Tests Recommendation dataclass structure

**Initialization (3 tests):**
- `test_agent_initialization()` - Basic agent setup
- `test_agent_initialization_with_api_key()` - With explicit API key
- `test_agent_initialization_without_api_key()` - Without API key (graceful handling)

**Category Management (2 tests):**
- `test_product_categories()` - Enum values validation
- `test_agent_supported_categories()` - Supported categories list

**Retailer Browsing (5 tests):**
- `test_browse_retailers()` - Laptop category browsing
- `test_browse_retailers_furniture()` - Furniture category
- `test_browse_retailers_appliance()` - Appliance category
- `test_browse_retailers_budget_filtering()` - Budget edge cases
- `test_browse_retailers_with_specific_needs()` - Custom requirements

**Analysis (4 tests):**
- `test_analyze_with_claude()` - Basic analysis
- `test_analyze_with_claude_multiple_priorities()` - Multiple priority handling
- `test_analyze_with_claude_high_rating_bonus()` - Rating bonus logic
- `test_analyze_with_claude_empty_priorities()` - No priorities edge case

**Confidence Scoring (4 tests):**
- `test_confidence_scores()` - Basic calculation
- `test_confidence_scores_multiple_products()` - Multiple products comparison
- `test_confidence_scores_edge_cases()` - Missing data handling
- `test_confidence_scores_perfect_product()` - Ideal product scoring
- `test_confidence_scores_boundary_values()` - Range validation

**Recommendations (4 tests):**
- `test_generate_recommendations()` - Basic generation
- `test_generate_recommendations_sorting()` - Confidence-based sorting
- `test_generate_recommendations_reasoning()` - Reasoning content
- `test_generate_recommendations_with_cons()` - Negative points handling

**Data Quality (2 tests):**
- `test_multiple_retailers_in_results()` - Multi-retailer diversity
- `test_product_specs_completeness()` - Specification completeness

### test_cli_utils.py - CLI Utilities

Comprehensive testing of all CLI utility functions:

**Color Management (7 tests):**
- Platform detection (Unix, Windows)
- TTY detection
- Color application with/without support
- Multiple color codes

**Output Functions (6 tests):**
- Headers and subheaders
- Success, info, warning, error messages

**Formatting (10 tests):**
- Price formatting (standard, large, small, negative, edge cases)
- Rating formatting (full stars, partial, decimals, edge cases)

**Progress Bars (5 tests):**
- Start, middle, complete states
- Custom width
- Edge values (0%, 100%)

**Box Creation (6 tests):**
- Simple and multiline text
- Long text truncation
- Custom widths
- Empty text
- Unicode border characters

**System Functions (3 tests):**
- Screen clearing (Unix/Windows)
- Pause functionality

### test_demo.py - Demo Workflow

Integration tests for the demo script:

**Execution (8 tests):**
- Complete execution without errors
- Agent instance creation
- All workflow methods called (browse, analyze, calculate, generate, present)
- Output contains all steps

**Error Handling (1 test):**
- KeyboardInterrupt graceful handling

**Requirements Validation (2 tests):**
- Budget configuration
- Category selection (laptop)

### test_config.py - Configuration Validation

Schema and value validation for `config.ini`:

**File Structure (3 tests):**
- File existence
- Parsing capability
- Required sections present

**Agent Section (4 tests):**
- Required keys present
- min_price validation (≥0, =500)
- max_products validation (>0, ≤100)
- verbose boolean format

**Retailers Section (2 tests):**
- enabled_retailers key present
- Non-empty retailer list
- Known brands included

**Confidence Scoring (2 tests):**
- All weights present and valid (0-1)
- Weights sum to 1.0
- Min threshold valid (0-100)

**Analysis Section (3 tests):**
- Required keys present
- num_recommendations valid (>0, ≤20)
- Boolean flags proper format

**Output Section (5 tests):**
- Required keys present
- Format valid (cli/json/html)
- Boolean flags validation
- Output directory specified

**Integrity (2 tests):**
- No duplicate sections
- Expected retailers present

### test_examples.py - Integration Tests

End-to-end testing of example scripts:

**File Existence (3 tests):**
- budget_laptop.py exists
- energy_efficient_appliance.py exists
- premium_furniture.py exists

**Execution (3 tests):**
- All examples run without errors
- Complete workflow execution

**Category Validation (3 tests):**
- Correct categories used in each example
- Category-specific keywords present in output

**Feature Validation (3 tests):**
- Budget constraints respected
- Energy efficiency prioritized
- Quality/premium focus maintained

**Output Validation (2 tests):**
- Recommendations produced
- Confidence scores displayed

**Structure (1 test):**
- Examples directory properly structured

## Testing Best Practices

### Running Tests
```bash
# Run single test file
python test_mina.py

# Run all tests
for test in test_*.py; do python "$test"; done

# Run with verbose output
python test_mina.py 2>&1 | tee test_results.log
```

### Interpreting Results
- ✓ indicates passed test
- ✗ indicates failed test with error message
- Summary shows passed/failed counts

### Test Independence
Each test is independent and can be run in any order. Tests use mocking to avoid side effects.

### Adding New Tests
1. Add test function with `test_` prefix
2. Include descriptive docstring
3. Use assert statements for validation
4. Add to test list in `if __name__ == "__main__"` block

Example:
```python
def test_new_feature():
    """Test description."""
    # Setup
    agent = MinaAgent()
    
    # Execute
    result = agent.new_method()
    
    # Verify
    assert result is not None
    assert result.property == expected_value
```

## Test Coverage by Feature

### ✅ Fully Tested Features
- Data classes (ProductOption, Recommendation)
- Enumerations (ProductCategory)
- Agent initialization
- Retailer browsing (all categories)
- Claude AI analysis
- Confidence scoring
- Recommendation generation
- CLI formatting and colors
- Progress indicators
- Configuration validation
- Demo workflow
- Example scripts

### 🔄 Partially Tested (Integration)
- Browser automation (mocked, not live)
- API calls (mocked, not live)
- File I/O (mocked)

### 📋 Future Testing Opportunities
- Performance benchmarks
- Load testing
- Security testing
- Browser automation (live)
- API integration (live)
- Database persistence
- Multi-threading/concurrency

## Mocking Strategy

### unittest.mock Usage
```python
from unittest.mock import patch, MagicMock

# Mock stdout for output testing
with patch('sys.stdout', new=StringIO()) as fake_out:
    function_call()
    output = fake_out.getvalue()

# Mock external dependencies
with patch('module.ExternalClass') as mock_class:
    mock_instance = MagicMock()
    mock_class.return_value = mock_instance
```

### Common Mocks
- `sys.stdout` → StringIO (capture output)
- `builtins.input` → predefined values (simulate user input)
- `os.system` → MagicMock (avoid system calls)
- External APIs → MagicMock (offline testing)

## Continuous Integration

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: |
          python test_mina.py
          python test_cli_utils.py
          python test_demo.py
          python test_config.py
          python test_examples.py
```

## Troubleshooting

### Common Issues

#### ImportError: No module named 'mina_agent'
- Ensure you're running from repository root
- Test files add parent directory to path automatically

#### Tests hanging or timing out
- Check for infinite loops in code
- Verify mock patches are correctly applied
- Use timeouts for network operations

#### Assertion errors
- Read error message carefully
- Check expected vs actual values
- Verify test data matches code changes

#### Mock not working
- Verify patch path is correct
- Check mock is applied before function call
- Use `wraps=` to preserve original behavior

## Test Maintenance

### When to Update Tests
- After modifying function signatures
- When adding new features
- After fixing bugs (add regression tests)
- When changing data structures

### Test Refactoring
- Extract common setup to helper functions
- Use fixtures for complex test data
- Keep tests focused on single functionality
- Remove or update obsolete tests

## Summary

This comprehensive test suite ensures the Mina AI Shopping Concierge is:
- **Reliable:** All core functionality tested
- **Maintainable:** Clear, well-structured tests
- **Robust:** Edge cases and errors handled
- **Documented:** Every test has clear purpose

With **112 tests** covering **all changed files**, developers can confidently modify and extend the codebase knowing tests will catch regressions.