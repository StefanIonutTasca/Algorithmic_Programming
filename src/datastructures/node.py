#!/usr/bin/env python3
"""
Node class for Binary Search Tree implementation
Date: March 15, 2025
"""
from typing import TypeVar, Generic, Optional

T = TypeVar('T')  # Generic type for node data


class Node(Generic[T]):
    """
    Node class for the Binary Search Tree
    Each node contains data and references to left and right children
    """

    def __init__(self, data: T):
        """
        Initialize a node with data and None for left and right children
        
        Args:
            data: The data to store in the node
        """
        self.data: T = data
        self.left: Optional[Node[T]] = None
        self.right: Optional[Node[T]] = None
        
    def __str__(self) -> str:
        """
        String representation of the node
        
        Returns:
            str: String representation of the node's data
        """
        return str(self.data)
    
    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf node (has no children)
        
        Returns:
            bool: True if the node is a leaf, False otherwise
        """
        return self.left is None and self.right is None
