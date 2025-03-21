"""
Custom BinarySearchTree implementation for the Automotive Parts Catalog System.
This data structure provides a binary search tree with generics.
"""
from typing import TypeVar, Generic, Optional, Callable, List, Any
from src.datastructures.linked_list import LinkedList

T = TypeVar('T')  # Generic type for the BinarySearchTree
K = TypeVar('K')  # Generic type for keys

class TreeNode(Generic[T]):
    """
    A node in a binary search tree.
    """
    
    def __init__(self, data: T):
        """
        Initialize a TreeNode with the given data.
        
        Args:
            data: The data to store in the TreeNode
        """
        self.data: T = data
        self.left: Optional[TreeNode[T]] = None
        self.right: Optional[TreeNode[T]] = None
        self.height: int = 1  # Height of the node (for AVL balancing if needed later)

class BinarySearchTree(Generic[T]):
    """
    A generic implementation of a binary search tree data structure.
    
    This class implements a binary search tree that can store elements of any type.
    It provides methods for adding, removing, and searching for elements, as well as
    various traversal methods.
    """
    
    def __init__(self, key_function: Optional[Callable[[T], Any]] = None):
        """
        Initialize an empty BinarySearchTree.
        
        Args:
            key_function: Optional function to extract a comparison key from each element.
                          If None, the element itself will be used as the key.
        """
        self._root: Optional[TreeNode[T]] = None
        self._size: int = 0
        self._key_function: Callable[[T], Any] = (lambda x: x) if key_function is None else key_function
    
    def __len__(self) -> int:
        """
        Return the number of elements in the BinarySearchTree.
        
        Returns:
            The number of elements in the BinarySearchTree
        """
        return self._size
    
    def __contains__(self, item: T) -> bool:
        """
        Check if the BinarySearchTree contains the specified item.
        
        Args:
            item: The item to check for
            
        Returns:
            True if the item is in the BinarySearchTree, False otherwise
        """
        return self._contains(self._root, self._key_function(item))
    
    def _contains(self, node: Optional[TreeNode[T]], key: Any) -> bool:
        """
        Check if the subtree rooted at the specified node contains an item with the given key.
        
        Args:
            node: The root of the subtree to search
            key: The key to search for
            
        Returns:
            True if the key is found, False otherwise
        """
        if node is None:
            return False
        
        item_key = self._key_function(node.data)
        
        if key < item_key:
            return self._contains(node.left, key)
        elif key > item_key:
            return self._contains(node.right, key)
        else:
            return True
    
    def insert(self, item: T) -> None:
        """
        Insert an item into the BinarySearchTree.
        
        Args:
            item: The item to insert
        """
        self._root = self._insert(self._root, item)
        self._size += 1
    
    def _insert(self, node: Optional[TreeNode[T]], item: T) -> TreeNode[T]:
        """
        Insert an item into the subtree rooted at the specified node.
        
        Args:
            node: The root of the subtree to insert into
            item: The item to insert
            
        Returns:
            The new root of the subtree
        """
        if node is None:
            return TreeNode(item)
        
        item_key = self._key_function(item)
        node_key = self._key_function(node.data)
        
        if item_key < node_key:
            node.left = self._insert(node.left, item)
        elif item_key > node_key:
            node.right = self._insert(node.right, item)
        else:
            # If the key already exists, replace the value
            node.data = item
            self._size -= 1  # Adjust size since we're not actually adding a new node
        
        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        return node
    
    def _get_height(self, node: Optional[TreeNode[T]]) -> int:
        """
        Get the height of the specified node.
        
        Args:
            node: The node to get the height of
            
        Returns:
            The height of the node, or 0 if the node is None
        """
        if node is None:
            return 0
        return node.height
    
    def remove(self, item: T) -> bool:
        """
        Remove the specified item from the BinarySearchTree.
        
        Args:
            item: The item to remove
            
        Returns:
            True if the item was found and removed, False otherwise
        """
        if self._root is None:
            return False
        
        result = [False]  # Use a list to allow modification in the closure
        
        def _remove_helper(node: Optional[TreeNode[T]], key: Any) -> Optional[TreeNode[T]]:
            if node is None:
                return None
            
            node_key = self._key_function(node.data)
            
            if key < node_key:
                node.left = _remove_helper(node.left, key)
            elif key > node_key:
                node.right = _remove_helper(node.right, key)
            else:
                # Found the node to remove
                result[0] = True
                
                # Case 1: Node with only one child or no child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                
                # Case 2: Node with two children
                # Get the inorder successor (smallest in the right subtree)
                successor = self._find_min(node.right)
                node.data = successor.data
                node.right = _remove_helper(node.right, self._key_function(successor.data))
            
            return node
        
        self._root = _remove_helper(self._root, self._key_function(item))
        
        if result[0]:
            self._size -= 1
        
        return result[0]
    
    def _find_min(self, node: TreeNode[T]) -> TreeNode[T]:
        """
        Find the minimum value node in the subtree rooted at the specified node.
        
        Args:
            node: The root of the subtree to search
            
        Returns:
            The node with the minimum value
        """
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def search(self, key: Any) -> Optional[T]:
        """
        Search for an item with the specified key.
        
        Args:
            key: The key to search for
            
        Returns:
            The item if found, None otherwise
        """
        return self._search(self._root, key)
    
    def _search(self, node: Optional[TreeNode[T]], key: Any) -> Optional[T]:
        """
        Search for an item with the specified key in the subtree rooted at the specified node.
        
        Args:
            node: The root of the subtree to search
            key: The key to search for
            
        Returns:
            The item if found, None otherwise
        """
        if node is None:
            return None
        
        node_key = self._key_function(node.data)
        
        if key < node_key:
            return self._search(node.left, key)
        elif key > node_key:
            return self._search(node.right, key)
        else:
            return node.data
    
    def in_order_traversal(self) -> List[T]:
        """
        Perform an in-order traversal of the BinarySearchTree.
        
        Returns:
            A list of the elements in in-order
        """
        result: List[T] = []
        self._in_order_traversal(self._root, result)
        return result
    
    def _in_order_traversal(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        """
        Helper method for in-order traversal.
        
        Args:
            node: The root of the subtree to traverse
            result: The list to add elements to
        """
        if node is not None:
            self._in_order_traversal(node.left, result)
            result.append(node.data)
            self._in_order_traversal(node.right, result)
    
    def pre_order_traversal(self) -> List[T]:
        """
        Perform a pre-order traversal of the BinarySearchTree.
        
        Returns:
            A list of the elements in pre-order
        """
        result: List[T] = []
        self._pre_order_traversal(self._root, result)
        return result
    
    def _pre_order_traversal(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        """
        Helper method for pre-order traversal.
        
        Args:
            node: The root of the subtree to traverse
            result: The list to add elements to
        """
        if node is not None:
            result.append(node.data)
            self._pre_order_traversal(node.left, result)
            self._pre_order_traversal(node.right, result)
    
    def post_order_traversal(self) -> List[T]:
        """
        Perform a post-order traversal of the BinarySearchTree.
        
        Returns:
            A list of the elements in post-order
        """
        result: List[T] = []
        self._post_order_traversal(self._root, result)
        return result
    
    def _post_order_traversal(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        """
        Helper method for post-order traversal.
        
        Args:
            node: The root of the subtree to traverse
            result: The list to add elements to
        """
        if node is not None:
            self._post_order_traversal(node.left, result)
            self._post_order_traversal(node.right, result)
            result.append(node.data)
    
    def level_order_traversal(self) -> List[T]:
        """
        Perform a level-order traversal of the BinarySearchTree.
        
        Returns:
            A list of the elements in level-order
        """
        if self._root is None:
            return []
        
        result: List[T] = []
        queue: LinkedList[TreeNode[T]] = LinkedList()
        queue.append(self._root)
        
        while not queue.is_empty():
            node = queue.remove_at(0)
            result.append(node.data)
            
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        
        return result
    
    def clear(self) -> None:
        """
        Remove all elements from the BinarySearchTree.
        """
        self._root = None
        self._size = 0
    
    def is_empty(self) -> bool:
        """
        Check if the BinarySearchTree is empty.
        
        Returns:
            True if the BinarySearchTree is empty, False otherwise
        """
        return self._size == 0
    
    def get_height(self) -> int:
        """
        Get the height of the BinarySearchTree.
        
        Returns:
            The height of the BinarySearchTree
        """
        return self._get_height(self._root)
