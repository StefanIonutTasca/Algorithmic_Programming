#!/usr/bin/env python3
"""
Automotive Parts Catalog System
Main entry point for the application
"""
from .gui.main_window import MainWindow
import tkinter as tk

def main():
    """
    Main function to start the application
    """
    print("Automotive Parts Catalog System")
    print("Starting application...")
    
    # Create and start the main application window
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
