"""
Performance panel for the Automotive Parts Catalog System.
This module provides the user interface for demonstrating and visualizing algorithm performance.
"""
import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict, Any, Tuple, Optional

from ..algorithms.search_algorithms import SearchAlgorithms
from ..algorithms.sort import quick_sort, merge_sort
from ..datastructures.array_list import ArrayList
from ..datastructures.linked_list import LinkedList
from ..datastructures.BinarySearchTree import BinarySearchTree


class PerformancePanel(ttk.Frame):
    """
    Panel for demonstrating and visualizing algorithm performance.
    
    This class creates and manages the user interface for running algorithm
    demonstrations and displaying their performance metrics.
    """
    
    def __init__(self, parent):
        """
        Initialize the performance panel.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        
        # Create a notebook with tabs for different algorithm categories
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs for different algorithm categories
        self._search_frame = ttk.Frame(self._notebook)
        self._sort_frame = ttk.Frame(self._notebook)
        self._data_structure_frame = ttk.Frame(self._notebook)
        
        self._notebook.add(self._search_frame, text="Search Algorithms")
        self._notebook.add(self._sort_frame, text="Sort Algorithms")
        self._notebook.add(self._data_structure_frame, text="Data Structures")
        
        # Setup each tab
        self._setup_search_tab()
        self._setup_sort_tab()
        self._setup_data_structure_tab()
    
    def _setup_search_tab(self):
        """Setup the search algorithms tab"""
        # Create a frame for controls
        controls_frame = ttk.LabelFrame(self._search_frame, text="Search Algorithm Testing")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create algorithm selection
        ttk.Label(controls_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self._search_algorithm_var = tk.StringVar()
        algorithm_combobox = ttk.Combobox(controls_frame, textvariable=self._search_algorithm_var, state="readonly")
        algorithm_combobox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        algorithm_combobox["values"] = ["Linear Search", "Binary Search", "Compare Both"]
        algorithm_combobox.current(2)  # Default to "Compare Both"
        
        # Create data structure selection
        ttk.Label(controls_frame, text="Data Structure:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self._search_structure_var = tk.StringVar()
        structure_combobox = ttk.Combobox(controls_frame, textvariable=self._search_structure_var, state="readonly")
        structure_combobox.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        structure_combobox["values"] = ["ArrayList", "LinkedList", "BinarySearchTree"]
        structure_combobox.current(0)  # Default to ArrayList
        
        # Create data size selection
        ttk.Label(controls_frame, text="Data Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self._search_size_var = tk.StringVar()
        size_combobox = ttk.Combobox(controls_frame, textvariable=self._search_size_var, state="readonly")
        size_combobox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        size_combobox["values"] = ["100", "1,000", "10,000", "100,000"]
        size_combobox.current(1)  # Default to 1,000
        
        # Run button
        self._search_run_button = ttk.Button(controls_frame, text="Run Test", command=self._run_search_test)
        self._search_run_button.grid(row=1, column=3, sticky=tk.E, padx=5, pady=5)
        
        # Create a frame for the chart
        chart_frame = ttk.LabelFrame(self._search_frame, text="Performance Results")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create matplotlib figure for visualization
        self._search_figure = plt.Figure(figsize=(6, 4), dpi=100)
        self._search_subplot = self._search_figure.add_subplot(111)
        self._search_canvas = FigureCanvasTkAgg(self._search_figure, chart_frame)
        self._search_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        self._search_results_text = tk.Text(self._search_frame, height=5, wrap=tk.WORD)
        self._search_results_text.pack(fill=tk.X, padx=5, pady=5)
        
    def _setup_sort_tab(self):
        """Setup the sort algorithms tab"""
        # Create a frame for controls
        controls_frame = ttk.LabelFrame(self._sort_frame, text="Sort Algorithm Testing")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create algorithm selection
        ttk.Label(controls_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self._sort_algorithm_var = tk.StringVar()
        algorithm_combobox = ttk.Combobox(controls_frame, textvariable=self._sort_algorithm_var, state="readonly")
        algorithm_combobox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        algorithm_combobox["values"] = ["Quick Sort", "Merge Sort", "Compare Both"]
        algorithm_combobox.current(2)  # Default to "Compare Both"
        
        # Create data structure selection
        ttk.Label(controls_frame, text="Data Structure:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self._sort_structure_var = tk.StringVar()
        structure_combobox = ttk.Combobox(controls_frame, textvariable=self._sort_structure_var, state="readonly")
        structure_combobox.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        structure_combobox["values"] = ["ArrayList", "LinkedList"]
        structure_combobox.current(0)  # Default to ArrayList
        
        # Create data size selection
        ttk.Label(controls_frame, text="Data Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self._sort_size_var = tk.StringVar()
        size_combobox = ttk.Combobox(controls_frame, textvariable=self._sort_size_var, state="readonly")
        size_combobox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        size_combobox["values"] = ["100", "1,000", "5,000", "10,000"]
        size_combobox.current(1)  # Default to 1,000
        
        # Run button
        self._sort_run_button = ttk.Button(controls_frame, text="Run Test", command=self._run_sort_test)
        self._sort_run_button.grid(row=1, column=3, sticky=tk.E, padx=5, pady=5)
        
        # Create a frame for the chart
        chart_frame = ttk.LabelFrame(self._sort_frame, text="Performance Results")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create matplotlib figure for visualization
        self._sort_figure = plt.Figure(figsize=(6, 4), dpi=100)
        self._sort_subplot = self._sort_figure.add_subplot(111)
        self._sort_canvas = FigureCanvasTkAgg(self._sort_figure, chart_frame)
        self._sort_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        self._sort_results_text = tk.Text(self._sort_frame, height=5, wrap=tk.WORD)
        self._sort_results_text.pack(fill=tk.X, padx=5, pady=5)
        
    def _setup_data_structure_tab(self):
        """Setup the data structures tab"""
        # Create a frame for controls
        controls_frame = ttk.LabelFrame(self._data_structure_frame, text="Data Structure Testing")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create operation selection
        ttk.Label(controls_frame, text="Operation:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self._ds_operation_var = tk.StringVar()
        operation_combobox = ttk.Combobox(controls_frame, textvariable=self._ds_operation_var, state="readonly")
        operation_combobox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        operation_combobox["values"] = ["Insert", "Delete", "Search", "Compare All"]
        operation_combobox.current(3)  # Default to "Compare All"
        
        # Create data structure selection
        ttk.Label(controls_frame, text="Data Structures:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self._ds_structures_var = tk.StringVar()
        structure_combobox = ttk.Combobox(controls_frame, textvariable=self._ds_structures_var, state="readonly")
        structure_combobox.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        structure_combobox["values"] = ["ArrayList", "LinkedList", "BinarySearchTree", "Compare All"]
        structure_combobox.current(3)  # Default to "Compare All"
        
        # Create data size selection
        ttk.Label(controls_frame, text="Data Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self._ds_size_var = tk.StringVar()
        size_combobox = ttk.Combobox(controls_frame, textvariable=self._ds_size_var, state="readonly")
        size_combobox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        size_combobox["values"] = ["100", "1,000", "5,000", "10,000"]
        size_combobox.current(1)  # Default to 1,000
        
        # Run button
        self._ds_run_button = ttk.Button(controls_frame, text="Run Test", command=self._run_data_structure_test)
        self._ds_run_button.grid(row=1, column=3, sticky=tk.E, padx=5, pady=5)
        
        # Create a frame for the chart
        chart_frame = ttk.LabelFrame(self._data_structure_frame, text="Performance Results")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create matplotlib figure for visualization
        self._ds_figure = plt.Figure(figsize=(6, 4), dpi=100)
        self._ds_subplot = self._ds_figure.add_subplot(111)
        self._ds_canvas = FigureCanvasTkAgg(self._ds_figure, chart_frame)
        self._ds_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        self._ds_results_text = tk.Text(self._data_structure_frame, height=5, wrap=tk.WORD)
        self._ds_results_text.pack(fill=tk.X, padx=5, pady=5)
    
    def _run_search_test(self):
        """Run the selected search algorithm test"""
        # Get parameters
        algorithm = self._search_algorithm_var.get()
        structure = self._search_structure_var.get()
        try:
            size = int(self._search_size_var.get().replace(",", ""))
        except ValueError:
            self._search_results_text.delete(1.0, tk.END)
            self._search_results_text.insert(tk.END, "Invalid data size")
            return
        
        # Clear previous results
        self._search_results_text.delete(1.0, tk.END)
        self._search_subplot.clear()
        
        # Generate test data
        data = self._generate_test_data(size)
        
        # Create appropriate data structure
        structured_data = self._convert_to_structure(data, structure)
        
        # Select a random target that exists in the data
        target_index = random.randint(0, len(data) - 1)
        target = data[target_index]
        
        # Prepare for chart
        algorithms = []
        times = []
        
        # Run the tests
        if algorithm in ["Linear Search", "Compare Both"]:
            # Measure linear search time
            start_time = time.time()
            if structure == "ArrayList" or structure == "LinkedList":
                # Use linear search for these structures
                result, search_time = SearchAlgorithms.linear_search(structured_data, target)
            else:
                # For BST, use its own search method
                result = structured_data.search(target)
                search_time = time.time() - start_time
            
            # Add to results
            algorithms.append("Linear Search")
            times.append(search_time)
            
            # Display result
            self._search_results_text.insert(tk.END, f"Linear Search on {structure} (size {size}):\n")
            self._search_results_text.insert(tk.END, f"Found at index {result}\n")
            self._search_results_text.insert(tk.END, f"Time: {search_time:.6f} seconds\n\n")
        
        if algorithm in ["Binary Search", "Compare Both"] and structure != "LinkedList":
            # Binary search requires sorted data for ArrayList
            if structure == "ArrayList":
                # Sort the data first
                sorted_data = sorted(structured_data)
                
                # Measure binary search time
                start_time = time.time()
                result, search_time = SearchAlgorithms.binary_search(sorted_data, target)
                
                # Add to results
                algorithms.append("Binary Search")
                times.append(search_time)
                
                # Display result
                self._search_results_text.insert(tk.END, f"Binary Search on {structure} (size {size}):\n")
                self._search_results_text.insert(tk.END, f"Found at index {result}\n")
                self._search_results_text.insert(tk.END, f"Time: {search_time:.6f} seconds\n\n")
            elif structure == "BinarySearchTree":
                # BST already supports efficient search
                # Display result
                self._search_results_text.insert(tk.END, "Binary Search is inherent in BinarySearchTree implementation\n")
        
        # Plot the results if we have any
        if times:
            self._search_subplot.bar(algorithms, times)
            self._search_subplot.set_xlabel("Algorithm")
            self._search_subplot.set_ylabel("Time (seconds)")
            self._search_subplot.set_title(f"Search Performance ({structure}, size {size})")
            
            # Format y-axis as milliseconds if times are very small
            if max(times) < 0.01:
                self._search_subplot.set_ylabel("Time (milliseconds)")
                self._search_subplot.set_yticklabels([f"{t*1000:.2f}" for t in self._search_subplot.get_yticks()])
            
            self._search_figure.tight_layout()
            self._search_canvas.draw()
    
    def _run_sort_test(self):
        """Run the selected sort algorithm test"""
        # Get parameters
        algorithm = self._sort_algorithm_var.get()
        structure = self._sort_structure_var.get()
        try:
            size = int(self._sort_size_var.get().replace(",", ""))
        except ValueError:
            self._sort_results_text.delete(1.0, tk.END)
            self._sort_results_text.insert(tk.END, "Invalid data size")
            return
        
        # Clear previous results
        self._sort_results_text.delete(1.0, tk.END)
        self._sort_subplot.clear()
        
        # Generate test data
        data = self._generate_test_data(size)
        
        # Create appropriate data structure
        structured_data = self._convert_to_structure(data, structure)
        
        # Prepare for chart
        algorithms = []
        times = []
        
        # Run the tests
        if algorithm in ["Quick Sort", "Compare Both"]:
            # Deep copy of data to avoid modifying the original
            quick_data = data.copy()
            
            # Measure quick sort time
            start_time = time.time()
            quick_result = quick_sort(quick_data)
            end_time = time.time()
            quick_time = end_time - start_time
            
            # Add to results
            algorithms.append("Quick Sort")
            times.append(quick_time)
            
            # Display result
            self._sort_results_text.insert(tk.END, f"Quick Sort on {structure} (size {size}):\n")
            self._sort_results_text.insert(tk.END, f"Time: {quick_time:.6f} seconds\n\n")
        
        if algorithm in ["Merge Sort", "Compare Both"]:
            # Deep copy of data to avoid modifying the original
            merge_data = data.copy()
            
            # Measure merge sort time
            start_time = time.time()
            merge_result = merge_sort(merge_data)
            end_time = time.time()
            merge_time = end_time - start_time
            
            # Add to results
            algorithms.append("Merge Sort")
            times.append(merge_time)
            
            # Display result
            self._sort_results_text.insert(tk.END, f"Merge Sort on {structure} (size {size}):\n")
            self._sort_results_text.insert(tk.END, f"Time: {merge_time:.6f} seconds\n\n")
        
        # Plot the results if we have any
        if times:
            self._sort_subplot.bar(algorithms, times)
            self._sort_subplot.set_xlabel("Algorithm")
            self._sort_subplot.set_ylabel("Time (seconds)")
            self._sort_subplot.set_title(f"Sort Performance ({structure}, size {size})")
            
            # Format y-axis as milliseconds if times are very small
            if max(times) < 0.01:
                self._sort_subplot.set_ylabel("Time (milliseconds)")
                self._sort_subplot.set_yticklabels([f"{t*1000:.2f}" for t in self._sort_subplot.get_yticks()])
            
            self._sort_figure.tight_layout()
            self._sort_canvas.draw()
    
    def _run_data_structure_test(self):
        """Run the selected data structure test"""
        # Get parameters
        operation = self._ds_operation_var.get()
        structure_choice = self._ds_structures_var.get()
        try:
            size = int(self._ds_size_var.get().replace(",", ""))
        except ValueError:
            self._ds_results_text.delete(1.0, tk.END)
            self._ds_results_text.insert(tk.END, "Invalid data size")
            return
        
        # Clear previous results
        self._ds_results_text.delete(1.0, tk.END)
        self._ds_subplot.clear()
        
        # Generate test data
        data = self._generate_test_data(size)
        
        # Determine which structures to test
        structures = []
        if structure_choice == "Compare All" or structure_choice == "ArrayList":
            structures.append("ArrayList")
        if structure_choice == "Compare All" or structure_choice == "LinkedList":
            structures.append("LinkedList")
        if structure_choice == "Compare All" or structure_choice == "BinarySearchTree":
            structures.append("BinarySearchTree")
        
        # Prepare for chart
        structure_names = []
        operation_times = []
        
        for structure_name in structures:
            # Create an empty structure
            if structure_name == "ArrayList":
                structure = ArrayList()
            elif structure_name == "LinkedList":
                structure = LinkedList()
            elif structure_name == "BinarySearchTree":
                structure = BinarySearchTree()
            
            # Test insert operation
            if operation == "Insert" or operation == "Compare All":
                # Measure insert time
                start_time = time.time()
                for item in data:
                    if structure_name == "BinarySearchTree":
                        structure.insert(item)
                    else:
                        structure.append(item)
                end_time = time.time()
                insert_time = end_time - start_time
                
                if operation == "Insert":
                    structure_names.append(structure_name)
                    operation_times.append(insert_time)
                
                # Display result
                self._ds_results_text.insert(tk.END, f"Insert {size} items into {structure_name}:\n")
                self._ds_results_text.insert(tk.END, f"Time: {insert_time:.6f} seconds\n\n")
            
            # We need to populate the structure for the other operations
            if operation != "Insert":
                for item in data:
                    if structure_name == "BinarySearchTree":
                        structure.insert(item)
                    else:
                        structure.append(item)
            
            # Test search operation
            if operation == "Search" or operation == "Compare All":
                # Select items to search for
                search_items = random.sample(data, min(100, size))
                
                # Measure search time
                start_time = time.time()
                for item in search_items:
                    if structure_name == "BinarySearchTree":
                        structure.search(item)
                    elif structure_name == "ArrayList" or structure_name == "LinkedList":
                        try:
                            structure.index_of(item)
                        except:
                            # If index_of is not implemented, just check if item is in the structure
                            item in structure
                end_time = time.time()
                search_time = end_time - start_time
                
                if operation == "Search":
                    structure_names.append(structure_name)
                    operation_times.append(search_time)
                
                # Display result
                self._ds_results_text.insert(tk.END, f"Search for {len(search_items)} items in {structure_name}:\n")
                self._ds_results_text.insert(tk.END, f"Time: {search_time:.6f} seconds\n\n")
            
            # Test delete operation
            if operation == "Delete" or operation == "Compare All":
                # Select items to delete
                delete_items = random.sample(data, min(100, size))
                
                # Measure delete time
                start_time = time.time()
                for item in delete_items:
                    if structure_name == "BinarySearchTree":
                        structure.delete(item)
                    elif structure_name == "ArrayList" or structure_name == "LinkedList":
                        try:
                            structure.remove(item)
                        except:
                            # If remove is not implemented, we'll just note that
                            pass
                end_time = time.time()
                delete_time = end_time - start_time
                
                if operation == "Delete":
                    structure_names.append(structure_name)
                    operation_times.append(delete_time)
                
                # Display result
                self._ds_results_text.insert(tk.END, f"Delete {len(delete_items)} items from {structure_name}:\n")
                self._ds_results_text.insert(tk.END, f"Time: {delete_time:.6f} seconds\n\n")
            
            # For "Compare All" operation, we'll add all three operations to the chart
            if operation == "Compare All":
                if structure_name == "ArrayList":
                    structure_names.extend(["ArrayList-Insert", "ArrayList-Search", "ArrayList-Delete"])
                    operation_times.extend([insert_time, search_time, delete_time])
                elif structure_name == "LinkedList":
                    structure_names.extend(["LinkedList-Insert", "LinkedList-Search", "LinkedList-Delete"])
                    operation_times.extend([insert_time, search_time, delete_time])
                elif structure_name == "BinarySearchTree":
                    structure_names.extend(["BST-Insert", "BST-Search", "BST-Delete"])
                    operation_times.extend([insert_time, search_time, delete_time])
        
        # Plot the results if we have any
        if operation_times:
            # For "Compare All" operations, group by operation type
            if operation == "Compare All" and structure_choice == "Compare All":
                # Reorganize data for grouped bar chart
                insert_times = [operation_times[i] for i in range(0, len(operation_times), 3)]
                search_times = [operation_times[i] for i in range(1, len(operation_times), 3)]
                delete_times = [operation_times[i] for i in range(2, len(operation_times), 3)]
                
                # Create x positions
                x = range(len(insert_times))
                width = 0.25
                
                # Create grouped bar chart
                self._ds_subplot.bar([i - width for i in x], insert_times, width, label='Insert')
                self._ds_subplot.bar(x, search_times, width, label='Search')
                self._ds_subplot.bar([i + width for i in x], delete_times, width, label='Delete')
                
                # Set labels
                self._ds_subplot.set_xlabel("Data Structure")
                self._ds_subplot.set_ylabel("Time (seconds)")
                self._ds_subplot.set_title(f"Data Structure Operations (size {size})")
                self._ds_subplot.set_xticks(x)
                self._ds_subplot.set_xticklabels(["ArrayList", "LinkedList", "BinarySearchTree"])
                self._ds_subplot.legend()
            else:
                # Simple bar chart for specific operation or structure
                self._ds_subplot.bar(structure_names, operation_times)
                self._ds_subplot.set_xlabel("Data Structure")
                self._ds_subplot.set_ylabel("Time (seconds)")
                if operation != "Compare All":
                    self._ds_subplot.set_title(f"{operation} Performance (size {size})")
                else:
                    self._ds_subplot.set_title(f"Data Structure Operations for {structure_choice} (size {size})")
            
            # Format y-axis as milliseconds if times are very small
            if max(operation_times) < 0.01:
                self._ds_subplot.set_ylabel("Time (milliseconds)")
                self._ds_subplot.set_yticklabels([f"{t*1000:.2f}" for t in self._ds_subplot.get_yticks()])
            
            self._ds_figure.tight_layout()
            self._ds_canvas.draw()
    
    def _generate_test_data(self, size: int) -> List[int]:
        """
        Generate random test data.
        
        Args:
            size: Number of data items to generate
            
        Returns:
            List of random integers
        """
        return [random.randint(1, 10000) for _ in range(size)]
    
    def _convert_to_structure(self, data, structure_name):
        """
        Convert data to the specified data structure.
        
        Args:
            data: List of data to convert
            structure_name: Name of the structure to convert to
            
        Returns:
            The data in the specified structure
        """
        if structure_name == "ArrayList":
            result = ArrayList()
            for item in data:
                result.append(item)  
            return result
        elif structure_name == "LinkedList":
            result = LinkedList()
            for item in data:
                result.append(item)  
            return result
        elif structure_name == "BinarySearchTree":
            result = BinarySearchTree()
            for item in data:
                result.insert(item)  
            return result
        else:
            # Default to returning the original list
            return data
