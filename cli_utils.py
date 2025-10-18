"""
CLI Utilities for Mina

Provides formatting and display utilities for the command-line interface.
"""

import sys


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def supports_color():
    """
    Check if the terminal supports color output.
    
    Returns:
        bool: True if colors are supported
    """
    # Check if we're on Windows and if so, enable ANSI support
    if sys.platform == "win32":
        try:
            import colorama
            colorama.init()
            return True
        except ImportError:
            return False
    
    # Unix-like systems typically support colors
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


def colored(text, color_code):
    """
    Colorize text if terminal supports it.
    
    Args:
        text: Text to colorize
        color_code: ANSI color code
        
    Returns:
        Colorized text or plain text
    """
    if supports_color():
        return f"{color_code}{text}{Colors.ENDC}"
    return text


def print_header(text):
    """Print a formatted header."""
    print("\n" + colored("=" * 60, Colors.BOLD))
    print(colored(text, Colors.HEADER + Colors.BOLD))
    print(colored("=" * 60, Colors.BOLD))


def print_subheader(text):
    """Print a formatted subheader."""
    print("\n" + colored(text, Colors.OKBLUE + Colors.BOLD))
    print(colored("-" * 60, Colors.OKBLUE))


def print_success(text):
    """Print success message."""
    print(colored(f"✓ {text}", Colors.OKGREEN))


def print_info(text):
    """Print info message."""
    print(colored(f"ℹ {text}", Colors.OKCYAN))


def print_warning(text):
    """Print warning message."""
    print(colored(f"⚠ {text}", Colors.WARNING))


def print_error(text):
    """Print error message."""
    print(colored(f"✗ {text}", Colors.FAIL))


def format_price(price):
    """
    Format price with proper currency symbol.
    
    Args:
        price: Price value
        
    Returns:
        Formatted price string
    """
    return f"${price:,.2f}"


def format_rating(rating):
    """
    Format rating with stars.
    
    Args:
        rating: Rating value (0-5)
        
    Returns:
        Formatted rating string
    """
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "★" * full_stars
    if half_star:
        stars += "⭐"
    stars += "☆" * empty_stars
    
    return f"{stars} ({rating}/5.0)"


def print_progress_bar(current, total, width=40):
    """
    Print a progress bar.
    
    Args:
        current: Current progress value
        total: Total value
        width: Width of progress bar
    """
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = progress * 100
    
    print(f"\r[{bar}] {percentage:.1f}%", end="", flush=True)
    
    if current == total:
        print()  # New line when complete


def create_box(text, width=60):
    """
    Create a text box with borders.
    
    Args:
        text: Text to display in box
        width: Width of box
        
    Returns:
        Formatted box string
    """
    lines = text.split('\n')
    output = []
    
    output.append("┌" + "─" * (width - 2) + "┐")
    
    for line in lines:
        # Pad or truncate line to fit
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        padding = width - 4 - len(line)
        output.append(f"│ {line}{' ' * padding} │")
    
    output.append("└" + "─" * (width - 2) + "┘")
    
    return '\n'.join(output)


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause and wait for user input."""
    input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Demo the utilities
    print_header("Mina CLI Utilities Demo")
    
    print_success("This is a success message")
    print_info("This is an info message")
    print_warning("This is a warning message")
    print_error("This is an error message")
    
    print_subheader("Formatting Examples")
    print(f"Price: {format_price(1999.99)}")
    print(f"Rating: {format_rating(4.7)}")
    
    print_subheader("Progress Bar")
    for i in range(1, 11):
        print_progress_bar(i, 10)
        import time
        time.sleep(0.1)
    
    print_subheader("Text Box")
    box_text = "Mina - AI Shopping Concierge\nMaking high-end purchases with confidence"
    print(create_box(box_text))
