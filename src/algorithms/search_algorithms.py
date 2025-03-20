"""
Search algorithm implementations for the Automotive Parts Catalog System.
This module provides linear and binary search algorithms with performance tracking.
"""
from typing import TypeVar, List, Callable, Optional, Tuple, Any
import time

T = TypeVar('T')  # Generic type for the elements

class SearchAlgorithms:
    """
    A collection of search algorithms with performance tracking.
    
    This class implements various search algorithms and provides methods
    to measure and compare their performance.
    """
    
    @staticmethod
    def linear_search(data: List[T], target: T) -> Tuple[int, float]:
        """
        Perform a linear search on the given data.
        
        Args:
            data: The list of elements to search through
            target: The element to search for
            
        Returns:
            A tuple containing:
                - The index of the target element, or -1 if not found
                - The execution time in seconds
        """
        start_time = time.time()
        
        for i in range(len(data)):
            if data[i] == target:
                end_time = time.time()
                return i, end_time - start_time
        
        end_time = time.time()
        return -1, end_time - start_time
    
    @staticmethod
    def linear_search_by_key(data: List[T], key_func: Callable[[T], Any], target_key: Any) -> Tuple[Optional[T], float]:
        """
        Perform a linear search using a key extraction function.
        
        Args:
            data: The list of elements to search through
            key_func: A function that extracts the key from an element
            target_key: The key to search for
            
        Returns:
            A tuple containing:
                - The found element, or None if not found
                - The execution time in seconds
        """
        start_time = time.time()
        
        for item in data:
            if key_func(item) == target_key:
                end_time = time.time()
                return item, end_time - start_time
        
        end_time = time.time()
        return None, end_time - start_time
    
    @staticmethod
    def binary_search(data: List[T], target: T, comparator: Optional[Callable[[T, T], int]] = None) -> Tuple[int, float]:
        """
        Perform a binary search on the given sorted data.
        
        Args:
            data: The sorted list of elements to search through
            target: The element to search for
            comparator: An optional function that compares two elements and returns:
                        negative if first < second,
                        zero if first == second,
                        positive if first > second
            
        Returns:
            A tuple containing:
                - The index of the target element, or -1 if not found
                - The execution time in seconds
        """
        start_time = time.time()
        
        def default_comparator(a: T, b: T) -> int:
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return 0
        
        comp = comparator or default_comparator
        
        low = 0
        high = len(data) - 1
        
        while low <= high:
            mid = (low + high) // 2
            comparison = comp(data[mid], target)
            
            if comparison == 0:
                end_time = time.time()
                return mid, end_time - start_time
            elif comparison < 0:
                low = mid + 1
            else:
                high = mid - 1
        
        end_time = time.time()
        return -1, end_time - start_time
    
    @staticmethod
    def binary_search_by_key(data: List[T], key_func: Callable[[T], Any], target_key: Any) -> Tuple[Optional[T], float]:
        """
        Perform a binary search using a key extraction function on sorted data.
        
        The data must be sorted according to the keys extracted by key_func.
        
        Args:
            data: The sorted list of elements to search through
            key_func: A function that extracts the key from an element
            target_key: The key to search for
            
        Returns:
            A tuple containing:
                - The found element, or None if not found
                - The execution time in seconds
        """
        start_time = time.time()
        
        low = 0
        high = len(data) - 1
        
        while low <= high:
            mid = (low + high) // 2
            current_key = key_func(data[mid])
            
            if current_key == target_key:
                end_time = time.time()
                return data[mid], end_time - start_time
            elif current_key < target_key:
                low = mid + 1
            else:
                high = mid - 1
        
        end_time = time.time()
        return None, end_time - start_time
    
    @staticmethod
    def compare_search_algorithms(data: List[T], target: T) -> dict:
        """
        Compare the performance of different search algorithms.
        
        Args:
            data: The list of elements to search through
            target: The element to search for
            
        Returns:
            A dictionary with algorithm names as keys and tuples of (found_index, execution_time) as values
        """
        # Make a copy of the data and sort it for binary search
        sorted_data = sorted(data)
        
        # Find the target in the sorted list for binary search
        target_in_sorted = target
        for item in sorted_data:
            if item == target:
                target_in_sorted = item
                break
        
        results = {}
        
        # Run linear search
        index_linear, time_linear = SearchAlgorithms.linear_search(data, target)
        results["Linear Search"] = (index_linear, time_linear)
        
        # Run binary search
        index_binary, time_binary = SearchAlgorithms.binary_search(sorted_data, target_in_sorted)
        results["Binary Search"] = (index_binary, time_binary)
        
        return results
