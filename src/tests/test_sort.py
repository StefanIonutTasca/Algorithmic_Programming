"""
Test module for the sorting algorithm implementations.
"""

from src.algorithms.sort import quick_sort, merge_sort
from src.tests.test_search import Part
import random
import time

def test_sort_algorithms_with_integers():
    """
    Test the sorting algorithms with a list of integers.
    """
    # Create an unsorted list of integers
    numbers = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 6, 8]
    print("Original list:", numbers)
    
    # Test quicksort
    print("\nTesting QuickSort with integers:")
    result = quick_sort(numbers)
    print("Sorted list:", result.sorted_items)
    print(f"QuickSort execution time: {result.execution_time:.10f} seconds")
    
    # Test mergesort
    print("\nTesting MergeSort with integers:")
    result = merge_sort(numbers)
    print("Sorted list:", result.sorted_items)
    print(f"MergeSort execution time: {result.execution_time:.10f} seconds")


def test_sort_algorithms_with_parts():
    """
    Test the sorting algorithms with a list of Part objects.
    """
    # Create a list of car parts
    parts = [
        Part(1007, "Alternator", "Electrical", 120.99),
        Part(1002, "Air Filter", "Filters", 15.99),
        Part(1006, "Battery", "Electrical", 89.99),
        Part(1003, "Brake Pads", "Brakes", 45.99),
        Part(1001, "Oil Filter", "Filters", 12.99),
        Part(1008, "Radiator", "Cooling", 75.99),
        Part(1004, "Spark Plugs", "Ignition", 8.99),
        Part(1009, "Timing Belt", "Engine", 28.99),
        Part(1010, "Water Pump", "Cooling", 35.99),
        Part(1005, "Wiper Blades", "Exterior", 22.99)
    ]
    
    # Define key functions
    id_key = lambda part: part.part_id
    name_key = lambda part: part.name
    price_key = lambda part: part.price
    
    print("\nOriginal part list:")
    for part in parts:
        print(f"- {part}")
    
    # Test sorting by ID
    print("\nSorting parts by ID:")
    result = quick_sort(parts, id_key)
    print("\nQuickSort result:")
    for part in result.sorted_items:
        print(f"- {part}")
    print(f"QuickSort execution time: {result.execution_time:.10f} seconds")
    
    # Test sorting by name
    print("\nSorting parts by Name:")
    result = merge_sort(parts, name_key)
    print("\nMergeSort result:")
    for part in result.sorted_items:
        print(f"- {part}")
    print(f"MergeSort execution time: {result.execution_time:.10f} seconds")
    
    # Test sorting by price
    print("\nSorting parts by Price:")
    result = quick_sort(parts, price_key)
    print("\nQuickSort result:")
    for part in result.sorted_items:
        print(f"- {part}")
    print(f"QuickSort execution time: {result.execution_time:.10f} seconds")


def compare_sort_performance():
    """
    Compare the performance of QuickSort and MergeSort with different data sizes.
    """
    def create_random_list(size):
        return [random.randint(1, 10000) for _ in range(size)]
    
    def test_with_size(size):
        data = create_random_list(size)
        
        # QuickSort
        start = time.time()
        quick_result = quick_sort(data)
        quick_time = quick_result.execution_time
        
        # MergeSort
        start = time.time()
        merge_result = merge_sort(data)
        merge_time = merge_result.execution_time
        
        return quick_time, merge_time
    
    # Test with different sizes
    sizes = [100, 1000, 10000]
    print("\nComparing sorting algorithm performance:")
    
    for size in sizes:
        quick_time, merge_time = test_with_size(size)
        print(f"\nSize: {size} elements")
        print(f"QuickSort time: {quick_time:.6f} seconds")
        print(f"MergeSort time: {merge_time:.6f} seconds")
        
    # Test with sorted data
    print("\nTesting with already sorted data (10,000 elements):")
    sorted_data = list(range(10000))
    
    # QuickSort
    quick_result = quick_sort(sorted_data)
    quick_time = quick_result.execution_time
    
    # MergeSort
    merge_result = merge_sort(sorted_data)
    merge_time = merge_result.execution_time
    
    print(f"QuickSort time: {quick_time:.6f} seconds")
    print(f"MergeSort time: {merge_time:.6f} seconds")
    
    # Test with reverse sorted data
    print("\nTesting with reverse sorted data (10,000 elements):")
    reverse_data = list(range(10000, 0, -1))
    
    # QuickSort
    quick_result = quick_sort(reverse_data)
    quick_time = quick_result.execution_time
    
    # MergeSort
    merge_result = merge_sort(reverse_data)
    merge_time = merge_result.execution_time
    
    print(f"QuickSort time: {quick_time:.6f} seconds")
    print(f"MergeSort time: {merge_time:.6f} seconds")


if __name__ == "__main__":
    test_sort_algorithms_with_integers()
    test_sort_algorithms_with_parts()
    compare_sort_performance()
