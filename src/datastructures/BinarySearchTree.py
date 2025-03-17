#!/usr/bin/env python3
"""
Binary Search Tree implementation
Date: March 17, 2025
"""

from .Node import Node
import time

class BinarySearchTree:
    """
    Binary Search Tree implementation
    Supports insertion, deletion, search, and traversal operations
    """

    def __init__(self, comparator=None):
        """
        Initialize an empty binary search tree
        
        Args:
            comparator: Optional custom comparison function for the data
        """
        self.root = None
        self.size = 0
        # Use custom comparator if provided, otherwise use default comparison
        self.comparator = comparator if comparator else lambda x, y: (x > y) - (x < y)
        
    def __len__(self):
        """
        Get the number of nodes in the tree
        
        Returns:
            int: The number of nodes
        """
        return self.size
    
    def insert(self, data):
        """
        Insert data into the binary search tree
        
        Args:
            data: The data to insert
            
        Returns:
            bool: True if insertion was successful, False if data already exists
        """
        # Start performance measurement
        start_time = time.time()
        
        if self.root is None:
            self.root = Node(data)
            self.size += 1
            return True, time.time() - start_time
        
        return self._insert_recursive(self.root, data, start_time)
    
    def _insert_recursive(self, current, data, start_time):
        """
        Helper method to recursively insert data into the tree
        
        Args:
            current: The current node being examined
            data: The data to insert
            start_time: Time when the insert operation started
            
        Returns:
            bool: True if insertion was successful, False if data already exists
            float: Time taken for the operation
        """
        # Compare the data
        comparison = self.comparator(data, current.data)
        
        # Equal - data already exists
        if comparison == 0:
            return False, time.time() - start_time
        
        # Less than - go left
        elif comparison < 0:
            if current.left is None:
                current.left = Node(data)
                self.size += 1
                return True, time.time() - start_time
            return self._insert_recursive(current.left, data, start_time)
        
        # Greater than - go right
        else:
            if current.right is None:
                current.right = Node(data)
                self.size += 1
                return True, time.time() - start_time
            return self._insert_recursive(current.right, data, start_time)
    
    def search(self, data):
        """
        Search for data in the binary search tree
        
        Args:
            data: The data to search for
            
        Returns:
            bool: True if data is found, False otherwise
            float: Time taken for the operation
        """
        # Start performance measurement
        start_time = time.time()
        
        if self.root is None:
            return False, time.time() - start_time
        
        return self._search_recursive(self.root, data, start_time)
    
    def _search_recursive(self, current, data, start_time):
        """
        Helper method to recursively search for data in the tree
        
        Args:
            current: The current node being examined
            data: The data to search for
            start_time: Time when the search operation started
            
        Returns:
            bool: True if data is found, False otherwise
            float: Time taken for the operation
        """
        if current is None:
            return False, time.time() - start_time
        
        # Compare the data
        comparison = self.comparator(data, current.data)
        
        # Equal - found the data
        if comparison == 0:
            return True, time.time() - start_time
        
        # Less than - go left
        elif comparison < 0:
            return self._search_recursive(current.left, data, start_time)
        
        # Greater than - go right
        else:
            return self._search_recursive(current.right, data, start_time)
    
    def delete(self, data):
        """
        Delete data from the binary search tree
        
        Args:
            data: The data to delete
            
        Returns:
            bool: True if deletion was successful, False if data not found
            float: Time taken for the operation
        """
        # Start performance measurement
        start_time = time.time()
        
        if self.root is None:
            return False, time.time() - start_time
        
        result, self.root, duration = self._delete_recursive(self.root, data, start_time)
        if result:
            self.size -= 1
        return result, duration
    
    def _delete_recursive(self, current, data, start_time):
        """
        Helper method to recursively delete data from the tree
        
        Args:
            current: The current node being examined
            data: The data to delete
            start_time: Time when the delete operation started
            
        Returns:
            bool: True if deletion was successful, False if data not found
            Node: The new current node after deletion
            float: Time taken for the operation
        """
        if current is None:
            return False, None, time.time() - start_time
        
        # Compare the data
        comparison = self.comparator(data, current.data)
        
        # Less than - go left
        if comparison < 0:
            result, current.left, duration = self._delete_recursive(current.left, data, start_time)
            return result, current, duration
        
        # Greater than - go right
        elif comparison > 0:
            result, current.right, duration = self._delete_recursive(current.right, data, start_time)
            return result, current, duration
        
        # Equal - found the node to delete
        else:
            # Case 1: Leaf node (no children)
            if current.is_leaf():
                return True, None, time.time() - start_time
            
            # Case 2: Only one child
            elif current.left is None:
                return True, current.right, time.time() - start_time
            elif current.right is None:
                return True, current.left, time.time() - start_time
            
            # Case 3: Two children
            else:
                # Find inorder successor (smallest node in right subtree)
                successor = self._find_min(current.right)
                current.data = successor.data
                result, current.right, duration = self._delete_recursive(current.right, successor.data, start_time)
                return result, current, duration
    
    def _find_min(self, node):
        """
        Find the node with the minimum value in the subtree rooted at node
        
        Args:
            node: The root of the subtree
            
        Returns:
            Node: The node with the minimum value
        """
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def inorder_traversal(self):
        """
        Perform an inorder traversal of the tree
        
        Returns:
            list: List of data in sorted order
            float: Time taken for the operation
        """
        # Start performance measurement
        start_time = time.time()
        
        result = []
        self._inorder_recursive(self.root, result)
        return result, time.time() - start_time
    
    def _inorder_recursive(self, node, result):
        """
        Helper method for inorder traversal
        
        Args:
            node: The current node
            result: The list to store the traversal result
        """
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)
    
    def get_height(self):
        """
        Get the height of the tree
        
        Returns:
            int: The height of the tree
        """
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """
        Helper method to calculate the height recursively
        
        Args:
            node: The current node
            
        Returns:
            int: The height of the subtree rooted at node
        """
        if node is None:
            return -1
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return max(left_height, right_height) + 1
    
    def to_list(self):
        """
        Convert the tree to a list in sorted order
        
        Returns:
            list: List of data in sorted order
        """
        result, _ = self.inorder_traversal()
        return result
    
    def is_empty(self):
        """
        Check if the tree is empty
        
        Returns:
            bool: True if the tree is empty, False otherwise
        """
        return self.root is None
