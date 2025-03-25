"""
Search algorithm implementations for the Automotive Parts Catalog System.
"""
from typing import TypeVar, Generic, List, Optional, Callable, Any
import time

T = TypeVar('T')  # Generic type for the search algorithms
K = TypeVar('K')  # Generic type for keys

class SearchResult:
    """
    Class to hold the result of a search operation, including the execution time.
    """
    
    def __init__(self, found: bool, index: int, execution_time: float):
        """
        Initialize a SearchResult.
        
        Args:
            found: Whether the item was found
            index: The index of the item if found, -1 otherwise
            execution_time: The time taken to execute the search in seconds
        """
        self.found = found
        self.index = index
        self.execution_time = execution_time

def linear_search(items: List[T], target: T, key_function: Optional[Callable[[T], Any]] = None) -> SearchResult:
    """
    Perform a linear search on the given list for the target.
    
    Args:
        items: The list to search
        target: The item to search for
        key_function: Optional function to extract a comparison key from each element
    
    Returns:
        A SearchResult containing the search results and execution time
    """
    start_time = time.time()
    
    if key_function is None:
        # Search by direct comparison
        for i, item in enumerate(items):
            if item == target:
                end_time = time.time()
                return SearchResult(True, i, end_time - start_time)
    else:
        # Search by key comparison
        target_key = key_function(target)
        for i, item in enumerate(items):
            if key_function(item) == target_key:
                end_time = time.time()
                return SearchResult(True, i, end_time - start_time)
    
    end_time = time.time()
    return SearchResult(False, -1, end_time - start_time)

def binary_search(items: List[T], target: T, key_function: Optional[Callable[[T], Any]] = None) -> SearchResult:
    """
    Perform a binary search on the given sorted list for the target.
    
    Args:
        items: The sorted list to search
        target: The item to search for
        key_function: Optional function to extract a comparison key from each element
    
    Returns:
        A SearchResult containing the search results and execution time
    """
    start_time = time.time()
    
    if key_function is None:
        # Use the item itself as the key
        key_function = lambda x: x
    
    target_key = key_function(target)
    
    left = 0
    right = len(items) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_key = key_function(items[mid])
        
        if mid_key == target_key:
            end_time = time.time()
            return SearchResult(True, mid, end_time - start_time)
        elif mid_key < target_key:
            left = mid + 1
        else:
            right = mid - 1
    
    end_time = time.time()
    return SearchResult(False, -1, end_time - start_time)
