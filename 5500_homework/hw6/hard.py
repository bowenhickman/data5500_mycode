"""
ChatGPT prompt included per instructions:

Please write a Python program to solve each of the following questions. 

Create a folder named hw6, in your vscode environment. Create one Python file for each question: easy.py, medium.py, hard.py

You are highly encouraged to use ChatGPT.  You MUST include any prompts/questions you entered into ChatGPT, as a comment in your code.

Hard: (7 points)
3. Write a function that takes an array of integers as input and returns the maximum difference between any two numbers in the array.
Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.

Deliverables in Github: Create a folder, hw6, in your private repo, and add the files named easy.py, medium.py, hard.py.  These files should contain the code to solve each problem.
"""

from typing import Iterable


def max_difference(nums: Iterable[int]) -> int:
    """
    Return the maximum difference between any two numbers in nums.

    Interpretation:
        "Maximum difference between any two numbers" (order doesn't matter)
        is max(nums) - min(nums). This yields a non-negative result.
        Requires at least 2 elements.

    Time Complexity (Big-O):
        O(n) — one pass to find min and max.
    Space Complexity:
        O(1) auxiliary space.

    Raises:
        ValueError if fewer than 2 elements are provided.
    """
    iterator = iter(nums)
    try:
        first = next(iterator)
    except StopIteration:
        raise ValueError("Array must contain at least two numbers.")

    cur_min = first
    cur_max = first
    count = 1

    for x in iterator:
        count += 1
        if x < cur_min:
            cur_min = x
        elif x > cur_max:
            cur_max = x

    if count < 2:
        raise ValueError("Array must contain at least two numbers.")

    return cur_max - cur_min


if __name__ == "__main__":
    print(max_difference([7, 1, 5, 3, 6, 4]))   # 6 - 1 = 5
    print(max_difference([-10, -3, -20, 4]))    # 4 - (-20) = 24
    print(max_difference([100, 100]))           # 0
