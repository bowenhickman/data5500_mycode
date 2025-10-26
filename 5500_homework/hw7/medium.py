# medium.py — Search for a value in a Binary Search Tree (BST)
# This program defines a function that checks if a value
# exists in the BST and returns True or False.

from dataclasses import dataclass
from typing import Optional, Any

# Node class is the same as before
@dataclass
class Node:
    key: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None

def search(root: Optional[Node], value: Any) -> bool:
    # Start from the root and move down until the value is found or we reach a dead end
    current = root

    # Keep looping while there are still nodes to check
    while current is not None:
        # If we find the value, return True
        if value == current.key:
            return True
        # If the value is smaller, go to the left
        elif value < current.key:
            current = current.left
        # If the value is larger, go to the right
        else:
            current = current.right

    # If we run out of nodes, the value was not found
    return False

# Example run for quick testing
if __name__ == "__main__":
    # Simple helper to insert nodes (same as easy.py)
    def insert(root: Optional[Node], value: Any) -> Node:
        if root is None:
            return Node(value)
        if value < root.key:
            root.left = insert(root.left, value)
        else:
            root.right = insert(root.right, value)
        return root

    # Build a small example tree
    tree = None
    for num in [5, 3, 7, 2, 4, 6, 8]:
        tree = insert(tree, num)

    # Try searching for a value that exists and one that doesn't
    print(search(tree, 4))  # Should print True
    print(search(tree, 10)) # Should print False
