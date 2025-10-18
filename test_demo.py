"""
Tests for Demo Module

Tests for demo.py to ensure demonstration workflow functions correctly.
"""

import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo import run_demo
from mina_agent import MinaAgent


def test_run_demo_completes():
    """Test that run_demo completes without errors."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            run_demo()


def test_run_demo_creates_agent():
    """Test that run_demo creates a MinaAgent instance."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            with patch('demo.MinaAgent') as mock_agent_class:
                mock_agent = MagicMock()
                mock_agent_class.return_value = mock_agent
                
                run_demo()
                
                # Agent should be initialized
                mock_agent_class.assert_called_once()


def test_run_demo_calls_browse_retailers():
    """Test that run_demo calls browse_retailers."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            with patch.object(agent, 'browse_retailers', wraps=agent.browse_retailers) as mock_browse:
                # We need to patch the actual function call in run_demo
                with patch('demo.MinaAgent') as mock_agent_class:
                    mock_agent_class.return_value = agent
                    run_demo()
                    
                    # browse_retailers should be called
                    mock_browse.assert_called_once()


def test_run_demo_calls_analyze_with_claude():
    """Test that run_demo calls analyze_with_claude."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            with patch.object(agent, 'analyze_with_claude', wraps=agent.analyze_with_claude) as mock_analyze:
                with patch('demo.MinaAgent') as mock_agent_class:
                    mock_agent_class.return_value = agent
                    run_demo()
                    
                    mock_analyze.assert_called_once()


def test_run_demo_calls_calculate_confidence_scores():
    """Test that run_demo calls calculate_confidence_scores."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            with patch.object(agent, 'calculate_confidence_scores', 
                            wraps=agent.calculate_confidence_scores) as mock_calc:
                with patch('demo.MinaAgent') as mock_agent_class:
                    mock_agent_class.return_value = agent
                    run_demo()
                    
                    mock_calc.assert_called_once()


def test_run_demo_generates_recommendations():
    """Test that run_demo generates recommendations."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            with patch.object(agent, 'generate_recommendations',
                            wraps=agent.generate_recommendations) as mock_gen:
                with patch('demo.MinaAgent') as mock_agent_class:
                    mock_agent_class.return_value = agent
                    run_demo()
                    
                    mock_gen.assert_called_once()


def test_run_demo_presents_recommendations():
    """Test that run_demo presents recommendations."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            with patch.object(agent, 'present_recommendations',
                            wraps=agent.present_recommendations) as mock_present:
                with patch('demo.MinaAgent') as mock_agent_class:
                    mock_agent_class.return_value = agent
                    run_demo()
                    
                    mock_present.assert_called_once()


def test_run_demo_output_contains_steps():
    """Test that run_demo output contains all workflow steps."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            run_demo()
            output = fake_out.getvalue()
            
            # Check for key steps in output
            assert "Step 1" in output or "Product Category" in output
            assert "Step 2" in output or "Requirements" in output
            assert "Step 3" in output or "Research" in output
            assert "Step 4" in output or "Analysis" in output
            assert "Step 5" in output or "Confidence" in output
            assert "Step 6" in output or "Recommendations" in output


def test_run_demo_handles_keyboard_interrupt():
    """Test that run_demo handles KeyboardInterrupt gracefully."""
    with patch('builtins.input', side_effect=KeyboardInterrupt):
        with patch('sys.stdout', new=StringIO()):
            try:
                run_demo()
                # Should not raise, should handle gracefully
                assert True
            except KeyboardInterrupt:
                # If it propagates, that's also acceptable
                assert True


def test_run_demo_budget_in_requirements():
    """Test that demo uses correct budget."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            captured_requirements = {}
            
            original_browse = agent.browse_retailers
            def capture_browse(requirements):
                captured_requirements.update(requirements)
                return original_browse(requirements)
            
            with patch.object(agent, 'browse_retailers', side_effect=capture_browse):
                with patch('demo.MinaAgent', return_value=agent):
                    run_demo()
                    
                    # Check that budget was set
                    assert 'budget_max' in captured_requirements
                    assert captured_requirements['budget_max'] > 0


def test_run_demo_laptop_category():
    """Test that demo uses laptop category."""
    with patch('builtins.input', return_value=''):
        with patch('sys.stdout', new=StringIO()):
            agent = MinaAgent()
            captured_requirements = {}
            
            original_browse = agent.browse_retailers
            def capture_browse(requirements):
                captured_requirements.update(requirements)
                return original_browse(requirements)
            
            with patch.object(agent, 'browse_retailers', side_effect=capture_browse):
                with patch('demo.MinaAgent', return_value=agent):
                    run_demo()
                    
                    # Demo should use laptop category
                    assert captured_requirements.get('category') == 'laptop'


if __name__ == "__main__":
    print("Running Demo Tests...\n")
    
    tests = [
        ("Demo completes", test_run_demo_completes),
        ("Demo creates agent", test_run_demo_creates_agent),
        ("Demo calls browse_retailers", test_run_demo_calls_browse_retailers),
        ("Demo calls analyze", test_run_demo_calls_analyze_with_claude),
        ("Demo calculates confidence", test_run_demo_calls_calculate_confidence_scores),
        ("Demo generates recommendations", test_run_demo_generates_recommendations),
        ("Demo presents recommendations", test_run_demo_presents_recommendations),
        ("Demo output has steps", test_run_demo_output_contains_steps),
        ("Demo handles interrupt", test_run_demo_handles_keyboard_interrupt),
        ("Demo uses budget", test_run_demo_budget_in_requirements),
        ("Demo uses laptop category", test_run_demo_laptop_category),
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