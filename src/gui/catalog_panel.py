"""
Catalog panel for the Automotive Parts Catalog System.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional
import threading

from src.models.part import Part


class CatalogPanel(ttk.Frame):
    """
    Panel for displaying and browsing the parts catalog.
    """
    
    def __init__(self, parent, app):
        """
        Initialize the catalog panel.
        
        Args:
            parent: The parent widget
            app: The main application instance
        """
        super().__init__(parent)
        self.app = app
        
        # Create the UI components
        self.create_widgets()
        
        # Current category filter
        self.current_category = None
    
    def create_widgets(self):
        """
        Create the UI widgets for the catalog panel.
        """
        # Main vertical split
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel (categories)
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame)
        
        # Right panel (parts list)
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame)
        
        # Categories section
        self.create_categories_section()
        
        # Parts list section
        self.create_parts_list_section()
        
        # Part details section
        self.create_part_details_section()
    
    def create_categories_section(self):
        """
        Create the categories section in the left panel.
        """
        # Categories header
        ttk.Label(self.left_frame, text="Categories", style="Section.TLabel").pack(
            fill=tk.X, padx=5, pady=5
        )
        
        # Categories listbox with scrollbar
        list_frame = ttk.Frame(self.left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.categories_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            exportselection=0
        )
        self.categories_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.categories_listbox.yview)
        
        # Add "All Categories" option
        self.categories_listbox.insert(tk.END, "All Categories")
        
        # Bind event
        self.categories_listbox.bind("<<ListboxSelect>>", self.on_category_select)
    
    def create_parts_list_section(self):
        """
        Create the parts list section in the right panel.
        """
        # Header frame with title and search
        header_frame = ttk.Frame(self.right_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Parts list header
        self.parts_header = ttk.Label(header_frame, text="All Parts", style="Section.TLabel")
        self.parts_header.pack(side=tk.LEFT, padx=5)
        
        # Search entry
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="Search: ").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_button = ttk.Button(
            search_frame, 
            text="Search", 
            command=self.on_search
        )
        self.search_button.pack(side=tk.LEFT)
        
        # Parts treeview with scrollbar
        tree_frame = ttk.Frame(self.right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create vertical scrollbar
        vscrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create horizontal scrollbar
        hscrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create treeview
        self.parts_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Category", "Price"),
            show="headings",
            yscrollcommand=vscrollbar.set,
            xscrollcommand=hscrollbar.set
        )
        self.parts_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        vscrollbar.config(command=self.parts_tree.yview)
        hscrollbar.config(command=self.parts_tree.xview)
        
        # Configure columns
        self.parts_tree.heading("ID", text="ID")
        self.parts_tree.heading("Name", text="Name")
        self.parts_tree.heading("Category", text="Category")
        self.parts_tree.heading("Price", text="Price")
        
        self.parts_tree.column("ID", width=60, minwidth=50)
        self.parts_tree.column("Name", width=200, minwidth=150)
        self.parts_tree.column("Category", width=100, minwidth=80)
        self.parts_tree.column("Price", width=80, minwidth=70)
        
        # Bind event
        self.parts_tree.bind("<<TreeviewSelect>>", self.on_part_select)
    
    def create_part_details_section(self):
        """
        Create the part details section in the right panel.
        """
        # Part details frame
        self.details_frame = ttk.LabelFrame(self.right_frame, text="Part Details")
        self.details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Detail fields - using a grid layout
        self.detail_fields = {}
        
        fields = [
            ("Name", "name"),
            ("ID", "part_id"),
            ("Category", "category"),
            ("Price", "price"),
            ("Description", "description")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(self.details_frame, text=f"{label_text}:").grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2
            )
            
            value_var = tk.StringVar()
            self.detail_fields[field_name] = value_var
            
            ttk.Label(
                self.details_frame, 
                textvariable=value_var,
                wraplength=400
            ).grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Compatible vehicles section
        ttk.Label(self.details_frame, text="Compatible Vehicles:").grid(
            row=len(fields), column=0, sticky=tk.NW, padx=5, pady=2
        )
        
        # Scrollable listbox for compatible vehicles
        compat_frame = ttk.Frame(self.details_frame)
        compat_frame.grid(row=len(fields), column=1, sticky=tk.EW, padx=5, pady=2)
        
        scrollbar = ttk.Scrollbar(compat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.compat_listbox = tk.Listbox(
            compat_frame,
            height=5,
            yscrollcommand=scrollbar.set
        )
        self.compat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.compat_listbox.yview)
        
        # Initially hide the details
        self.details_frame.pack_forget()
    
    def load_categories(self):
        """
        Load the categories into the listbox.
        """
        # Clear current items (except "All Categories")
        self.categories_listbox.delete(1, tk.END)
        
        # Add categories from the catalog
        for category in self.app.catalog.get_categories():
            self.categories_listbox.insert(tk.END, category.name)
    
    def load_parts(self, parts=None):
        """
        Load parts into the treeview.
        
        Args:
            parts: List of parts to display. If None, display all parts.
        """
        # Clear current items
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        # Get parts to display
        if parts is None:
            parts = self.app.catalog.get_parts()
        
        # Add parts to the treeview
        for part in parts:
            self.parts_tree.insert(
                "", 
                tk.END, 
                values=(
                    part.part_id, 
                    part.name, 
                    part.category, 
                    f"${part.price:.2f}"
                ),
                tags=(str(part.part_id),)
            )
    
    def display_part_details(self, part: Part):
        """
        Display the details of a part.
        
        Args:
            part: The part to display details for
        """
        # Show the details frame if hidden
        self.details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Update the detail fields
        self.detail_fields["name"].set(part.name)
        self.detail_fields["part_id"].set(str(part.part_id))
        self.detail_fields["category"].set(part.category)
        self.detail_fields["price"].set(f"${part.price:.2f}")
        self.detail_fields["description"].set(part.description)
        
        # Clear and update the compatible vehicles list
        self.compat_listbox.delete(0, tk.END)
        
        if part.compatible_vehicles:
            compat_list = []
            for compat in part.compatible_vehicles:
                make, model, year = compat.split(":")
                compat_list.append(f"{year} {make} {model}")
            
            # Sort by make, then model, then year
            compat_list.sort()
            
            for compat in compat_list:
                self.compat_listbox.insert(tk.END, compat)
        else:
            self.compat_listbox.insert(tk.END, "No compatible vehicles found")
    
    def on_category_select(self, event):
        """
        Handle category selection event.
        
        Args:
            event: The event object
        """
        # Get the selected category
        selection = self.categories_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        category_name = self.categories_listbox.get(index)
        
        # Update the current category
        self.current_category = None if category_name == "All Categories" else category_name
        
        # Update the header
        self.parts_header.config(
            text=f"All Parts" if category_name == "All Categories" else f"{category_name}"
        )
        
        # Filter parts by category
        if category_name == "All Categories":
            parts = self.app.catalog.get_parts()
        else:
            parts = self.app.catalog.get_parts_by_category(category_name)
        
        # Update the parts list
        self.load_parts(parts)
        
        # Clear search
        self.search_var.set("")
    
    def on_part_select(self, event):
        """
        Handle part selection event.
        
        Args:
            event: The event object
        """
        # Get the selected part
        selection = self.parts_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        part_id = int(self.parts_tree.item(item, "values")[0])
        
        # Get the part object
        part = self.app.catalog.get_part(part_id)
        if part:
            # Display the part details
            self.display_part_details(part)
    
    def on_search(self):
        """
        Handle search button click.
        """
        query = self.search_var.get().strip()
        if not query:
            # If search is empty, just show the current category
            self.on_category_select(None)
            return
        
        # Search for parts
        results = self.app.catalog.search_parts(query)
        
        # If a category is selected, filter by category
        if self.current_category:
            filtered_results = []
            for part in results:
                if part.category == self.current_category:
                    filtered_results.append(part)
            results = filtered_results
        
        # Update the parts list
        self.load_parts(results)
        
        # Update header
        if self.current_category:
            self.parts_header.config(
                text=f"{self.current_category} - Search: {query}"
            )
        else:
            self.parts_header.config(
                text=f"Search: {query}"
            )
    
    def on_data_loaded(self):
        """
        Called when data is loaded into the application.
        """
        # Load categories and parts
        self.load_categories()
        self.load_parts()
        
        # Select "All Categories" by default
        self.categories_listbox.selection_set(0)
