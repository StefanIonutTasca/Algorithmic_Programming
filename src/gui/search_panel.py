"""
Search panel for the Automotive Parts Catalog System.
This module provides the user interface for searching parts by vehicle.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional

from ..models.vehicle_models import CarMake, CarModel, ModelYear


class SearchPanel(ttk.Frame):
    """
    Panel for searching automotive parts by vehicle and category.
    
    This class creates and manages the user interface for selecting a vehicle
    (make, model, year) and part category to search for compatible parts.
    """
    
    def __init__(self, parent, search_callback: Callable[[str, str, int, str], None]):
        """
        Initialize the search panel.
        
        Args:
            parent: The parent widget
            search_callback: Callback function for the search action
        """
        super().__init__(parent)
        self._search_callback = search_callback
        self._makes: List[CarMake] = []
        
        # Current selections
        self._selected_make: Optional[CarMake] = None
        self._selected_model: Optional[CarModel] = None
        self._selected_year: Optional[ModelYear] = None
        
        # Create a frame for the search criteria
        criteria_frame = ttk.LabelFrame(self, text="Search Criteria")
        criteria_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the make selection dropdown
        ttk.Label(criteria_frame, text="Car Make:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self._make_var = tk.StringVar()
        self._make_combobox = ttk.Combobox(criteria_frame, textvariable=self._make_var, state="readonly")
        self._make_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self._make_combobox.bind("<<ComboboxSelected>>", self._on_make_selected)
        
        # Create the model selection dropdown
        ttk.Label(criteria_frame, text="Car Model:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self._model_var = tk.StringVar()
        self._model_combobox = ttk.Combobox(criteria_frame, textvariable=self._model_var, state="readonly")
        self._model_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self._model_combobox.bind("<<ComboboxSelected>>", self._on_model_selected)
        
        # Create the year selection dropdown
        ttk.Label(criteria_frame, text="Model Year:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self._year_var = tk.StringVar()
        self._year_combobox = ttk.Combobox(criteria_frame, textvariable=self._year_var, state="readonly")
        self._year_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self._year_combobox.bind("<<ComboboxSelected>>", self._on_year_selected)
        
        # Create the part category selection dropdown
        ttk.Label(criteria_frame, text="Part Category:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self._category_var = tk.StringVar()
        self._category_combobox = ttk.Combobox(criteria_frame, textvariable=self._category_var, state="readonly")
        self._category_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Set default categories
        self._category_combobox["values"] = ["", "Engine", "Transmission", "Brakes", "Suspension", 
                                           "Electrical", "Body", "Interior", "Accessories"]
        
        # Create the search button
        search_button = ttk.Button(criteria_frame, text="Search", command=self._on_search)
        search_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        for i in range(5):
            criteria_frame.grid_rowconfigure(i, weight=1)
        criteria_frame.grid_columnconfigure(1, weight=1)
    
    def set_makes(self, makes: List[CarMake]) -> None:
        """
        Set the available car makes for selection.
        
        Args:
            makes: List of car makes
        """
        # Filter out any non-CarMake objects or lists
        valid_makes = []
        for make in makes:
            if hasattr(make, 'get_name'):
                valid_makes.append(make)
            elif isinstance(make, list) and len(make) > 0 and hasattr(make[0], 'get_name'):
                # If we received a list of makes, add its items individually
                valid_makes.extend([m for m in make if hasattr(m, 'get_name')])
            else:
                print(f"Warning: Invalid make object encountered: {type(make)}")
        
        self._makes = valid_makes
        
        # Only process valid makes that have a get_name method
        make_names = []
        for make in valid_makes:
            try:
                make_names.append(make.get_name())
            except Exception as e:
                print(f"Error getting make name: {e}")
        
        self._make_combobox["values"] = make_names
        
        # Clear other selections
        self._model_combobox.set("")
        self._model_combobox["values"] = []
        self._year_combobox.set("")
        self._year_combobox["values"] = []
        
        self._selected_make = None
        self._selected_model = None
        self._selected_year = None
    
    def _on_make_selected(self, event) -> None:
        """
        Handle the selection of a car make.
        
        Args:
            event: The combobox selection event
        """
        make_name = self._make_var.get()
        
        # Find the selected make
        self._selected_make = None
        for make in self._makes:
            if make.get_name() == make_name:
                self._selected_make = make
                break
        
        if self._selected_make:
            # Update the model dropdown
            models = self._selected_make.get_models()
            model_names = [model.get_name() for model in models]
            self._model_combobox["values"] = model_names
            
            # Clear the model and year selections
            self._model_combobox.set("")
            self._year_combobox.set("")
            self._year_combobox["values"] = []
            
            self._selected_model = None
            self._selected_year = None
    
    def _on_model_selected(self, event) -> None:
        """
        Handle the selection of a car model.
        
        Args:
            event: The combobox selection event
        """
        if not self._selected_make:
            return
            
        model_name = self._model_var.get()
        
        # Find the selected model
        self._selected_model = None
        for model in self._selected_make.get_models():
            if model.get_name() == model_name:
                self._selected_model = model
                break
        
        if self._selected_model:
            # Update the year dropdown
            years = self._selected_model.get_years()
            year_values = [str(year.get_year()) for year in years]
            self._year_combobox["values"] = year_values
            
            # Clear the year selection
            self._year_combobox.set("")
            self._selected_year = None
    
    def _on_year_selected(self, event) -> None:
        """
        Handle the selection of a model year.
        
        Args:
            event: The combobox selection event
        """
        if not self._selected_model:
            return
            
        try:
            year_value = int(self._year_var.get())
            
            # Find the selected year
            self._selected_year = None
            for year in self._selected_model.get_years():
                if year.get_year() == year_value:
                    self._selected_year = year
                    break
        except ValueError:
            # Invalid year value
            self._selected_year = None
    
    def _on_search(self) -> None:
        """
        Handle the search button click.
        """
        make_id = self._selected_make.get_id() if self._selected_make else ""
        model_id = self._selected_model.get_id() if self._selected_model else ""
        year = self._selected_year.get_year() if self._selected_year else 0
        category = self._category_var.get()
        
        # Call the search callback with the selected criteria
        self._search_callback(make_id, model_id, year, category)
