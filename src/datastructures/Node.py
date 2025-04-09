#!/usr/bin/env python3
"""
Node class for Binary Search Tree implementation
Date: March 15, 2025
"""


class Node:
    """
    Node class for the Binary Search Tree
    Each node contains data and references to left and right children
    """

    def __init__(self, data):
        """
        Initialize a node with data and None for left and right children
        
        Args:
            data: The data to store in the node
        """
        self.data = data
        self.left = None
        self.right = None
        
    def __str__(self):
        """
        String representation of the node
        
        Returns:
            str: String representation of the node's data
        """
        return str(self.data)
    
    def is_leaf(self):
        """
        Check if the node is a leaf node (has no children)
        
        Returns:
            bool: True if the node is a leaf, False otherwise
        """
        return self.left is None and self.right is None
