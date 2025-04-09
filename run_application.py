#!/usr/bin/env python3
"""
Automotive Parts Catalog System Launcher
This script provides a convenient way to launch the application
"""

import os
import sys
import tkinter as tk

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
    
    if os.path.exists(car_makes_path):
        print(f"Found car makes data at {car_makes_path}")
    else:
        print(f"Warning: Car makes data not found at {car_makes_path}")
    
    if os.path.exists(parts_path):
        print(f"Found parts data at {parts_path}")
    else:
        print(f"Warning: Parts data not found at {parts_path}")
    
    # Run the application
    print("Starting the Automotive Parts Catalog System...")
    
    # Import the required modules here to ensure paths are set up correctly
    try:
        # Create the Tkinter root window
        root = tk.Tk()
        root.title("Automotive Parts Catalog System")
        root.geometry("1000x700")
        root.minsize(800, 600)
        
        # Import the MainWindow class
        from src.gui.main_window import MainWindow
        
        # Create and run the main window
        app = MainWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
