"""
Comprehensive Tests for CLI Utilities

Tests for cli_utils.py including color handling, formatting,
and display utilities.
"""

import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_utils import (
    Colors, supports_color, colored, print_header, print_subheader,
    print_success, print_info, print_warning, print_error,
    format_price, format_rating, print_progress_bar, create_box,
    clear_screen, pause
)


def test_colors_class_attributes():
    """Test that Colors class has all required ANSI codes."""
    assert hasattr(Colors, 'HEADER')
    assert hasattr(Colors, 'OKBLUE')
    assert hasattr(Colors, 'OKCYAN')
    assert hasattr(Colors, 'OKGREEN')
    assert hasattr(Colors, 'WARNING')
    assert hasattr(Colors, 'FAIL')
    assert hasattr(Colors, 'ENDC')
    assert hasattr(Colors, 'BOLD')
    assert hasattr(Colors, 'UNDERLINE')
    
    # Verify they're strings
    assert isinstance(Colors.HEADER, str)
    assert isinstance(Colors.ENDC, str)


def test_supports_color_unix():
    """Test color support detection on Unix systems."""
    with patch('sys.platform', 'linux'):
        with patch('sys.stdout') as mock_stdout:
            mock_stdout.isatty.return_value = True
            assert supports_color()


def test_supports_color_no_tty():
    """Test color support when not a TTY."""
    with patch('sys.platform', 'linux'):
        with patch('sys.stdout') as mock_stdout:
            mock_stdout.isatty.return_value = False
            assert not supports_color()


def test_supports_color_windows_with_colorama():
    """Test color support on Windows with colorama."""
    with patch('sys.platform', 'win32'):
        with patch.dict('sys.modules', {'colorama': MagicMock()}):
            # Should return True when colorama is available
            result = supports_color()
            assert isinstance(result, bool)


def test_colored_with_color_support():
    """Test colored function when colors are supported."""
    with patch('cli_utils.supports_color', return_value=True):
        result = colored("test text", Colors.OKGREEN)
        assert Colors.OKGREEN in result
        assert Colors.ENDC in result
        assert "test text" in result


def test_colored_without_color_support():
    """Test colored function when colors are not supported."""
    with patch('cli_utils.supports_color', return_value=False):
        result = colored("test text", Colors.OKGREEN)
        assert result == "test text"
        assert Colors.OKGREEN not in result


def test_print_header():
    """Test print_header function output."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('cli_utils.supports_color', return_value=False):
            print_header("Test Header")
            output = fake_out.getvalue()
            assert "Test Header" in output
            assert "=" in output


def test_print_subheader():
    """Test print_subheader function output."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('cli_utils.supports_color', return_value=False):
            print_subheader("Test Subheader")
            output = fake_out.getvalue()
            assert "Test Subheader" in output
            assert "-" in output


def test_print_success():
    """Test print_success function."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('cli_utils.supports_color', return_value=False):
            print_success("Operation successful")
            output = fake_out.getvalue()
            assert "✓" in output
            assert "Operation successful" in output


def test_print_info():
    """Test print_info function."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('cli_utils.supports_color', return_value=False):
            print_info("Information message")
            output = fake_out.getvalue()
            assert "i" in output
            assert "Information message" in output


def test_print_warning():
    """Test print_warning function."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('cli_utils.supports_color', return_value=False):
            print_warning("Warning message")
            output = fake_out.getvalue()
            assert "⚠" in output
            assert "Warning message" in output


def test_print_error():
    """Test print_error function."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('cli_utils.supports_color', return_value=False):
            print_error("Error message")
            output = fake_out.getvalue()
            assert "✗" in output
            assert "Error message" in output


def test_format_price_standard():
    """Test price formatting with standard values."""
    assert format_price(1999.99) == "$1,999.99"
    assert format_price(100) == "$100.00"
    assert format_price(0) == "$0.00"


def test_format_price_large_values():
    """Test price formatting with large values."""
    assert format_price(1000000) == "$1,000,000.00"
    assert format_price(999999.99) == "$999,999.99"


def test_format_price_small_decimals():
    """Test price formatting with small decimal values."""
    assert format_price(0.99) == "$0.99"
    assert format_price(5.50) == "$5.50"


def test_format_rating_full_stars():
    """Test rating formatting with full stars."""
    result = format_rating(5.0)
    assert "★★★★★" in result
    assert "(5.0/5.0)" in result or "5.0" in result


def test_format_rating_partial_stars():
    """Test rating formatting with partial stars."""
    result = format_rating(4.5)
    assert "★★★★" in result
    assert "4.5" in result


def test_format_rating_low_rating():
    """Test rating formatting with low ratings."""
    result = format_rating(2.0)
    assert "★★" in result
    assert "2.0" in result


def test_format_rating_edge_cases():
    """Test rating formatting with edge case values."""
    result_zero = format_rating(0.0)
    assert "0.0" in result_zero
    
    result_max = format_rating(5.0)
    assert "5.0" in result_max


def test_format_rating_decimal_values():
    """Test rating formatting with various decimal values."""
    ratings = [3.3, 4.7, 2.8, 1.5, 4.9]
    for rating in ratings:
        result = format_rating(rating)
        assert str(rating) in result
        assert "★" in result or "☆" in result


def test_print_progress_bar_start():
    """Test progress bar at start."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        print_progress_bar(0, 100)
        output = fake_out.getvalue()
        assert "[" in output
        assert "]" in output
        assert "0.0%" in output


def test_print_progress_bar_middle():
    """Test progress bar at middle."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        print_progress_bar(50, 100)
        output = fake_out.getvalue()
        assert "50.0%" in output


