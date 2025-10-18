"""
Tests for Configuration File

Validates config.ini schema, required keys, and value ranges.
"""

import sys
import os
import configparser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_config_file_exists():
    """Test that config.ini file exists."""
    assert os.path.exists("config.ini"), "config.ini file not found"


def test_config_can_be_parsed():
    """Test that config.ini can be parsed."""
    config = configparser.ConfigParser()
    files_read = config.read("config.ini")
    assert len(files_read) > 0, "Could not read config.ini"


def test_config_has_required_sections():
    """Test that config.ini has all required sections."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    required_sections = ['agent', 'retailers', 'confidence_scoring', 'analysis', 'output']
    
    for section in required_sections:
        assert section in config.sections(), f"Missing required section: {section}"


def test_agent_section_keys():
    """Test agent section has required keys."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    required_keys = ['min_price', 'max_products', 'verbose']
    
    for key in required_keys:
        assert config.has_option('agent', key), f"Missing key in [agent]: {key}"


def test_agent_min_price_valid():
    """Test that min_price is a valid positive number."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    min_price = config.getint('agent', 'min_price')
    assert min_price >= 0, "min_price should be non-negative"
    assert min_price == 500, "min_price should be 500 for high-end purchases"


def test_agent_max_products_valid():
    """Test that max_products is a valid positive number."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    max_products = config.getint('agent', 'max_products')
    assert max_products > 0, "max_products should be positive"
    assert max_products <= 100, "max_products should be reasonable (<=100)"


def test_agent_verbose_is_boolean():
    """Test that verbose is a boolean value."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    verbose = config.get('agent', 'verbose').lower()
    assert verbose in ['true', 'false', 'yes', 'no', '1', '0'], \
        "verbose should be a boolean value"


def test_retailers_section_keys():
    """Test retailers section has required keys."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    assert config.has_option('retailers', 'enabled_retailers'), \
        "Missing enabled_retailers in [retailers]"


def test_retailers_list_not_empty():
    """Test that enabled_retailers list is not empty."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    retailers = config.get('retailers', 'enabled_retailers')
    assert len(retailers.strip()) > 0, "enabled_retailers should not be empty"
    
    retailers_list = [r.strip() for r in retailers.split(',')]
    assert len(retailers_list) > 0, "Should have at least one retailer"


def test_confidence_scoring_weights():
    """Test that confidence scoring weights are valid."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    required_weights = ['rating_weight', 'fit_score_weight', 
                       'review_confidence_weight', 'data_completeness_weight']
    
    total_weight = 0.0
    for weight_key in required_weights:
        assert config.has_option('confidence_scoring', weight_key), \
            f"Missing weight: {weight_key}"
        
        weight = config.getfloat('confidence_scoring', weight_key)
        assert 0.0 <= weight <= 1.0, f"{weight_key} should be between 0 and 1"
        total_weight += weight
    
    # Weights should sum to 1.0 (allow small floating point error)
    assert abs(total_weight - 1.0) < 0.01, \
        f"Confidence weights should sum to 1.0, got {total_weight}"


def test_confidence_min_threshold():
    """Test that min_confidence_threshold is valid."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    min_threshold = config.getfloat('confidence_scoring', 'min_confidence_threshold')
    assert 0.0 <= min_threshold <= 100.0, \
        "min_confidence_threshold should be between 0 and 100"


def test_analysis_section_keys():
    """Test analysis section has required keys."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    required_keys = ['num_recommendations', 'include_price_history', 
                    'include_sustainability']
    
    for key in required_keys:
        assert config.has_option('analysis', key), \
            f"Missing key in [analysis]: {key}"


def test_analysis_num_recommendations():
    """Test that num_recommendations is valid."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    num_recs = config.getint('analysis', 'num_recommendations')
    assert num_recs > 0, "num_recommendations should be positive"
    assert num_recs <= 20, "num_recommendations should be reasonable (<=20)"


def test_analysis_boolean_flags():
    """Test that analysis boolean flags are valid."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    bool_keys = ['include_price_history', 'include_sustainability']
    
    for key in bool_keys:
        value = config.get('analysis', key).lower()
        assert value in ['true', 'false', 'yes', 'no', '1', '0'], \
            f"{key} should be a boolean value"


def test_output_section_keys():
    """Test output section has required keys."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    required_keys = ['format', 'use_colors', 'save_to_file', 'output_directory']
    
    for key in required_keys:
        assert config.has_option('output', key), \
            f"Missing key in [output]: {key}"


def test_output_format_valid():
    """Test that output format is valid."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    format_val = config.get('output', 'format').lower()
    valid_formats = ['cli', 'json', 'html']
    assert format_val in valid_formats, \
        f"format should be one of {valid_formats}, got {format_val}"


def test_output_use_colors_boolean():
    """Test that use_colors is a boolean."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    use_colors = config.get('output', 'use_colors').lower()
    assert use_colors in ['true', 'false', 'yes', 'no', '1', '0'], \
        "use_colors should be a boolean value"


def test_output_save_to_file_boolean():
    """Test that save_to_file is a boolean."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    save = config.get('output', 'save_to_file').lower()
    assert save in ['true', 'false', 'yes', 'no', '1', '0'], \
        "save_to_file should be a boolean value"


def test_output_directory_specified():
    """Test that output_directory is specified."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    output_dir = config.get('output', 'output_directory')
    assert len(output_dir.strip()) > 0, "output_directory should not be empty"


def test_config_no_duplicate_sections():
    """Test that config has no duplicate sections."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    sections = config.sections()
    assert len(sections) == len(set(sections)), \
        "Config should not have duplicate sections"


def test_retailers_known_brands():
    """Test that retailers list contains known brands."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    retailers = config.get('retailers', 'enabled_retailers')
    retailers_list = [r.strip() for r in retailers.split(',')]
    
    # Check for some expected retailers
    expected_retailers = ['Amazon', 'Best Buy']
    for expected in expected_retailers:
        assert any(expected in r for r in retailers_list), \
            f"Should include {expected} in retailers list"


if __name__ == "__main__":
    print("Running Config Validation Tests...\n")
    
    tests = [
        ("Config file exists", test_config_file_exists),
        ("Config can be parsed", test_config_can_be_parsed),
        ("Required sections present", test_config_has_required_sections),
        ("Agent section keys", test_agent_section_keys),
        ("Agent min_price valid", test_agent_min_price_valid),
        ("Agent max_products valid", test_agent_max_products_valid),
        ("Agent verbose boolean", test_agent_verbose_is_boolean),
        ("Retailers section keys", test_retailers_section_keys),
        ("Retailers list not empty", test_retailers_list_not_empty),
        ("Confidence scoring weights", test_confidence_scoring_weights),
        ("Confidence min threshold", test_confidence_min_threshold),
        ("Analysis section keys", test_analysis_section_keys),
        ("Analysis num recommendations", test_analysis_num_recommendations),
        ("Analysis boolean flags", test_analysis_boolean_flags),
        ("Output section keys", test_output_section_keys),
        ("Output format valid", test_output_format_valid),
        ("Output use_colors boolean", test_output_use_colors_boolean),
        ("Output save_to_file boolean", test_output_save_to_file_boolean),
        ("Output directory specified", test_output_directory_specified),
        ("No duplicate sections", test_config_no_duplicate_sections),
        ("Retailers known brands", test_retailers_known_brands),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except (AssertionError, OSError, ValueError) as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}\n")
    
    sys.exit(0 if failed == 0 else 1)