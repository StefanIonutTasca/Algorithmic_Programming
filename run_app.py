"""
Automotive Parts Catalog System - Launcher
This script launches the main application with proper import paths.
"""
import os
import sys

# Add the current directory to the path so we can import modules correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import and run the application
from src.gui.main_window import MainWindow
import tkinter as tk

if __name__ == "__main__":
    print("Starting Automotive Parts Catalog System...")
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
