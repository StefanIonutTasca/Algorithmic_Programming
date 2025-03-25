"""
Test module for the search algorithm implementations.
"""

from src.algorithms.search import linear_search, binary_search
from src.datastructures.array_list import ArrayList
import time

class Part:
    """
    A simple car part class for testing the search algorithms.
    """
    
    def __init__(self, part_id: int, name: str, category: str, price: float):
        """
        Initialize a Part with the given attributes.
        
        Args:
            part_id: The unique ID of the part
            name: The name of the part
            category: The category of the part
            price: The price of the part
        """
        self.part_id = part_id
        self.name = name
        self.category = category
        self.price = price
    
    def __str__(self) -> str:
        """
        Return a string representation of the Part.
        
        Returns:
            A string representation of the Part
        """
        return f"{self.name} (ID: {self.part_id}, Category: {self.category}, Price: ${self.price:.2f})"
    
    def __eq__(self, other):
        """
        Check if the Part is equal to another Part.
        
        Args:
            other: The other Part to compare to
            
        Returns:
            True if the Parts are equal, False otherwise
        """
        if not isinstance(other, Part):
            return False
        return self.part_id == other.part_id


def test_search_algorithms_with_integers():
    """
    Test the search algorithms with a list of integers.
    """
    # Create a list of integers
    numbers = [10, 25, 35, 45, 55, 65, 75, 85, 95]
    
    # Test linear search
    print("Testing Linear Search with integers:")
    target = 55
    result = linear_search(numbers, target)
    
    if result.found:
        print(f"Found {target} at index {result.index}")
    else:
        print(f"{target} not found")
    
    print(f"Linear Search execution time: {result.execution_time:.10f} seconds")
    
    # Test binary search
    print("\nTesting Binary Search with integers:")
    result = binary_search(numbers, target)
    
    if result.found:
        print(f"Found {target} at index {result.index}")
    else:
        print(f"{target} not found")
    
    print(f"Binary Search execution time: {result.execution_time:.10f} seconds")
    
    # Test with target not in the list
    print("\nTesting with target not in the list:")
    target = 30
    
    result = linear_search(numbers, target)
    print(f"Linear Search: {target} {'found' if result.found else 'not found'} in {result.execution_time:.10f} seconds")
    
    result = binary_search(numbers, target)
    print(f"Binary Search: {target} {'found' if result.found else 'not found'} in {result.execution_time:.10f} seconds")


def test_search_algorithms_with_parts():
    """
    Test the search algorithms with a list of Part objects.
    """
    # Create a list of car parts
    parts = [
        Part(1001, "Oil Filter", "Filters", 12.99),
        Part(1002, "Air Filter", "Filters", 15.99),
        Part(1003, "Brake Pads", "Brakes", 45.99),
        Part(1004, "Spark Plugs", "Ignition", 8.99),
        Part(1005, "Wiper Blades", "Exterior", 22.99),
        Part(1006, "Battery", "Electrical", 89.99),
        Part(1007, "Alternator", "Electrical", 120.99),
        Part(1008, "Radiator", "Cooling", 75.99),
        Part(1009, "Timing Belt", "Engine", 28.99),
        Part(1010, "Water Pump", "Cooling", 35.99)
    ]
    
    # Sort parts by ID for binary search
    sorted_parts = sorted(parts, key=lambda part: part.part_id)
    
    # Test linear search
    print("\nTesting Linear Search with Part objects:")
    target_part = Part(1005, "", "", 0)  # Only part_id matters for equality
    
    result = linear_search(parts, target_part)
    
    if result.found:
        print(f"Found part: {parts[result.index]}")
    else:
        print("Part not found")
    
    print(f"Linear Search execution time: {result.execution_time:.10f} seconds")
    
    # Test binary search
    print("\nTesting Binary Search with Part objects:")
    
    # Define a key function for the binary search
    key_function = lambda part: part.part_id
    
    result = binary_search(sorted_parts, target_part, key_function)
    
    if result.found:
        print(f"Found part: {sorted_parts[result.index]}")
    else:
        print("Part not found")
    
    print(f"Binary Search execution time: {result.execution_time:.10f} seconds")
    
    # Test with target not in the list
    print("\nTesting with part not in the list:")
    target_part = Part(1020, "", "", 0)  # Non-existent part ID
    
    result = linear_search(parts, target_part)
    print(f"Linear Search: Part ID {target_part.part_id} {'found' if result.found else 'not found'} in {result.execution_time:.10f} seconds")
    
    result = binary_search(sorted_parts, target_part, key_function)
    print(f"Binary Search: Part ID {target_part.part_id} {'found' if result.found else 'not found'} in {result.execution_time:.10f} seconds")


def compare_search_performance():
    """
    Compare the performance of linear search and binary search with a large dataset.
    """
    # Create a large dataset
    data_size = 100000
    large_dataset = [i for i in range(data_size)]
    
    print(f"\nComparing search performance with {data_size} elements:")
    
    # Test with a target in the beginning
    target = 10
    print(f"\nTarget {target} (near beginning):")
    
    result = linear_search(large_dataset, target)
    print(f"Linear Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    result = binary_search(large_dataset, target)
    print(f"Binary Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    # Test with a target in the middle
    target = data_size // 2
    print(f"\nTarget {target} (middle):")
    
    result = linear_search(large_dataset, target)
    print(f"Linear Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    result = binary_search(large_dataset, target)
    print(f"Binary Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    # Test with a target at the end
    target = data_size - 10
    print(f"\nTarget {target} (near end):")
    
    result = linear_search(large_dataset, target)
    print(f"Linear Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    result = binary_search(large_dataset, target)
    print(f"Binary Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    # Test with a target not in the list
    target = data_size + 100
    print(f"\nTarget {target} (not in list):")
    
    result = linear_search(large_dataset, target)
    print(f"Linear Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")
    
    result = binary_search(large_dataset, target)
    print(f"Binary Search: {'found' if result.found else 'not found'} in {result.execution_time:.6f} seconds")


if __name__ == "__main__":
    test_search_algorithms_with_integers()
    test_search_algorithms_with_parts()
    compare_search_performance()
