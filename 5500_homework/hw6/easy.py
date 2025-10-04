"""
ChatGPT prompt included per instructions:

Please write a Python program to solve each of the following questions. 

Create a folder named hw6, in your vscode environment. Create one Python file for each question: easy.py, medium.py, hard.py

You are highly encouraged to use ChatGPT.  You MUST include any prompts/questions you entered into ChatGPT, as a comment in your code.

Easy: (3 points)
1. Given an array of integers, write a function to calculate the sum of all elements in the array.
Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.

Deliverables in Github: Create a folder, hw6, in your private repo, and add the files named easy.py, medium.py, hard.py.  These files should contain the code to solve each problem.
"""

from typing import Iterable


def sum_array(nums: Iterable[int]) -> int:
    """
    Return the sum of all elements in the iterable.

    We use an explicit loop to make the operation clear; using Python's built-in
    sum(nums) is also correct and equivalent in time complexity.

    Time Complexity (Big-O):
        O(n) — we visit each element exactly once.
    Space Complexity:
        O(1) auxiliary space (ignoring input storage).
    """
    total = 0
    for x in nums:
        total += x
    return total


if __name__ == "__main__":
    # Simple sanity checks
    print(sum_array([1, 2, 3, 4]))          # 10
    print(sum_array([]))                     # 0
    print(sum_array([-5, 5, 10, -10, 7]))   # 7