def test_print_progress_bar_complete():
    """Test progress bar at completion."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        print_progress_bar(100, 100)
        output = fake_out.getvalue()
        assert "100.0%" in output


def test_print_progress_bar_custom_width():
    """Test progress bar with custom width."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        print_progress_bar(25, 100, width=20)
        output = fake_out.getvalue()
        assert "25.0%" in output


def test_create_box_simple_text():
    """Test create_box with simple text."""
    result = create_box("Hello World")
    assert "┌" in result
    assert "└" in result
    assert "│" in result
    assert "Hello World" in result


def test_create_box_multiline_text():
    """Test create_box with multiline text."""
    text = "Line 1\nLine 2\nLine 3"
    result = create_box(text)
    assert "Line 1" in result
    assert "Line 2" in result
    assert "Line 3" in result
    assert result.count("│") >= 6  # At least 2 borders per line


def test_create_box_long_text():
    """Test create_box with text longer than box width."""
    long_text = "a" * 100
    result = create_box(long_text, width=60)
    assert "..." in result  # Should truncate with ellipsis


def test_create_box_custom_width():
    """Test create_box with custom width."""
    result = create_box("Test", width=40)
    # First line should be close to 40 chars
    first_line = result.split('\n')[0]
    assert 38 <= len(first_line) <= 42


def test_create_box_empty_text():
    """Test create_box with empty text."""
    result = create_box("")
    assert "┌" in result
    assert "└" in result
    assert "│" in result


def test_clear_screen_unix():
    """Test clear_screen on Unix systems."""
    with patch('os.system') as mock_system:
        with patch('os.name', 'posix'):
            clear_screen()
            mock_system.assert_called_once_with('clear')


def test_clear_screen_windows():
    """Test clear_screen on Windows systems."""
    with patch('os.system') as mock_system:
        with patch('os.name', 'nt'):
            clear_screen()
            mock_system.assert_called_once_with('cls')


def test_pause():
    """Test pause function."""
    with patch('builtins.input', return_value=''):
        pause()  # Should not raise exception


def test_colored_multiple_color_codes():
    """Test colored with different color codes."""
    with patch('cli_utils.supports_color', return_value=True):
        colors_to_test = [
            Colors.HEADER,
            Colors.OKBLUE,
            Colors.OKCYAN,
            Colors.OKGREEN,
            Colors.WARNING,
            Colors.FAIL,
            Colors.BOLD
        ]
        
        for color in colors_to_test:
            result = colored("test", color)
            assert color in result
            assert Colors.ENDC in result


def test_format_price_negative_values():
    """Test price formatting with negative values (edge case)."""
    result = format_price(-100.50)
    assert "-$100.50" in result or "$-100.50" in result


def test_format_price_very_large():
    """Test price formatting with very large values."""
    result = format_price(9999999.99)
    assert "$9,999,999.99" in result
    assert "," in result  # Should have commas


def test_progress_bar_edge_values():
    """Test progress bar with edge case values."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        print_progress_bar(1, 1)
        output = fake_out.getvalue()
        assert "100.0%" in output


def test_box_border_characters():
    """Test that create_box uses correct Unicode box drawing characters."""
    result = create_box("Test")
    # Check for box drawing characters
    assert "┌" in result  # Top-left corner
    assert "┐" in result  # Top-right corner
    assert "└" in result  # Bottom-left corner
    assert "┘" in result  # Bottom-right corner
    assert "─" in result  # Horizontal line
    assert "│" in result  # Vertical line


if __name__ == "__main__":
    print("Running CLI Utils Tests...\n")
    
    tests = [
        ("Colors class attributes", test_colors_class_attributes),
        ("Color support - Unix", test_supports_color_unix),
        ("Color support - No TTY", test_supports_color_no_tty),
        ("Color support - Windows", test_supports_color_windows_with_colorama),
        ("Colored - with support", test_colored_with_color_support),
        ("Colored - without support", test_colored_without_color_support),
        ("Print header", test_print_header),
        ("Print subheader", test_print_subheader),
        ("Print success", test_print_success),
        ("Print info", test_print_info),
        ("Print warning", test_print_warning),
        ("Print error", test_print_error),
        ("Format price - standard", test_format_price_standard),
        ("Format price - large values", test_format_price_large_values),
        ("Format price - small decimals", test_format_price_small_decimals),
        ("Format price - negative", test_format_price_negative_values),
        ("Format price - very large", test_format_price_very_large),
        ("Format rating - full stars", test_format_rating_full_stars),
        ("Format rating - partial stars", test_format_rating_partial_stars),
        ("Format rating - low rating", test_format_rating_low_rating),
        ("Format rating - edge cases", test_format_rating_edge_cases),
        ("Format rating - decimals", test_format_rating_decimal_values),
        ("Progress bar - start", test_print_progress_bar_start),
        ("Progress bar - middle", test_print_progress_bar_middle),
        ("Progress bar - complete", test_print_progress_bar_complete),
        ("Progress bar - custom width", test_print_progress_bar_custom_width),
        ("Progress bar - edge values", test_progress_bar_edge_values),
        ("Create box - simple", test_create_box_simple_text),
        ("Create box - multiline", test_create_box_multiline_text),
        ("Create box - long text", test_create_box_long_text),
        ("Create box - custom width", test_create_box_custom_width),
        ("Create box - empty text", test_create_box_empty_text),
        ("Create box - borders", test_box_border_characters),
        ("Clear screen - Unix", test_clear_screen_unix),
        ("Clear screen - Windows", test_clear_screen_windows),
        ("Pause", test_pause),
        ("Colored - multiple codes", test_colored_multiple_color_codes),
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