"""
Custom ArrayList implementation for the Automotive Parts Catalog System.
This data structure provides dynamic array functionality with generics.
"""
from typing import TypeVar, Generic, List, Optional, Callable, Any

T = TypeVar('T')  # Generic type for the ArrayList

class ArrayList(Generic[T]):
    """
    A generic implementation of an ArrayList data structure.
    
    This class implements a resizable array that can store elements of any type.
    It provides methods for adding, removing, and accessing elements, as well as
    various utility methods for searching and manipulation.
    """
    
    def __init__(self, initial_capacity: int = 10):
        """
        Initialize an empty ArrayList with the specified initial capacity.
        
        Args:
            initial_capacity: The initial size of the underlying array
        """
        self._data: List[Optional[T]] = [None] * initial_capacity
        self._size: int = 0
        self._capacity: int = initial_capacity
    
    def __len__(self) -> int:
        """
        Return the number of elements in the ArrayList.
        
        Returns:
            The number of elements in the ArrayList
        """
        return self._size
    
    def __getitem__(self, index: int) -> T:
        """
        Get the element at the specified index.
        
        Args:
            index: The index of the element to retrieve
            
        Returns:
            The element at the specified index
            
        Raises:
            IndexError: If the index is out of bounds
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        return self._data[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """
        Set the element at the specified index to the given value.
        
        Args:
            index: The index of the element to set
            value: The value to set
            
        Raises:
            IndexError: If the index is out of bounds
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        self._data[index] = value
    
    def __contains__(self, item: Any) -> bool:
        """
        Check if the ArrayList contains the specified item.
        
        Args:
            item: The item to check for
            
        Returns:
            True if the item is in the ArrayList, False otherwise
        """
        for i in range(self._size):
            if self._data[i] == item:
                return True
        return False
    
    def __iter__(self):
        """
        Return an iterator over the elements in the ArrayList.
        
        Returns:
            An iterator over the elements
        """
        for i in range(self._size):
            yield self._data[i]
    
    def __str__(self) -> str:
        """
        Return a string representation of the ArrayList.
        
        Returns:
            A string representation of the ArrayList
        """
        if self._size == 0:
            return "[]"
        result = "["
        for i in range(self._size - 1):
            result += f"{self._data[i]}, "
        result += f"{self._data[self._size - 1]}]"
        return result
    
    def append(self, item: T) -> None:
        """
        Add an item to the end of the ArrayList.
        
        Args:
            item: The item to add
        """
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = item
        self._size += 1
    
    def insert(self, index: int, item: T) -> None:
        """
        Insert an item at the specified index.
        
        Args:
            index: The index at which to insert the item
            item: The item to insert
            
        Raises:
            IndexError: If the index is out of bounds
        """
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        
        # Shift elements to make room for the new item
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        
        self._data[index] = item
        self._size += 1
    
    def remove(self, item: T) -> bool:
        """
        Remove the first occurrence of the specified item from the ArrayList.
        
        Args:
            item: The item to remove
            
        Returns:
            True if the item was found and removed, False otherwise
        """
        for i in range(self._size):
            if self._data[i] == item:
                self.remove_at(i)
                return True
        return False
    
    def remove_at(self, index: int) -> T:
        """
        Remove and return the item at the specified index.
        
        Args:
            index: The index of the item to remove
            
        Returns:
            The removed item
            
        Raises:
            IndexError: If the index is out of bounds
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        
        item = self._data[index]
        
        # Shift elements to fill the gap
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        
        self._data[self._size - 1] = None
        self._size -= 1
        
        # Shrink the array if it's less than 1/4 full
        if self._size > 0 and self._size < self._capacity // 4:
            self._resize(self._capacity // 2)
        
        return item
    
    def clear(self) -> None:
        """
        Remove all elements from the ArrayList.
        """
        self._data = [None] * self._capacity
        self._size = 0
    
    def index_of(self, item: T) -> int:
        """
        Find the index of the first occurrence of the specified item.
        
        Args:
            item: The item to find
            
        Returns:
            The index of the item, or -1 if not found
        """
        for i in range(self._size):
            if self._data[i] == item:
                return i
        return -1
    
    def get(self, index: int) -> T:
        """
        Get the element at the specified index.
        
        Args:
            index: The index of the element to retrieve
            
        Returns:
            The element at the specified index
            
        Raises:
            IndexError: If the index is out of bounds
        """
        return self[index]
    
    def set(self, index: int, item: T) -> T:
        """
        Replace the element at the specified index with the given value.
        
        Args:
            index: The index of the element to replace
            item: The new value
            
        Returns:
            The previous value at the index
            
        Raises:
            IndexError: If the index is out of bounds
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        
        old_value = self._data[index]
        self._data[index] = item
        return old_value
    
    def is_empty(self) -> bool:
        """
        Check if the ArrayList is empty.
        
        Returns:
            True if the ArrayList is empty, False otherwise
        """
        return self._size == 0
    
    def _resize(self, new_capacity: int) -> None:
        """
        Resize the underlying array to the specified new capacity.
        
        Args:
            new_capacity: The new capacity for the array
        """
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
    
    def sort(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> None:
        """
        Sort the elements in the ArrayList.
        
        Args:
            key: A function that extracts a comparison key from each element
            reverse: If True, sort in descending order
        """
        # Create a temporary list with actual elements (no None values)
        temp = [self._data[i] for i in range(self._size)]
        # Sort the temporary list
        temp.sort(key=key, reverse=reverse)
        # Copy the sorted elements back to the ArrayList
        for i in range(self._size):
            self._data[i] = temp[i]
