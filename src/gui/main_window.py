"""
Main window for the Automotive Parts Catalog System.
This module provides the main application window and coordinates all GUI components.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from typing import Dict, List, Any, Optional

from src.datastructures.BinarySearchTree import BinarySearchTree
from src.models.vehicle_models import CarMake, CarModel, ModelYear
from src.models.part import Part
from src.gui.search_panel import SearchPanel
from src.gui.results_panel import ResultsPanel
from src.gui.part_detail_panel import PartDetailPanel
from src.gui.performance_panel import PerformancePanel


class MainWindow:
    """
    Main application window for the Automotive Parts Catalog System.
    
    This class creates and manages the main application window and its components.
    It coordinates the interaction between different panels and handles data loading.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window.
        
        Args:
            root: The root Tkinter window
        """
        self._root = root
        self._root.title("Automotive Parts Catalog System")
        self._root.geometry("1000x700")
        self._root.minsize(800, 600)
        
        # Data containers
        self._makes_tree: Optional[BinarySearchTree[CarMake]] = None
        self._parts_by_id: Dict[str, Part] = {}
        
        # Set up the main frame
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a notebook for tabbed interface
        self._notebook = ttk.Notebook(self._main_frame)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create the search tab
        self._search_frame = ttk.Frame(self._notebook)
        self._notebook.add(self._search_frame, text="Search Parts")
        
        # Create the performance tab with a more descriptive name
        self._performance_frame = ttk.Frame(self._notebook)
        self._notebook.add(self._performance_frame, text="Algorithm & Data Structure Performance")
        
        # Initialize the panels
        self._search_panel = SearchPanel(self._search_frame, self._on_search)
        self._search_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Create a frame for results and details
        self._results_detail_frame = ttk.Frame(self._search_frame)
        self._results_detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Set up the results and detail panels with a sash divider
        self._results_detail_paned = ttk.PanedWindow(self._results_detail_frame, orient=tk.HORIZONTAL)
        self._results_detail_paned.pack(fill=tk.BOTH, expand=True)
        
        self._results_panel = ResultsPanel(self._results_detail_paned, self._on_part_selected)
        self._part_detail_panel = PartDetailPanel(self._results_detail_paned)
        
        self._results_detail_paned.add(self._results_panel, weight=1)
        self._results_detail_paned.add(self._part_detail_panel, weight=1)
        
        # Add a button frame at the bottom of the search tab for quick access to performance metrics
        self._button_frame = ttk.Frame(self._search_frame)
        self._button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            self._button_frame,
            text="View Algorithm Performance",
            command=lambda: self._notebook.select(1)  # Select the performance tab
        ).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Initialize the performance panel with our enhanced implementation
        self._performance_panel = PerformancePanel(self._performance_frame)
        self._performance_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Set up the status bar
        self._status_var = tk.StringVar()
        self._status_bar = ttk.Label(
            self._root, 
            textvariable=self._status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self._status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._status_var.set("Ready")
        
        # Load initial data
        self._load_data()
    
    def _load_data(self) -> None:
        """
        Load initial data for the application.
        
        This method loads car makes, models, years, and parts data from JSON files.
        """
        try:
            # Get the base directory for data files
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
            
            # Load makes data - fixed filename to match car_makes.json
            makes_path = os.path.join(base_dir, "car_makes.json")
            if os.path.exists(makes_path):
                with open(makes_path, 'r') as file:
                    makes_data = json.load(file)
                self._load_makes(makes_data)
                self._status_var.set(f"Loaded {len(makes_data)} car makes")
            
            # Load parts data
            parts_path = os.path.join(base_dir, "parts.json")
            if os.path.exists(parts_path):
                with open(parts_path, 'r') as file:
                    parts_data = json.load(file)
                self._load_parts(parts_data)
                self._status_var.set(f"Loaded {len(parts_data)} parts")
            
            # Update UI components with loaded data
            if self._makes_tree:
                makes = self._makes_tree.inorder_traversal()
                self._search_panel.set_makes(makes)
        
        except Exception as e:
            messagebox.showerror("Error Loading Data", str(e))
            self._status_var.set("Error loading data")
    
    def _load_makes(self, makes_data: List[Dict[str, Any]]) -> None:
        """
        Load car makes data into the binary search tree.
        
        Args:
            makes_data: List of car make dictionaries
        """
        # Create a binary search tree with a custom comparator
        self._makes_tree = BinarySearchTree(lambda a, b: -1 if a.get_name() < b.get_name() else (1 if a.get_name() > b.get_name() else 0))
        
        # Add each make to the tree
        for make_data in makes_data:
            make = CarMake.from_dict(make_data)
            self._makes_tree.insert(make)
    
    def _load_parts(self, parts_data: List[Dict[str, Any]]) -> None:
        """
        Load parts data into the application.
        
        Args:
            parts_data: List of part dictionaries
        """
        for part_data in parts_data:
            part = Part.from_dict(part_data)
            self._parts_by_id[part.get_id()] = part
    
    def _on_search(self, make_id: str, model_id: str, year: int, part_category: str) -> None:
        """
        Handle the search event from the search panel.
        
        Args:
            make_id: Selected make ID
            model_id: Selected model ID
            year: Selected year
            part_category: Selected part category
        """
        if not make_id:
            messagebox.showinfo("Selection Required", "Please select a car make")
            return
        
        # Find compatible parts
        compatible_parts = []
        for part in self._parts_by_id.values():
            if (part_category == "" or part.get_category() == part_category) and \
               (not model_id or part.is_compatible_with(make_id, model_id, year)):
                compatible_parts.append(part)
        
        # Update the results panel
        self._results_panel.set_parts(compatible_parts)
        
        # Clear the detail panel
        self._part_detail_panel.clear()
        
        # Update status
        self._status_var.set(f"Found {len(compatible_parts)} parts")
    
    def _on_part_selected(self, part: Part) -> None:
        """
        Handle the part selection event from the results panel.
        
        Args:
            part: The selected part
        """
        self._part_detail_panel.set_part(part)
        self._status_var.set(f"Selected: {part.get_name()}")
    
    def run_algorithm_demo(self, algorithm_name: str, data_size: int) -> None:
        """
        Run a demonstration of the specified algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to demonstrate
            data_size: Size of the data to use
        """
        # Forward to the performance panel
        self._performance_panel.run_algorithm_demo(algorithm_name, data_size)
        
        # Switch to the performance tab
        self._notebook.select(1)  # Select the performance tab
        
        # Update status bar with demo info
        self._status_var.set(f"Running {algorithm_name} demo with {data_size} items")
