"""
BinarySearchTree implementation for the Automotive Parts Catalog System.
This data structure provides hierarchical storage with efficient search capabilities.
"""
from typing import TypeVar, Generic, Optional, Callable, List, Any
from .node import Node

T = TypeVar('T')  # Generic type for the BinarySearchTree

class BinarySearchTree(Generic[T]):
    """
    A generic implementation of a Binary Search Tree data structure.
    
    This class implements a binary search tree that can store elements of any type.
    It provides methods for adding, removing, and searching for elements, as well as
    various traversal methods.
    """
    
    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None):
        """
        Initialize an empty Binary Search Tree with an optional custom comparator.
        
        Args:
            comparator: A function that compares two elements and returns:
                        negative if first < second,
                        zero if first == second,
                        positive if first > second
        """
        self._root: Optional[Node[T]] = None
        self._size: int = 0
        self._comparator = comparator or self._default_comparator
        
    def _default_comparator(self, a: T, b: T) -> int:
        """
        Default comparator function that uses the < and > operators.
        
        Args:
            a: First element to compare
            b: Second element to compare
            
        Returns:
            -1 if a < b, 0 if a == b, 1 if a > b
        """
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
            
    def insert(self, data: T) -> None:
        """
        Insert an element into the Binary Search Tree.
        
        Args:
            data: The element to insert
        """
        self._root = self._insert_recursive(self._root, data)
        self._size += 1
        
    def _insert_recursive(self, node: Optional[Node[T]], data: T) -> Node[T]:
        """
        Recursively insert an element into the tree.
        
        Args:
            node: The current node being examined
            data: The element to insert
            
        Returns:
            The node that was inserted or the updated subtree root
        """
        if node is None:
            return Node(data)
            
        compare_result = self._comparator(data, node.get_data())
        
        if compare_result < 0:
            node.set_left(self._insert_recursive(node.get_left(), data))
        elif compare_result > 0:
            node.set_right(self._insert_recursive(node.get_right(), data))
        else:
            # Duplicate data - update the node with the new data
            node.set_data(data)
            self._size -= 1  # Prevent size increment in the calling method
            
        return node
        
    def search(self, data: T) -> Optional[T]:
        """
        Search for an element in the Binary Search Tree.
        
        Args:
            data: The element to search for
            
        Returns:
            The found element or None if not found
        """
        node = self._search_recursive(self._root, data)
        return node.get_data() if node else None
        
    def _search_recursive(self, node: Optional[Node[T]], data: T) -> Optional[Node[T]]:
        """
        Recursively search for an element in the tree.
        
        Args:
            node: The current node being examined
            data: The element to search for
            
        Returns:
            The node containing the element or None if not found
        """
        if node is None:
            return None
            
        compare_result = self._comparator(data, node.get_data())
        
        if compare_result < 0:
            return self._search_recursive(node.get_left(), data)
        elif compare_result > 0:
            return self._search_recursive(node.get_right(), data)
        else:
            return node
            
    def delete(self, data: T) -> bool:
        """
        Delete an element from the Binary Search Tree.
        
        Args:
            data: The element to delete
            
        Returns:
            True if the element was found and deleted, False otherwise
        """
        if self._root is None:
            return False
            
        result = [False]  # Use a list for the result to be able to modify it in the helper method
        self._root = self._delete_recursive(self._root, data, result)
        
        if result[0]:
            self._size -= 1
            
        return result[0]
        
    def _delete_recursive(self, node: Optional[Node[T]], data: T, result: List[bool]) -> Optional[Node[T]]:
        """
        Recursively delete an element from the tree.
        
        Args:
            node: The current node being examined
            data: The element to delete
            result: A list containing a boolean to track if deletion was successful
            
        Returns:
            The updated subtree root after deletion
        """
        if node is None:
            return None
            
        compare_result = self._comparator(data, node.get_data())
        
        if compare_result < 0:
            node.set_left(self._delete_recursive(node.get_left(), data, result))
        elif compare_result > 0:
            node.set_right(self._delete_recursive(node.get_right(), data, result))
        else:
            result[0] = True  # Element found and will be deleted
            
            # Case 1: Node is a leaf
            if node.is_leaf():
                return None
                
            # Case 2: Node has only one child
            if node.get_left() is None:
                return node.get_right()
            if node.get_right() is None:
                return node.get_left()
                
            # Case 3: Node has two children
            # Find the inorder successor (smallest element in the right subtree)
            successor_data = self._find_min(node.get_right())
            node.set_data(successor_data)
            
            # Delete the inorder successor
            temp_result = [False]  # Temporary result for the recursive call
            node.set_right(self._delete_recursive(node.get_right(), successor_data, temp_result))
            
        return node
        
    def _find_min(self, node: Node[T]) -> T:
        """
        Find the minimum element in the subtree rooted at the given node.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The minimum element in the subtree
        """
        current = node
        while current.get_left() is not None:
            current = current.get_left()
        return current.get_data()
        
    def contains(self, data: T) -> bool:
        """
        Check if the Binary Search Tree contains the specified element.
        
        Args:
            data: The element to check for
            
        Returns:
            True if the element is in the tree, False otherwise
        """
        return self._search_recursive(self._root, data) is not None
        
    def __len__(self) -> int:
        """
        Return the number of elements in the Binary Search Tree.
        
        Returns:
            The number of elements in the tree
        """
        return self._size
        
    def is_empty(self) -> bool:
        """
        Check if the Binary Search Tree is empty.
        
        Returns:
            True if the tree is empty, False otherwise
        """
        return self._size == 0
        
    def clear(self) -> None:
        """
        Remove all elements from the Binary Search Tree.
        """
        self._root = None
        self._size = 0
        
    def inorder_traversal(self) -> List[T]:
        """
        Perform an inorder traversal of the Binary Search Tree.
        
        Returns:
            A list of elements in sorted order
        """
        result = []
        self._inorder_recursive(self._root, result)
        return result
        
    def _inorder_recursive(self, node: Optional[Node[T]], result: List[T]) -> None:
        """
        Recursively perform an inorder traversal.
        
        Args:
            node: The current node being visited
            result: The list to add elements to
        """
        if node is not None:
            self._inorder_recursive(node.get_left(), result)
            result.append(node.get_data())
            self._inorder_recursive(node.get_right(), result)
            
    def preorder_traversal(self) -> List[T]:
        """
        Perform a preorder traversal of the Binary Search Tree.
        
        Returns:
            A list of elements in preorder
        """
        result = []
        self._preorder_recursive(self._root, result)
        return result
        
    def _preorder_recursive(self, node: Optional[Node[T]], result: List[T]) -> None:
        """
        Recursively perform a preorder traversal.
        
        Args:
            node: The current node being visited
            result: The list to add elements to
        """
        if node is not None:
            result.append(node.get_data())
            self._preorder_recursive(node.get_left(), result)
            self._preorder_recursive(node.get_right(), result)
            
    def postorder_traversal(self) -> List[T]:
        """
        Perform a postorder traversal of the Binary Search Tree.
        
        Returns:
            A list of elements in postorder
        """
        result = []
        self._postorder_recursive(self._root, result)
        return result
        
    def _postorder_recursive(self, node: Optional[Node[T]], result: List[T]) -> None:
        """
        Recursively perform a postorder traversal.
        
        Args:
            node: The current node being visited
            result: The list to add elements to
        """
        if node is not None:
            self._postorder_recursive(node.get_left(), result)
            self._postorder_recursive(node.get_right(), result)
            result.append(node.get_data())
            
    def get_height(self) -> int:
        """
        Get the height of the Binary Search Tree.
        
        Returns:
            The height of the tree (number of edges in longest path from root to leaf)
        """
        return self._get_height_recursive(self._root)
        
    def _get_height_recursive(self, node: Optional[Node[T]]) -> int:
        """
        Recursively calculate the height of the subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The height of the subtree
        """
        if node is None:
            return -1
            
        left_height = self._get_height_recursive(node.get_left())
        right_height = self._get_height_recursive(node.get_right())
        
        return max(left_height, right_height) + 1
    
    def __str__(self) -> str:
        """
        Return a string representation of the Binary Search Tree.
        
        Returns:
            A string representation of the tree
        """
        if self.is_empty():
            return "BinarySearchTree{}"
        
        elements = self.inorder_traversal()
        return f"BinarySearchTree{elements}"
    
    def find_by_key(self, key_func: Callable[[T], Any], target_key: Any) -> Optional[T]:
        """
        Find an element by a key derived from a function.
        
        This is useful for searching by a specific field in an object.
        
        Args:
            key_func: A function that extracts the key from an element
            target_key: The key to search for
            
        Returns:
            The found element or None if not found
        """
        return self._find_by_key_recursive(self._root, key_func, target_key)
    
    def _find_by_key_recursive(self, node: Optional[Node[T]], key_func: Callable[[T], Any], 
                               target_key: Any) -> Optional[T]:
        """
        Recursively search for an element by key.
        
        Args:
            node: The current node being examined
            key_func: A function that extracts the key from an element
            target_key: The key to search for
            
        Returns:
            The found element or None if not found
        """
        if node is None:
            return None
        
        current_key = key_func(node.get_data())
        
        if current_key == target_key:
            return node.get_data()
        
        # In a BST, we would normally know which subtree to search based on the ordering
        # But since we're searching by a custom key, we need to search both subtrees
        left_result = self._find_by_key_recursive(node.get_left(), key_func, target_key)
        if left_result is not None:
            return left_result
        
        return self._find_by_key_recursive(node.get_right(), key_func, target_key)
