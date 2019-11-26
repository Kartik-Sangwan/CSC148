"""Prep 6 Synthesize

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
Your task in this prep is to implement each of the following recursive functions
on nested lists, using the following steps for *Recursive Function Design*:

1.  Identify the recursive structure of the input (in this case, always a nested
    list), and write down the code template for nested lists:

    def f(obj: Union[int, List]) -> ...:
        if isinstance(obj, int):
            ...
        else:
            ...
            for sublist in obj:
                ... f(sublist) ...
            ...

2.  Implement the base case(s) directly (in this case, a single integer).
3.  Write down a concrete example with a somewhat complex argument, (in this
    case, a nested list with around 3 sub-nested-lists), and then write down
    the relevant recursive calls and what they should return.
4.  Determine how to combine the recursive calls to compute the correct output.
    Make sure you can express this in English first, and then implement your
    idea.

HINT: The implementations here should be similar to ones you've seen
before in the readings or comprehension questions.
"""
from typing import Union, List


def num_positives(obj: Union[int, List]) -> int:
    """Return the number of positive integers in <obj>.

    Remember, 0 is *not* positive.

    >>> num_positives(17)
    1
    >>> num_positives(-10)
    0
    >>> num_positives([1, -2, [-10, 2, [3], 4, -5], 4])
    5
    """
    if isinstance(obj, int) and obj > 0:
        return 1
    elif isinstance(obj, int) and obj <= 0:
        return 0
    else:
        num = 0
        for sublist in obj:
            num += num_positives(sublist)
    return num


def nested_max(obj: Union[int, List]) -> int:
    """Return the maximum integer stored in nested list <obj>.

    Return 0 if <obj> does not contain any integers.

    Precondition: all integers in <obj> are > 0.

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    maximum = 0
    if isinstance(obj, int):
        return obj
    else:
        for sublist in obj:
            local_max = nested_max(sublist)
            if local_max > maximum:
                maximum = local_max
        return maximum


def max_length(obj: Union[int, List]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> max_length(17)
    0
    >>> max_length([1, 2, [1, 2], 4])
    4
    >>> max_length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return 0
    else:
        max_len = 0
        for sublist in obj:
            local_max_len = max_length(sublist)
            if local_max_len > max_len:
                max_len = local_max_len
        return max(max_len, len(obj))


def count(obj: Union[int, List], n: int) -> int:
    """count the number of occurences of n in obj.
    """
    if isinstance(obj, int):
        if obj == n:
            return 1
        else:
            return 0
    else:
        c = 0
        for sublist in obj:
            c += count(sublist, n)
        return c


if __name__ == '__main__':
    import doctest
    doctest.testmod()
