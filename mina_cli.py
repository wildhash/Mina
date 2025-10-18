#!/usr/bin/env python3
"""
Mina - AI Shopping Concierge CLI

Command-line interface for the Mina AI shopping assistant.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mina_agent import MinaAgent


def main():
    """Main entry point for Mina CLI."""
    # Initialize and run the agent
    agent = MinaAgent()
    agent.run()


if __name__ == "__main__":
    main()
