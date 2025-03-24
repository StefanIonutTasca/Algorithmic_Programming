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
        
        # Create a frame for controls
        controls_frame = ttk.LabelFrame(self, text="Performance Testing")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create algorithm selection
        ttk.Label(controls_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self._algorithm_var = tk.StringVar()
        algorithm_combobox = ttk.Combobox(controls_frame, textvariable=self._algorithm_var, state="readonly")
        algorithm_combobox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        algorithm_combobox["values"] = ["Linear Search", "Binary Search", "Compare Both"]
        algorithm_combobox.current(2)  # Default to "Compare Both"
        
        # Create data size selection
        ttk.Label(controls_frame, text="Data Size:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self._size_var = tk.StringVar()
        size_combobox = ttk.Combobox(controls_frame, textvariable=self._size_var, state="readonly")
        size_combobox.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        size_combobox["values"] = ["100", "1,000", "10,000", "100,000"]
        size_combobox.current(1)  # Default to 1,000
        
        # Create run button
        run_button = ttk.Button(controls_frame, text="Run Test", command=self._on_run_test)
        run_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Create a frame for results
        results_frame = ttk.LabelFrame(self, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a canvas for the chart
        self._fig, self._ax = plt.subplots(figsize=(8, 4))
        self._canvas = FigureCanvasTkAgg(self._fig, master=results_frame)
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize with an empty chart
        self._ax.set_title("Algorithm Performance Comparison")
        self._ax.set_xlabel("Algorithm")
        self._ax.set_ylabel("Execution Time (seconds)")
        self._fig.tight_layout()
        self._canvas.draw()
        
        # Configure grid weights
        for i in range(5):
            controls_frame.grid_columnconfigure(i, weight=1)
    
    def _on_run_test(self) -> None:
        """
        Handle the run test button click.
        """
        algorithm = self._algorithm_var.get()
        
        try:
            size_str = self._size_var.get().replace(',', '')
            size = int(size_str)
        except ValueError:
            size = 1000  # Default size
        
        self.run_algorithm_demo(algorithm, size)
    
    def run_algorithm_demo(self, algorithm_name: str, data_size: int) -> None:
        """
        Run a demonstration of the specified algorithm and display the results.
        
        Args:
            algorithm_name: Name of the algorithm to demonstrate
            data_size: Size of the data to use
        """
        # Generate random data
        data = [random.randint(1, 1000000) for _ in range(data_size)]
        
        # Sort the data for binary search
        sorted_data = sorted(data)
        
        # Choose a random target (ensure it exists in the data)
        target_index = random.randint(0, data_size - 1)
        target = data[target_index]
        
        # Run the algorithms
        results = {}
        
        if algorithm_name == "Linear Search" or algorithm_name == "Compare Both":
            start_time = time.time()
            index, _ = SearchAlgorithms.linear_search(data, target)
            end_time = time.time()
            results["Linear Search"] = (index, end_time - start_time)
        
        if algorithm_name == "Binary Search" or algorithm_name == "Compare Both":
            # Find the target in the sorted list
            target_in_sorted = target
            sorted_index = sorted_data.index(target)
            
            start_time = time.time()
            index, _ = SearchAlgorithms.binary_search(sorted_data, target_in_sorted)
            end_time = time.time()
            results["Binary Search"] = (index, end_time - start_time)
        
        # Update the chart
        self._update_chart(results, algorithm_name, data_size, target)
    
    def _update_chart(self, results: Dict[str, Tuple[int, float]], algorithm_name: str, 
                      data_size: int, target: int) -> None:
        """
        Update the chart with the algorithm performance results.
        
        Args:
            results: Dictionary of algorithm results
            algorithm_name: Name of the algorithm
            data_size: Size of the data used
            target: Target value that was searched for
        """
        # Clear the previous chart
        self._ax.clear()
        
        # Extract algorithm names and execution times
        algorithms = list(results.keys())
        times = [results[alg][1] for alg in algorithms]
        
        # Create a bar chart
        bars = self._ax.bar(algorithms, times)
        
        # Add labels
        for bar in bars:
            height = bar.get_height()
            self._ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.0001,
                f"{height:.4f}",
                ha="center"
            )
        
        # Add titles and labels
        title = f"Search Algorithm Performance ({data_size:,} elements)"
        if algorithm_name == "Compare Both":
            title += "\nTarget value: " + str(target)
        
        self._ax.set_title(title)
        self._ax.set_xlabel("Algorithm")
        self._ax.set_ylabel("Execution Time (seconds)")
        
        # Update the chart
        self._fig.tight_layout()
        self._canvas.draw()
        
        # Print a summary
        print(f"Algorithm Performance Summary:")
        print(f"Data Size: {data_size:,}")
        print(f"Target Value: {target}")
        for alg, (index, time_taken) in results.items():
            print(f"{alg}: Found at index {index}, Time: {time_taken:.6f} seconds")
