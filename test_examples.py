"""
Integration Tests for Example Scripts

Tests for the example scripts in examples/ directory to ensure
they run correctly and demonstrate the full workflow.
"""

import sys
import os
from unittest.mock import patch
from io import StringIO
import importlib.util

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_example_module(filename):
    """Helper to load an example module."""
    filepath = os.path.join("examples", filename)
    spec = importlib.util.spec_from_file_location("example_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_budget_laptop_example_exists():
    """Test that budget_laptop.py example exists."""
    example_path = os.path.join("examples", "budget_laptop.py")
    assert os.path.exists(example_path), "budget_laptop.py not found"


def test_energy_efficient_appliance_example_exists():
    """Test that energy_efficient_appliance.py example exists."""
    example_path = os.path.join("examples", "energy_efficient_appliance.py")
    assert os.path.exists(example_path), "energy_efficient_appliance.py not found"


def test_premium_furniture_example_exists():
    """Test that premium_furniture.py example exists."""
    example_path = os.path.join("examples", "premium_furniture.py")
    assert os.path.exists(example_path), "premium_furniture.py not found"


def test_budget_laptop_example_runs():
    """Test that budget_laptop example runs without errors."""
    with patch('sys.stdout', new=StringIO()):
        module = load_example_module("budget_laptop.py")
        module.budget_laptop_example()


def test_energy_efficient_appliance_example_runs():
    """Test that energy_efficient_appliance example runs without errors."""
    with patch('sys.stdout', new=StringIO()):
        module = load_example_module("energy_efficient_appliance.py")
        module.energy_efficient_appliance_example()


def test_premium_furniture_example_runs():
    """Test that premium_furniture example runs without errors."""
    with patch('sys.stdout', new=StringIO()):
        module = load_example_module("premium_furniture.py")
        module.premium_furniture_example()


def test_budget_laptop_uses_correct_category():
    """Test that budget laptop example uses laptop category."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        module = load_example_module("budget_laptop.py")
        module.budget_laptop_example()
        output = fake_out.getvalue()
        assert "laptop" in output.lower()


def test_budget_laptop_has_budget_constraint():
    """Test that budget laptop example respects budget."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        module = load_example_module("budget_laptop.py")
        module.budget_laptop_example()
        output = fake_out.getvalue()
        # Should mention budget
        assert "$" in output or "budget" in output.lower()


def test_energy_efficient_appliance_uses_correct_category():
    """Test that appliance example uses appliance category."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        module = load_example_module("energy_efficient_appliance.py")
        module.energy_efficient_appliance_example()
        output = fake_out.getvalue()
        assert "appliance" in output.lower() or "washing" in output.lower()


def test_energy_efficient_has_energy_priority():
    """Test that energy efficient example prioritizes energy efficiency."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        module = load_example_module("energy_efficient_appliance.py")
        module.energy_efficient_appliance_example()
        output = fake_out.getvalue()
        assert "energy" in output.lower() or "efficient" in output.lower()


def test_premium_furniture_uses_correct_category():
    """Test that furniture example uses furniture category."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        module = load_example_module("premium_furniture.py")
        module.premium_furniture_example()
        output = fake_out.getvalue()
        assert "furniture" in output.lower() or "chair" in output.lower()


def test_premium_furniture_has_quality_focus():
    """Test that premium furniture example focuses on quality."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        module = load_example_module("premium_furniture.py")
        module.premium_furniture_example()
        output = fake_out.getvalue()
        assert "premium" in output.lower() or "quality" in output.lower() or "ergonomic" in output.lower()


def test_examples_produce_recommendations():
    """Test that all examples produce recommendations."""
    examples = [
        ("budget_laptop.py", "budget_laptop_example"),
        ("energy_efficient_appliance.py", "energy_efficient_appliance_example"),
        ("premium_furniture.py", "premium_furniture_example"),
    ]
    
    for filename, func_name in examples:
        with patch('sys.stdout', new=StringIO()) as fake_out:
            module = load_example_module(filename)
            func = getattr(module, func_name)
            func()
            output = fake_out.getvalue()
            
            # Should contain recommendation indicators
            assert "recommendation" in output.lower() or "confidence" in output.lower(), \
                f"{filename} should produce recommendations"


def test_examples_show_confidence_scores():
    """Test that examples display confidence scores."""
    examples = [
        ("budget_laptop.py", "budget_laptop_example"),
        ("energy_efficient_appliance.py", "energy_efficient_appliance_example"),
        ("premium_furniture.py", "premium_furniture_example"),
    ]
    
    for filename, func_name in examples:
        with patch('sys.stdout', new=StringIO()) as fake_out:
            module = load_example_module(filename)
            func = getattr(module, func_name)
            func()
            output = fake_out.getvalue()
            
            # Should show confidence percentage
            assert "%" in output or "confidence" in output.lower(), \
                f"{filename} should display confidence scores"


def test_examples_directory_structure():
    """Test that examples directory has proper structure."""
    assert os.path.isdir("examples"), "examples/ directory should exist"
    
    example_files = os.listdir("examples")
    py_files = [f for f in example_files if f.endswith('.py')]
    
    assert len(py_files) >= 3, "Should have at least 3 example files"


if __name__ == "__main__":
    print("Running Example Scripts Integration Tests...\n")
    
    tests = [
        ("Budget laptop exists", test_budget_laptop_example_exists),
        ("Energy appliance exists", test_energy_efficient_appliance_example_exists),
        ("Premium furniture exists", test_premium_furniture_example_exists),
        ("Budget laptop runs", test_budget_laptop_example_runs),
        ("Energy appliance runs", test_energy_efficient_appliance_example_runs),
        ("Premium furniture runs", test_premium_furniture_example_runs),
        ("Budget laptop category", test_budget_laptop_uses_correct_category),
        ("Budget laptop constraint", test_budget_laptop_has_budget_constraint),
        ("Energy appliance category", test_energy_efficient_appliance_uses_correct_category),
        ("Energy priority", test_energy_efficient_has_energy_priority),
        ("Furniture category", test_premium_furniture_uses_correct_category),
        ("Furniture quality focus", test_premium_furniture_has_quality_focus),
        ("Examples produce recommendations", test_examples_produce_recommendations),
        ("Examples show confidence", test_examples_show_confidence_scores),
        ("Examples directory structure", test_examples_directory_structure),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}\n")
    
    sys.exit(0 if failed == 0 else 1)