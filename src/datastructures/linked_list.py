"""
Custom LinkedList implementation for the Automotive Parts Catalog System.
This data structure provides a doubly linked list with generics.
"""
from typing import TypeVar, Generic, Optional, Iterator, Any, Callable, List

T = TypeVar('T')  # Generic type for the LinkedList

class Node(Generic[T]):
    """
    A node in a doubly linked list.
    """
    
    def __init__(self, data: T):
        """
        Initialize a Node with the given data.
        
        Args:
            data: The data to store in the Node
        """
        self.data: T = data
        self.next: Optional[Node[T]] = None
        self.prev: Optional[Node[T]] = None

class LinkedList(Generic[T]):
    """
    A generic implementation of a doubly linked list data structure.
    
    This class implements a doubly linked list that can store elements of any type.
    It provides methods for adding, removing, and accessing elements, as well as
    various utility methods for searching and manipulation.
    """
    
    def __init__(self):
        """
        Initialize an empty LinkedList.
        """
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._size: int = 0
    
    def __len__(self) -> int:
        """
        Return the number of elements in the LinkedList.
        
        Returns:
            The number of elements in the LinkedList
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
        
        return self._get_node(index).data
    
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
        
        self._get_node(index).data = value
    
    def __contains__(self, item: Any) -> bool:
        """
        Check if the LinkedList contains the specified item.
        
        Args:
            item: The item to check for
            
        Returns:
            True if the item is in the LinkedList, False otherwise
        """
        current = self._head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False
    
    def __iter__(self) -> Iterator[T]:
        """
        Return an iterator over the elements in the LinkedList.
        
        Returns:
            An iterator over the elements
        """
        current = self._head
        while current:
            yield current.data
            current = current.next
    
    def __str__(self) -> str:
        """
        Return a string representation of the LinkedList.
        
        Returns:
            A string representation of the LinkedList
        """
        if self._size == 0:
            return "[]"
        
        result = "["
        current = self._head
        
        while current.next:
            result += f"{current.data}, "
            current = current.next
        
        result += f"{current.data}]"
        return result
    
    def append(self, item: T) -> None:
        """
        Add an item to the end of the LinkedList.
        
        Args:
            item: The item to add
        """
        new_node = Node(item)
        
        if self._head is None:
            # First element
            self._head = new_node
            self._tail = new_node
        else:
            # Add to the end
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        
        self._size += 1
    
    def prepend(self, item: T) -> None:
        """
        Add an item to the start of the LinkedList.
        
        Args:
            item: The item to add
        """
        new_node = Node(item)
        
        if self._head is None:
            # First element
            self._head = new_node
            self._tail = new_node
        else:
            # Add to the beginning
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        
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
        
        if index == 0:
            self.prepend(item)
        elif index == self._size:
            self.append(item)
        else:
            # Find the node at the specified index
            current = self._get_node(index)
            
            # Create the new node
            new_node = Node(item)
            
            # Insert the new node before the current node
            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node
            
            self._size += 1
    
    def remove(self, item: T) -> bool:
        """
        Remove the first occurrence of the specified item from the LinkedList.
        
        Args:
            item: The item to remove
            
        Returns:
            True if the item was found and removed, False otherwise
        """
        current = self._head
        
        while current:
            if current.data == item:
                self._remove_node(current)
                return True
            current = current.next
        
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
        
        node = self._get_node(index)
        self._remove_node(node)
        return node.data
    
    def clear(self) -> None:
        """
        Remove all elements from the LinkedList.
        """
        self._head = None
        self._tail = None
        self._size = 0
    
    def index_of(self, item: T) -> int:
        """
        Find the index of the first occurrence of the specified item.
        
        Args:
            item: The item to find
            
        Returns:
            The index of the item, or -1 if not found
        """
        current = self._head
        index = 0
        
        while current:
            if current.data == item:
                return index
            current = current.next
            index += 1
        
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
        
        node = self._get_node(index)
        old_value = node.data
        node.data = item
        return old_value
    
    def is_empty(self) -> bool:
        """
        Check if the LinkedList is empty.
        
        Returns:
            True if the LinkedList is empty, False otherwise
        """
        return self._size == 0
    
    def _get_node(self, index: int) -> Node[T]:
        """
        Get the Node at the specified index.
        
        Args:
            index: The index of the Node to retrieve
            
        Returns:
            The Node at the specified index
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        
        # Optimize for faster access by approaching from the appropriate end
        if index <= self._size // 2:
            # Approach from the head
            current = self._head
            for _ in range(index):
                current = current.next
        else:
            # Approach from the tail
            current = self._tail
            for _ in range(self._size - 1 - index):
                current = current.prev
        
        return current
    
    def _remove_node(self, node: Node[T]) -> None:
        """
        Remove the specified Node from the LinkedList.
        
        Args:
            node: The Node to remove
        """
        # Handle removing the only node
        if self._size == 1:
            self._head = None
            self._tail = None
        
        # Handle removing the head
        elif node is self._head:
            self._head = node.next
            self._head.prev = None
        
        # Handle removing the tail
        elif node is self._tail:
            self._tail = node.prev
            self._tail.next = None
        
        # Handle removing a middle node
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        
        self._size -= 1
    
    def to_list(self) -> List[T]:
        """
        Convert the LinkedList to a Python list.
        
        Returns:
            A Python list containing all elements in the LinkedList
        """
        result = []
        current = self._head
        
        while current:
            result.append(current.data)
            current = current.next
        
        return result
    
    def from_list(self, items: List[T]) -> None:
        """
        Initialize the LinkedList from a Python list.
        
        Args:
            items: The list of items to add
        """
        self.clear()
        for item in items:
            self.append(item)
