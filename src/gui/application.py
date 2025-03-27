"""
Main GUI application for the Automotive Parts Catalog System.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import threading
import os
import sys
import random
from typing import List, Dict, Any, Callable, Optional, Tuple

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.datastructures.array_list import ArrayList
from src.datastructures.linked_list import LinkedList
from src.datastructures.binary_search_tree import BinarySearchTree
from src.algorithms.search import linear_search, binary_search
from src.algorithms.sort import quick_sort, merge_sort
from src.models.part import Part, PartCategory, PartCatalog
from src.models.vehicle import VehicleMake, VehicleModel, VehicleYear, VehicleRegistry
from src.gui.catalog_panel import CatalogPanel
from src.gui.search_panel import SearchPanel
from src.gui.algorithm_panel import AlgorithmPanel
from src.gui.data_panel import DataPanel


class Application(tk.Tk):
    """
    Main application class for the Automotive Parts Catalog System.
    """
    
    def __init__(self):
        """
        Initialize the application.
        """
        super().__init__()
        
        self.title("Automotive Parts Catalog System")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Set up the style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the 'clam' theme for a more modern look
        
        # Configure colors
        bg_color = "#f0f0f0"
        frame_bg = "#ffffff"
        header_bg = "#333333"
        header_fg = "#ffffff"
        
        self.style.configure("TFrame", background=frame_bg)
        self.style.configure("Header.TFrame", background=header_bg)
        self.style.configure("Header.TLabel", background=header_bg, foreground=header_fg, font=("Arial", 14, "bold"))
        self.style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        self.style.configure("Subtitle.TLabel", font=("Arial", 12))
        self.style.configure("Section.TLabel", font=("Arial", 12, "bold"))
        
        # Configure the root window
        self.configure(background=bg_color)
        
        # Initialize data structures
        self.catalog = PartCatalog()
        self.registry = VehicleRegistry()
        
        # List representations of our data for algorithm testing
        self.array_list_data = ArrayList[Part]()
        self.linked_list_data = LinkedList[Part]()
        self.binary_search_tree_data = BinarySearchTree[Part]()
        
        # Current data sample size (percentage of full dataset)
        self.data_sample_size = 100  # Default to 100%
        
        # Create the main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header
        self.create_header()
        
        # Create the notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the catalog panel
        self.catalog_panel = CatalogPanel(self.notebook, self)
        self.notebook.add(self.catalog_panel, text="Catalog")
        
        # Create the search panel
        self.search_panel = SearchPanel(self.notebook, self)
        self.notebook.add(self.search_panel, text="Search")
        
        # Create the algorithm panel
        self.algorithm_panel = AlgorithmPanel(self.notebook, self)
        self.notebook.add(self.algorithm_panel, text="Algorithms")
        
        # Create the data panel
        self.data_panel = DataPanel(self.notebook, self)
        self.notebook.add(self.data_panel, text="Data")
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind events
        self.bind("<Configure>", self.on_resize)
        
        # Load sample data
        self.load_sample_data()
    
    def create_header(self):
        """
        Create the application header.
        """
        header_frame = ttk.Frame(self.main_container, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        header_label = ttk.Label(
            header_frame, 
            text="Automotive Parts Catalog System", 
            style="Header.TLabel",
            padding=(10, 5)
        )
        header_label.pack(side=tk.LEFT)
    
    def on_resize(self, event):
        """
        Handle window resize events.
        """
        # Only process events from the main window
        if event.widget == self:
            # Do any resizing adjustments if needed
            pass
    
    def load_sample_data(self):
        """
        Load sample data into the application.
        """
        self.status_var.set("Loading sample data...")
        
        # Start in a separate thread to avoid blocking the UI
        threading.Thread(target=self._load_sample_data_thread, daemon=True).start()
    
    def _load_sample_data_thread(self):
        """
        Thread function to load sample data.
        """
        try:
            # Create categories
            categories = [
                PartCategory(1, "Filters", "Air, oil, and fuel filters"),
                PartCategory(2, "Brakes", "Brake pads, rotors, and calipers"),
                PartCategory(3, "Engine", "Engine components and parts"),
                PartCategory(4, "Suspension", "Suspension and steering components"),
                PartCategory(5, "Electrical", "Electrical components and wiring"),
                PartCategory(6, "Transmission", "Transmission components and fluids"),
                PartCategory(7, "Cooling", "Cooling system components"),
                PartCategory(8, "Body", "Body panels and parts")
            ]
            
            for category in categories:
                self.catalog.add_category(category)
            
            # Create makes
            makes = [
                VehicleMake(1, "Honda"),
                VehicleMake(2, "Toyota"),
                VehicleMake(3, "Ford"),
                VehicleMake(4, "Chevrolet"),
                VehicleMake(5, "BMW"),
                VehicleMake(6, "Mercedes-Benz"),
                VehicleMake(7, "Audi"),
                VehicleMake(8, "Volkswagen")
            ]
            
            for make in makes:
                self.registry.add_make(make)
            
            # Create models
            models_data = [
                # Honda models
                (1, 101, "Civic"),
                (1, 102, "Accord"),
                (1, 103, "CR-V"),
                # Toyota models
                (2, 201, "Camry"),
                (2, 202, "Corolla"),
                (2, 203, "RAV4"),
                # Ford models
                (3, 301, "F-150"),
                (3, 302, "Mustang"),
                (3, 303, "Explorer"),
                # Chevrolet models
                (4, 401, "Silverado"),
                (4, 402, "Camaro"),
                (4, 403, "Equinox"),
                # BMW models
                (5, 501, "3 Series"),
                (5, 502, "5 Series"),
                (5, 503, "X5"),
                # Mercedes-Benz models
                (6, 601, "C-Class"),
                (6, 602, "E-Class"),
                (6, 603, "GLE"),
                # Audi models
                (7, 701, "A4"),
                (7, 702, "A6"),
                (7, 703, "Q5"),
                # Volkswagen models
                (8, 801, "Golf"),
                (8, 802, "Passat"),
                (8, 803, "Tiguan")
            ]
            
            for make_id, model_id, model_name in models_data:
                make = self.registry.get_make(make_id)
                if make:
                    model = VehicleModel(model_id, model_name)
                    make.add_model(model)
                    
                    # Add years for each model (2015-2023)
                    for year in range(2015, 2024):
                        model.add_year(VehicleYear(year))
            
            # Create parts (100 sample parts)
            parts_data = []
            part_names = [
                # Filters
                "Oil Filter", "Air Filter", "Fuel Filter", "Cabin Air Filter", "Transmission Filter",
                # Brakes
                "Front Brake Pads", "Rear Brake Pads", "Front Brake Rotors", "Rear Brake Rotors",
                "Brake Calipers", "Brake Fluid", "Brake Lines", "Brake Master Cylinder",
                # Engine
                "Spark Plugs", "Ignition Coils", "Timing Belt", "Timing Chain", "Alternator",
                "Starter Motor", "Engine Oil", "Oil Pan", "Head Gasket", "Valve Cover", "Turbocharger",
                # Suspension
                "Struts", "Shocks", "Control Arms", "Tie Rods", "Ball Joints", "Wheel Bearings",
                "Sway Bar Links", "Coil Springs", "Leaf Springs", "Strut Mounts",
                # Electrical
                "Battery", "Alternator", "Starter", "Headlights", "Tail Lights", "Turn Signals",
                "Ignition Switch", "Sensors", "Fuses", "Relays", "Wiring Harness",
                # Transmission
                "Transmission Fluid", "Clutch Kit", "Flywheel", "Torque Converter", "Transmission Mount",
                "Shift Cable", "Transmission Solenoid", "Transmission Control Module",
                # Cooling
                "Radiator", "Thermostat", "Water Pump", "Coolant", "Radiator Hoses", "Radiator Cap",
                "Cooling Fan", "Fan Clutch",
                # Body
                "Hood", "Fenders", "Doors", "Trunk Lid", "Bumper Cover", "Grille", "Side Mirrors",
                "Wiper Blades", "Windshield", "Weather Stripping"
            ]
            
            # Generate 100 parts with different combinations of names and categories
            part_id = 1001
            for category_name in ["Filters", "Brakes", "Engine", "Suspension", "Electrical", 
                                 "Transmission", "Cooling", "Body"]:
                related_parts = [p for p in part_names if any(
                    keyword in p.lower() for keyword in category_name.lower().split())]
                
                # If no direct match, use all parts
                if not related_parts:
                    related_parts = part_names
                
                # Add at least 10 parts per category
                for i in range(12):
                    name = random.choice(related_parts)
                    price = round(random.uniform(5.99, 299.99), 2)
                    description = f"High quality {name.lower()} for optimal performance."
                    
                    part = Part(part_id, name, category_name, price, description)
                    self.catalog.add_part(part)
                    
                    # Randomly assign compatibility with vehicles
                    for make in makes:
                        # Each part is compatible with 30% of makes
                        if random.random() < 0.3:
                            for model in make.get_models():
                                # Compatible with 40% of models for each compatible make
                                if random.random() < 0.4:
                                    for year_obj in model.get_years():
                                        # Compatible with 60% of years for each compatible model
                                        if random.random() < 0.6:
                                            part.add_compatible_vehicle(
                                                make.name, 
                                                model.name, 
                                                year_obj.year
                                            )
                    
                    parts_data.append(part)
                    part_id += 1
            
            # Load data into our data structures
            for part in parts_data:
                self.array_list_data.append(part)
                self.linked_list_data.append(part)
                self.binary_search_tree_data.insert(part)
            
            # Update status
            self.status_var.set(f"Loaded {len(parts_data)} parts across {len(categories)} categories")
            
            # Notify panels that data is loaded
            self.catalog_panel.on_data_loaded()
            self.search_panel.on_data_loaded()
            self.algorithm_panel.on_data_loaded()
            self.data_panel.on_data_loaded()
            
        except Exception as e:
            self.status_var.set(f"Error loading sample data: {str(e)}")
            messagebox.showerror("Data Loading Error", f"Failed to load sample data: {str(e)}")
    
    def get_sample_data(self, percentage: int = 100) -> List[Part]:
        """
        Get a sample of the data based on the specified percentage.
        
        Args:
            percentage: Percentage of the full dataset to return (1-100)
            
        Returns:
            A list of Part objects representing the sample
        """
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be between 1 and 100")
        
        full_data = list(self.catalog.get_parts())
        if percentage == 100:
            return full_data
        
        sample_size = max(1, int(len(full_data) * percentage / 100))
        return random.sample(full_data, sample_size)
    
    def set_status(self, message: str):
        """
        Set the status bar message.
        
        Args:
            message: The message to display
        """
        self.status_var.set(message)
    
    def run(self):
        """
        Run the application main loop.
        """
        self.mainloop()
