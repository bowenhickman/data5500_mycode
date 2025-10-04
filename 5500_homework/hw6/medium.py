"""
ChatGPT prompt included per instructions:

Please write a Python program to solve each of the following questions. 

Create a folder named hw6, in your vscode environment. Create one Python file for each question: easy.py, medium.py, hard.py

You are highly encouraged to use ChatGPT.  You MUST include any prompts/questions you entered into ChatGPT, as a comment in your code.

Medium: (5 points)
2. Given an array of integers, write a function that finds the second largest number in the array.
Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.

Deliverables in Github: Create a folder, hw6, in your private repo, and add the files named easy.py, medium.py, hard.py.  These files should contain the code to solve each problem.
"""

from typing import Iterable, Optional


def second_largest(nums: Iterable[int]) -> Optional[int]:
    """
    Return the second largest *distinct* number in nums.
    If there are fewer than 2 distinct values, return None.

    Algorithm:
        Single pass, track the largest (m1) and second largest (m2).
        For each x:
          - if x > m1: shift m1 to m2, set m1 = x
          - elif m2 < x < m1: set m2 = x
        Equal values do not change order (ensures 'distinct').

    Time Complexity (Big-O):
        O(n) — one pass through the array.
    Space Complexity:
        O(1) auxiliary space.

    Examples:
        [5, 1, 7, 7, 3] -> 5   (largest=7, second largest=5)
        [2, 2, 2]       -> None (no second distinct)
        [9, -1]         -> -1
    """
    m1 = None  # largest
    m2 = None  # second largest

    for x in nums:
        if m1 is None or x > m1:
            m2 = m1
            m1 = x
        elif x != m1 and (m2 is None or x > m2):
            m2 = x

    return m2


if __name__ == "__main__":
    print(second_largest([5, 1, 7, 7, 3]))  # 5
    print(second_largest([2, 2, 2]))        # None
    print(second_largest([9, -1]))          # -1
    print(second_largest([-10, -3, -3, -5]))# -5
