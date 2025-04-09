#!/usr/bin/env python3
"""
Automotive Parts Catalog System Launcher
This script provides a convenient way to launch the application with proper error handling
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

# Enhanced error handling
def show_error(exc_type, exc_value, exc_traceback):
    """
    Global exception handler to capture and display uncaught exceptions
    """
    print("*** Uncaught Exception ***")
    print("Type:", exc_type)
    print("Value:", exc_value)
    traceback.print_tb(exc_traceback)
    # Re-raise to standard handler
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

# Set up the global exception handler
sys.excepthook = show_error

def report_callback_exception(exc, val, tb):
    """
    Handler for Tkinter widget callback exceptions
    """
    print("\n*** Tkinter Callback Exception ***")
    print("Type:", exc)
    print("Value:", val)
    traceback.print_tb(tb)
    messagebox.showerror("Application Error", f"An unexpected error occurred:\n{val}")

def main():
    """
    Main function to start the Automotive Parts Catalog System
    """
    # Get the absolute path to the src directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    # Add the project directory to the Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Ensure data directory exists
    data_dir = os.path.join(current_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at {data_dir}")
    
    # Check if data files exist and provide status
    car_makes_path = os.path.join(data_dir, 'car_makes.json')
    parts_path = os.path.join(data_dir, 'parts.json')
    
    missing_files = []
    if not os.path.exists(car_makes_path):
        missing_files.append("car_makes.json")
    if not os.path.exists(parts_path):
        missing_files.append("parts.json")
    
    # Initialize the Tkinter application
    try:
        print("Starting Automotive Parts Catalog System...")
        root = tk.Tk()
        root.title("Automotive Parts Catalog System")
        root.geometry("1000x700")
        root.minsize(800, 600)
        
        # Set up Tkinter exception handling
        root.report_callback_exception = report_callback_exception
        
        # If data files are missing, show a warning but continue
        if missing_files:
            missing_list = ", ".join(missing_files)
            warning_message = f"Warning: The following data files are missing:\n{missing_list}\n\nThe application may not function correctly."
            print(warning_message)
            messagebox.showwarning("Missing Data Files", warning_message)
        
        try:
            # Import here to ensure path is set up correctly
            from src.gui.main_window import MainWindow
            
            # Create and run the main application
            app = MainWindow(root)
            root.mainloop()
        except Exception as e:
            error_message = f"Error initializing application: {str(e)}"
            print(error_message)
            traceback.print_exc()
            messagebox.showerror("Initialization Error", error_message)
            
    except Exception as e:
        print(f"Critical Error: {str(e)}")
        traceback.print_exc()
        # Try to show a message box if possible
        try:
            messagebox.showerror("Critical Error", f"A critical error occurred:\n{str(e)}")
        except:
            print("Could not display error dialog. Application will exit.")
        sys.exit(1)

if __name__ == "__main__":
    main()
