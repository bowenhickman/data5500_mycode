# easy.py — Insert a value into a Binary Search Tree (BST)
# This program defines a simple Node class and a function
# to insert a new value into the tree while keeping it sorted.

from dataclasses import dataclass
from typing import Optional, Any

# Each Node represents one value in the tree
@dataclass
class Node:
    key: Any
    left: Optional["Node"] = None   # smaller values go here
    right: Optional["Node"] = None  # larger values go here

def insert(root: Optional[Node], value: Any) -> Node:
    # If the tree is empty, create a new node and return it as the root
    if root is None:
        return Node(value)

    # If the new value is smaller, go to the left side
    if value < root.key:
        root.left = insert(root.left, value)
    # If the new value is greater or equal, go to the right side
    else:
        root.right = insert(root.right, value)

    # Return the unchanged root node
    return root

# Example run for quick testing
if __name__ == "__main__":
    # Start with an empty tree
    tree = None

    # Insert values one at a time
    for num in [5, 3, 7, 2, 4, 6, 8]:
        tree = insert(tree, num)

    # The tree now holds the numbers 2–8 in sorted order
