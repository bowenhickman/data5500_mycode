"""
hard.py — Essay on deleting a node from a Binary Search Tree (BST)

When deleting a node from a binary search tree, we must make sure
the tree still follows the BST rule — values on the left must be smaller,
and values on the right must be larger than the node’s value.

Here are the three main cases:

1) The node to delete has no children (a leaf node)
   - Just remove it by setting its parent’s pointer to None.

2) The node to delete has one child
   - Replace the node with its child. This means linking the parent
     directly to that child so the tree stays connected.

3) The node to delete has two children
   - Find the node’s in-order successor (the smallest value in its right subtree)
     or in-order predecessor (the largest value in its left subtree).
   - Copy that value into the node you’re deleting.
   - Then delete the successor or predecessor node, which will now
     be a simpler case (it will have at most one child).

Challenges and edge cases:
- Deleting the root: If the node being deleted is the root, the function
  must return the new root of the tree.
- Empty tree: If the tree is empty, there’s nothing to delete.
- Duplicates: You need to decide whether duplicates are allowed. If they are,
  you should consistently decide whether they go to the left or right.
- Unbalanced trees: If the tree is very unbalanced, deleting can still work
  correctly, but it may be slow (up to O(n) time).

In summary:
Deleting from a BST keeps the tree valid by replacing or removing nodes
carefully so that all values remain ordered correctly.
"""
