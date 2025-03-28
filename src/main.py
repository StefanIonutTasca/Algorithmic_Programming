#!/usr/bin/env python3
"""
Automotive Parts Catalog System
Main entry point for the application
"""
import time
import os
import random
from typing import List, TypeVar, Generic, Callable, Any

from src.datastructures.array_list import ArrayList
from src.datastructures.linked_list import LinkedList
from src.algorithms.sort import merge_sort, quick_sort
from src.models.part import Part, PartCategory, PartCatalog
from src.models.vehicle import VehicleMake, VehicleModel, VehicleYear, VehicleRegistry
from src.utils.data_loader import DataLoader

T = TypeVar('T')

def measure_execution_time(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Measure the execution time of a function.
    
    Args:
        func: The function to measure
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        A tuple containing (function_result, execution_time_in_seconds)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def print_header(title: str) -> None:
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50)

def print_section(title: str) -> None:
    """Print a formatted section title"""
    print("\n" + "-" * 50)
    print(f" {title} ".center(50, "-"))
    print("-" * 50)

def print_result(operation: str, data_structure: str, time_taken: float) -> None:
    """Print formatted result of an operation"""
    print(f"{operation} using {data_structure}: {time_taken:.6f} seconds")

def compare_data_structures(parts: List[Part], sample_size: int = None) -> None:
    """
    Compare the performance of ArrayList and LinkedList.
    
    Args:
        parts: List of parts to use for comparison
        sample_size: Number of parts to use (None means all)
    """
    if sample_size is not None and sample_size < len(parts):
        sample_parts = random.sample(parts, sample_size)
    else:
        sample_parts = parts
        sample_size = len(parts)
    
    print_header(f"Data Structure Comparison ({sample_size} parts)")
    
    # Create data structures
    array_list = ArrayList[Part]()
    linked_list = LinkedList[Part]()
    
    # Test insertion
    print_section("Insertion Performance")
    
    # ArrayList insertion
    _, array_insert_time = measure_execution_time(
        lambda: [array_list.append(part) for part in sample_parts]
    )
    print_result("Insert", "ArrayList", array_insert_time)
    
    # LinkedList insertion
    _, linked_insert_time = measure_execution_time(
        lambda: [linked_list.append(part) for part in sample_parts]
    )
    print_result("Insert", "LinkedList", linked_insert_time)
    
    # Test access
    print_section("Access Performance")
    
    # Test random access (ArrayList strength)
    n = len(sample_parts)
    indices = [random.randint(0, n-1) for _ in range(min(1000, n))]
    
    # ArrayList access
    _, array_access_time = measure_execution_time(
        lambda: [array_list.get(i) for i in indices]
    )
    print_result("Random Access", "ArrayList", array_access_time)
    
    # LinkedList access (expected to be slower)
    _, linked_access_time = measure_execution_time(
        lambda: [linked_list.get(i) for i in indices]
    )
    print_result("Random Access", "LinkedList", linked_access_time)
    
    # Test deletion
    print_section("Deletion Performance")
    
    # Create new instances with data for deletion test
    array_list_delete = ArrayList[Part]()
    linked_list_delete = LinkedList[Part]()
    
    for part in sample_parts:
        array_list_delete.append(part)
        linked_list_delete.append(part)
    
    # Delete from middle and measure performance
    delete_indices = sorted([random.randint(0, n-1) for _ in range(min(100, n//2))], reverse=True)
    
    # ArrayList deletion
    _, array_delete_time = measure_execution_time(
        lambda: [array_list_delete.remove_at(i) for i in delete_indices]
    )
    print_result("Delete", "ArrayList", array_delete_time)
    
    # LinkedList deletion
    _, linked_delete_time = measure_execution_time(
        lambda: [linked_list_delete.remove_at(i) for i in delete_indices]
    )
    print_result("Delete", "LinkedList", linked_delete_time)

def compare_sorting_algorithms(parts: List[Part], sample_size: int = None) -> None:
    """
    Compare the performance of QuickSort and MergeSort.
    
    Args:
        parts: List of parts to use for comparison
        sample_size: Number of parts to use (None means all)
    """
    if sample_size is not None and sample_size < len(parts):
        sample_parts = random.sample(parts, sample_size)
    else:
        sample_parts = parts
        sample_size = len(parts)
    
    print_header(f"Sorting Algorithm Comparison ({sample_size} parts)")
    
    # Define comparison function for sorting
    def compare_by_price(a: Part, b: Part) -> int:
        if a.price < b.price:
            return -1
        elif a.price > b.price:
            return 1
        return 0
    
    # Test sorting by price
    print_section("Sorting by Price")
    
    # Make copies of the parts list for each sort
    parts_for_quick = sample_parts.copy()
    parts_for_merge = sample_parts.copy()
    
    # QuickSort
    _, quick_sort_time = measure_execution_time(
        quick_sort, parts_for_quick, 0, len(parts_for_quick) - 1, compare_by_price
    )
    print_result("Sort", "QuickSort", quick_sort_time)
    
    # MergeSort
    _, merge_sort_time = measure_execution_time(
        merge_sort, parts_for_merge, 0, len(parts_for_merge) - 1, compare_by_price
    )
    print_result("Sort", "MergeSort", merge_sort_time)
    
    # Verify sorting worked correctly
    is_quick_sorted = all(parts_for_quick[i].price <= parts_for_quick[i+1].price 
                          for i in range(len(parts_for_quick)-1))
    is_merge_sorted = all(parts_for_merge[i].price <= parts_for_merge[i+1].price 
                          for i in range(len(parts_for_merge)-1))
    
    print(f"\nQuickSort produced correct sorting: {is_quick_sorted}")
    print(f"MergeSort produced correct sorting: {is_merge_sorted}")
    
    # Also sort by name (string comparison)
    print_section("Sorting by Name")
    
    def compare_by_name(a: Part, b: Part) -> int:
        return -1 if a.name < b.name else 1 if a.name > b.name else 0
    
    # Make new copies
    parts_for_quick = sample_parts.copy()
    parts_for_merge = sample_parts.copy()
    
    # QuickSort
    _, quick_sort_time = measure_execution_time(
        quick_sort, parts_for_quick, 0, len(parts_for_quick) - 1, compare_by_name
    )
    print_result("Sort", "QuickSort", quick_sort_time)
    
    # MergeSort
    _, merge_sort_time = measure_execution_time(
        merge_sort, parts_for_merge, 0, len(parts_for_merge) - 1, compare_by_name
    )
    print_result("Sort", "MergeSort", merge_sort_time)

def main():
    """
    Main function to start the application
    """
    print_header("Automotive Parts Catalog System")
    print("Loading data...")
    
    # Create catalog and registry
    catalog = PartCatalog()
    registry = VehicleRegistry()
    
    # Generate sample data
    DataLoader.generate_sample_data(catalog, registry, num_parts=1000)
    
    print(f"Loaded {len(catalog.get_parts())} parts")
    print(f"Loaded {len(registry.get_makes())} vehicle makes")
    
    # Get all parts as a list
    all_parts = catalog.get_parts()
    
    # Compare data structures with different dataset sizes
    for size in [50, 200, 500, 1000]:
        if size <= len(all_parts):
            compare_data_structures(all_parts, size)
    
    # Compare sorting algorithms with different dataset sizes
    for size in [50, 200, 500, 1000]:
        if size <= len(all_parts):
            compare_sorting_algorithms(all_parts, size)
    
    print_header("Demo Complete")
    print("This console application demonstrates the performance of:")
    print("1. ArrayList vs LinkedList data structures")
    print("2. QuickSort vs MergeSort sorting algorithms")
    print("\nFor the full GUI application, please run the GUI module.")

if __name__ == "__main__":
    main()
