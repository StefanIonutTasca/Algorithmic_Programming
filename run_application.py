#!/usr/bin/env python3
"""
Automotive Parts Catalog System Launcher
This script provides a convenient way to launch the application
"""

import os
import sys
import subprocess

def main():
    """
    Main function to start the Automotive Parts Catalog System
    """
    # Get the absolute path to the src directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    # Add the src directory to the Python path
    sys.path.insert(0, current_dir)
    
    # Run the main.py script
    from src.main import main
    main()

if __name__ == "__main__":
    main()
