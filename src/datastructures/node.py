#!/usr/bin/env python3
"""
Node implementation for tree-based data structures in the Automotive Parts Catalog System.
This class represents a node in a binary tree with generic data.
"""
from typing import TypeVar, Generic, Optional, Any

T = TypeVar('T')  # Generic type for node data

class Node(Generic[T]):
    """
    A generic node implementation for tree-based data structures.
    
    This class implements a node that can store data of any type and
    references to left and right child nodes.
    """
    
    def __init__(self, data: T):
        """
        Initialize a node with the specified data.

        Args:
            data: The data to store in the node
        """
        self._data: T = data
        self._left: Optional['Node[T]'] = None
        self._right: Optional['Node[T]'] = None
    
    def get_data(self) -> T:
        """
        Get the data stored in the node.

        Returns:
            The data stored in the node
        """
        return self._data
    
    def set_data(self, data: T) -> None:
        """
        Set the data stored in the node.
        
        Args:
            data: The new data to store
        """
        self._data = data
    
    def get_left(self) -> Optional['Node[T]']:
        """
        Get the left child of the node.
        
        Returns:
            The left child node, or None if no left child exists
        """
        return self._left
    
    def set_left(self, left: Optional['Node[T]']) -> None:
        """
        Set the left child of the node.
        
        Args:
            left: The new left child node
        """
        self._left = left
    
    def get_right(self) -> Optional['Node[T]']:
        """
        Get the right child of the node.
        
        Returns:
            The right child node, or None if no right child exists
        """
        return self._right
    
    def set_right(self, right: Optional['Node[T]']) -> None:
        """
        Set the right child of the node.
        
        Args:
            right: The new right child node
        """
        self._right = right
    
    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf (has no children).

        Returns:
            True if the node is a leaf, False otherwise
        """
        return self._left is None and self._right is None

    def __str__(self) -> str:
        """
        Return a string representation of the node.

        Returns:
            A string representation of the node
        """
        return f"Node({self._data})"
