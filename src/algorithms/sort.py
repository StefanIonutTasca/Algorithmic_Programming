"""
Sorting algorithm implementations for the Automotive Parts Catalog System.
"""
from typing import TypeVar, List, Optional, Callable, Any
import time
import copy

T = TypeVar('T')  # Generic type for the sorting algorithms

class SortResult:
    """
    Class to hold the result of a sort operation, including the execution time.
    """
    
    def __init__(self, sorted_items: List[T], execution_time: float):
        """
        Initialize a SortResult.
        
        Args:
            sorted_items: The sorted list
            execution_time: The time taken to execute the sort in seconds
        """
        self.sorted_items = sorted_items
        self.execution_time = execution_time

def quick_sort(items: List[T], key_function: Optional[Callable[[T], Any]] = None) -> SortResult:
    """
    Sort the given list using the QuickSort algorithm.
    
    Args:
        items: The list to sort
        key_function: Optional function to extract a comparison key from each element
    
    Returns:
        A SortResult containing the sorted list and execution time
    """
    start_time = time.time()
    
    # Create a copy of the list to avoid modifying the original
    items_copy = copy.deepcopy(items)
    
    if not items_copy:
        end_time = time.time()
        return SortResult(items_copy, end_time - start_time)
    
    if key_function is None:
        # Use the item itself as the key
        key_function = lambda x: x
    
    def _quick_sort(arr: List[T], low: int, high: int) -> None:
        if low < high:
            # Partition the array and get the partition index
            partition_index = _partition(arr, low, high)
            
            # Sort the elements before and after the partition index
            _quick_sort(arr, low, partition_index - 1)
            _quick_sort(arr, partition_index + 1, high)
    
    def _partition(arr: List[T], low: int, high: int) -> int:
        # Choose the rightmost element as the pivot
        pivot_key = key_function(arr[high])
        
        # Index of the smaller element
        i = low - 1
        
        for j in range(low, high):
            # If the current element is smaller than or equal to the pivot
            if key_function(arr[j]) <= pivot_key:
                # Increment the index of the smaller element
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Swap the pivot element with the element at (i + 1)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        
        # Return the partition index
        return i + 1
    
    _quick_sort(items_copy, 0, len(items_copy) - 1)
    
    end_time = time.time()
    return SortResult(items_copy, end_time - start_time)

def merge_sort(items: List[T], key_function: Optional[Callable[[T], Any]] = None) -> SortResult:
    """
    Sort the given list using the MergeSort algorithm.
    
    Args:
        items: The list to sort
        key_function: Optional function to extract a comparison key from each element
    
    Returns:
        A SortResult containing the sorted list and execution time
    """
    start_time = time.time()
    
    # Create a copy of the list to avoid modifying the original
    items_copy = copy.deepcopy(items)
    
    if not items_copy:
        end_time = time.time()
        return SortResult(items_copy, end_time - start_time)
    
    if key_function is None:
        # Use the item itself as the key
        key_function = lambda x: x
    
    def _merge_sort(arr: List[T]) -> List[T]:
        if len(arr) <= 1:
            return arr
        
        # Divide the array into two halves
        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        
        # Merge the two halves
        return _merge(left, right)
    
    def _merge(left: List[T], right: List[T]) -> List[T]:
        result = []
        i = j = 0
        
        # Merge the two arrays in sorted order
        while i < len(left) and j < len(right):
            if key_function(left[i]) <= key_function(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add any remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    items_copy = _merge_sort(items_copy)
    
    end_time = time.time()
    return SortResult(items_copy, end_time - start_time)
