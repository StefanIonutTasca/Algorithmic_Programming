"""
Results panel for the Automotive Parts Catalog System.
This module provides the user interface for displaying search results.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional

from ..models.part import Part


class ResultsPanel(ttk.Frame):
    """
    Panel for displaying search results in the parts catalog system.
    
    This class creates and manages the user interface for displaying
    parts that match the search criteria.
    """
    
    def __init__(self, parent, select_callback: Callable[[Part], None]):
        """
        Initialize the results panel.
        
        Args:
            parent: The parent widget
            select_callback: Callback function for when a part is selected
        """
        super().__init__(parent)
        self._select_callback = select_callback
        self._parts: List[Part] = []
        
        # Create a label frame for the results
        results_frame = ttk.LabelFrame(self, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for displaying the parts
        columns = ("name", "category", "price")
        self._tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Define the column headings
        self._tree.heading("name", text="Part Name")
        self._tree.heading("category", text="Category")
        self._tree.heading("price", text="Price")
        
        # Define the column widths
        self._tree.column("name", width=200)
        self._tree.column("category", width=100)
        self._tree.column("price", width=80)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        
        # Place the treeview and scrollbar
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind the selection event
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)
    
    def set_parts(self, parts: List[Part]) -> None:
        """
        Set the parts to display in the results panel.
        
        Args:
            parts: List of parts to display
        """
        self._parts = parts
        
        # Clear the existing items
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        # Add the new parts
        for i, part in enumerate(parts):
            values = (
                part.get_name(),
                part.get_category(),
                f"${part.get_price():.2f}"
            )
            self._tree.insert("", tk.END, values=values, iid=str(i))
    
    def _on_tree_select(self, event) -> None:
        """
        Handle the tree item selection event.
        
        Args:
            event: The selection event
        """
        selection = self._tree.selection()
        if not selection:
            return
            
        # Get the selected part
        try:
            index = int(selection[0])
            if 0 <= index < len(self._parts):
                part = self._parts[index]
                self._select_callback(part)
        except ValueError:
            pass
