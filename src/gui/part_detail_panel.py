"""
Part detail panel for the Automotive Parts Catalog System.
This module provides the user interface for displaying detailed part information.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional

from ..models.part import Part


class PartDetailPanel(ttk.Frame):
    """
    Panel for displaying detailed information about a selected part.
    
    This class creates and manages the user interface for displaying
    detailed information about a selected automotive part.
    """
    
    def __init__(self, parent):
        """
        Initialize the part detail panel.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self._current_part: Optional[Part] = None
        
        # Create a label frame for the details
        details_frame = ttk.LabelFrame(self, text="Part Details")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create labels for part information
        ttk.Label(details_frame, text="Part ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self._id_var = tk.StringVar()
        ttk.Label(details_frame, textvariable=self._id_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(details_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self._name_var = tk.StringVar()
        ttk.Label(details_frame, textvariable=self._name_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(details_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self._category_var = tk.StringVar()
        ttk.Label(details_frame, textvariable=self._category_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(details_frame, text="Price:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self._price_var = tk.StringVar()
        ttk.Label(details_frame, textvariable=self._price_var).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(details_frame, text="Manufacturer:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self._manufacturer_var = tk.StringVar()
        ttk.Label(details_frame, textvariable=self._manufacturer_var).grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Description
        ttk.Label(details_frame, text="Description:").grid(row=5, column=0, sticky=tk.NW, padx=5, pady=2)
        self._description_text = tk.Text(details_frame, height=4, width=40, wrap=tk.WORD)
        self._description_text.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self._description_text.config(state=tk.DISABLED)
        
        # Specifications frame
        ttk.Label(details_frame, text="Specifications:").grid(row=6, column=0, sticky=tk.NW, padx=5, pady=2)
        specs_frame = ttk.Frame(details_frame)
        specs_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        self._specs_text = tk.Text(specs_frame, height=4, width=40, wrap=tk.WORD)
        self._specs_text.pack(fill=tk.BOTH, expand=True)
        self._specs_text.config(state=tk.DISABLED)
        
        # Compatible vehicles frame
        ttk.Label(details_frame, text="Compatible with:").grid(row=7, column=0, sticky=tk.NW, padx=5, pady=2)
        compat_frame = ttk.Frame(details_frame)
        compat_frame.grid(row=7, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        self._compat_listbox = tk.Listbox(compat_frame, height=5)
        self._compat_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        for i in range(8):
            details_frame.grid_rowconfigure(i, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)
        
        # Clear the details initially
        self.clear()
    
    def set_part(self, part: Part) -> None:
        """
        Set the part to display details for.
        
        Args:
            part: The part to display details for
        """
        self._current_part = part
        
        # Update the display with part information
        self._id_var.set(part.get_id())
        self._name_var.set(part.get_name())
        self._category_var.set(part.get_category())
        self._price_var.set(f"${part.get_price():.2f}")
        self._manufacturer_var.set(part.get_manufacturer())
        
        # Update the description
        self._description_text.config(state=tk.NORMAL)
        self._description_text.delete(1.0, tk.END)
        self._description_text.insert(tk.END, part.get_description())
        self._description_text.config(state=tk.DISABLED)
        
        # Update the specifications
        self._specs_text.config(state=tk.NORMAL)
        self._specs_text.delete(1.0, tk.END)
        
        specs = part.get_specifications()
        for key, value in specs.items():
            self._specs_text.insert(tk.END, f"{key}: {value}\n")
        
        self._specs_text.config(state=tk.DISABLED)
        
        # Update the compatible vehicles
        self._compat_listbox.delete(0, tk.END)
        
        compat_vehicles = part.get_compatible_vehicles()
        for vehicle_key in compat_vehicles:
            make_id, model_id, year = vehicle_key.split(":")
            self._compat_listbox.insert(tk.END, f"{make_id} {model_id} ({year})")
    
    def clear(self) -> None:
        """
        Clear the part details display.
        """
        self._current_part = None
        
        # Clear all fields
        self._id_var.set("")
        self._name_var.set("")
        self._category_var.set("")
        self._price_var.set("")
        self._manufacturer_var.set("")
        
        # Clear the description
        self._description_text.config(state=tk.NORMAL)
        self._description_text.delete(1.0, tk.END)
        self._description_text.config(state=tk.DISABLED)
        
        # Clear the specifications
        self._specs_text.config(state=tk.NORMAL)
        self._specs_text.delete(1.0, tk.END)
        self._specs_text.config(state=tk.DISABLED)
        
        # Clear the compatible vehicles
        self._compat_listbox.delete(0, tk.END)
