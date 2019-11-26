from typing import Union, List, Optional


def add_n(obj: Union[int, List], n: int) -> Union[int, List]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(obj, int):
        return obj + n
    else:
        s = []
        for sublist in obj:
            s.append(add_n(sublist, n))
        return s


def nested_list_equal(obj1: Union[int, List], obj2: Union[int, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    if isinstance(obj1, int) and isinstance(obj2, int):
        return obj1 == obj2
    elif (isinstance(obj1, list) and isinstance(obj2, int)) or (
            isinstance(obj2, list) and isinstance(obj1, int)):
        return False
    else:
        if len(obj1) != len(obj2):
            return False
        else:
            for i in range(len(obj1)):
                if not nested_list_equal(obj1[i], obj2[i]):
                    return False
        return True


def duplicate(obj: Union[int, List]) -> Union[int, List]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    # HINT: in the recursive case, you'll need to distinguish between
    # a <sublist> that is an int and a <sublist> that is a list
    # (put an isinstance check inside the loop).

    if isinstance(obj, int):
        return [obj, obj]
    else:
        s = []
        for sublist in obj:
            if isinstance(sublist, list):
                s.append(duplicate(sublist))
            else:
                s.extend(duplicate(sublist))
    return s


def __contains__(obj: Union[int, list], n: int) -> bool:
    """a"""
    if isinstance(obj, int):
        return obj == n
    else:
        for sublist in obj:
            if __contains__(sublist, n):
                return True
        return False


def first_at_depth(obj: Union[int, list], n: int) -> Optional[int]:
    """Returns the leftmost item at depth d.
    """
    if isinstance(obj, int):
        if n == 0:
            return obj
        else:
            return None
    else:
        for sublist in obj:
            item = first_at_depth(sublist, n - 1)
            if item is not None:
                return item


def add_one(obj: Union[int, List]) -> None:
    """add one to each integer in obj.
    """
    if isinstance(obj, int):
        pass
        # equivalent to return None
    else:
        for i in range(len(obj)):
            if isinstance(obj[i], int):
                # we have to mutate the contents of list if it is an integer
                # as we don't do anything in the base case.
                obj[i] += 1
            else:
                add_one(obj[i])

def semi_homogeneous(obj: Union[int, List]) -> bool:
    """Return whether obj is a semi-homogenenous nested list.(Lab 7)

    >>> semi_homogeneous(3)
    True
    >>> semi_homogeneous([1, 2, 3])
    True
    >>> semi_homogeneous([1, [2], 3])
    False
    >>> semi_homogeneous([3])
    True
    >>> semi_homogeneous([[1, 2], [3], [4]])
    True
    >>> semi_homogeneous([[[1],2 ,[3,3], [2]], [2], [3]])
    False
    """
    if obj == [] or isinstance(obj, int):
        return True
    else:
        # or you can just take the type of the first sublist right at the start.
        integers, lists = 0, 0
        for sublist in obj:
            if isinstance(sublist, int):
                integers = 1
                if not semi_homogeneous(sublist):
                    return False
            else:
                lists = 1
                if not semi_homogeneous(sublist):
                    return False

            if integers == 1 and isinstance(sublist, list):
                return False
            if lists == 1 and isinstance(sublist, int):
                return False

        return True
def max_same_depth(obj: Union[List, int], max_depth) -> int:
    """Return the maximum number of elements at any depth.
    """
    maximum = 0
    for i in range(max_depth):
        local_max = elements_at_depth(obj, i + 1)
        if local_max > maximum:
            maximum = local_max
    return maximum

def elements_at_depth(obj: Union[List, int], depth: int)->int:
    """Return the number of elements at depth in obj.
    """
    if isinstance(obj, int):
        if depth == 0:
            return 1
        else:
            return 0
    else:
        total = 0
        for sublist in obj:
            total += elements_at_depth(sublist, depth - 1)

        return total
def wrong_count_odd(obj: Union[int, List]) -> int:
    if isinstance(obj, int):
        if obj % 2 == 0:
            return 0
        else:
            return 1
    else:
        for sublist in obj:
            return wrong_count_odd(sublist)

def sum_wrong(obj: Union[List, int]) -> int:
    sum = 0
    if isinstance(obj, int):
        sum = sum + obj
    else:
        for lst_i in obj:
            sum_wrong(lst_i)
        return sum



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # import python_ta
    # python_ta.check_all()
    lst = 1
    add_one(lst)
    lst = [1, 0, [1, 2, 3, [4]]]
    elements_at_depth(lst, 2)
