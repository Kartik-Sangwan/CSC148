"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will write two different functions that operate on a Stack.
Pay attention to whether or not the stack should be modified.
"""
from typing import Any, List


###############################################################################
# Task 1: Practice with stacks
###############################################################################
class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in this stack. The end of the list represents
    #     the top of the stack.
    _items: List

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return self._items == []

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError
        else:
            return self._items.pop()

    def mysteryyy(self) -> None:
        """Reverese the bottom two elements of the stack.
        """
        first = self.pop()
        second = self.pop()
        if self.is_empty():
            self.push(first)
            self.push(second)
        else:
            self.push(second)
            mystery(s)
            self.push(first)

class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass


def size(s: Stack) -> int:
    """Return the number of items in s.

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size(s)
    3
    """
    side_stack = Stack()
    count = 0
    # Pop everything off <s> and onto <side_stack>, counting as we go.
    while not s.is_empty():
        side_stack.push(s.pop())
        count += 1
    # Now pop everything off <side_stack> and back onto <s>.
    while not side_stack.is_empty():
        s.push(side_stack.pop())
    # <s> is restored to its state at the start of the function call.
    # We consider that it was not mutated.
    return count


def remove_big(s: Stack) -> None:
    """Remove the items in <stack> that are greater than 5.

    Do not change the relative order of the other items.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> s.push(8)
    >>> s.push(4)
    >>> remove_big(s)
    >>> s.pop()
    4
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    """
    s_copy = Stack()
    while not s.is_empty():
        a = s.pop()
        if a <= 5:
            s_copy.push(a)
    while not s_copy.is_empty():
        s.push(s_copy.pop())



def double_stack(s: Stack) -> Stack:
    """Return a new stack that contains two copies of every item in <stack>.

    We'll leave it up to you to decide what order to put the copies into in
    the new stack.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> new_stack = double_stack(s)
    >>> s.pop()  # s should be unchanged.
    29
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    >>> new_items = []
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> sorted(new_items)
    [1, 1, 29, 29]
    """
    s1 = Stack()
    s2 = Stack()
    while not s.is_empty():
        a = s.pop()
        s1.push(a)
        s1.push(a)
        s2.push(a)
    while not s2.is_empty():
        s.push(s2.pop())

    return s1


def mystery(s: Stack) -> None:
    """
    Swap the bottom most and the top most element in the stack.
    """
    one = s.pop()
    temp = Stack()
    while not s.is_empty():
        temp.push(s.pop())
    two = temp.pop()
    s.push(one)
    while not temp.is_empty():
        s.push(temp.pop())
    s.push(two)


def reverse_list(lst: List[Any]) -> List[Any]:
    """reverese a list."""
    lst = [1]
    for i in range(len(l)//2):
        temp = l[i]
        l[i] = l[len(l) - i - 1]
        l[len(l) - i - 1] = temp
    return l


def size_w(stack: Stack):
    """"wrong implementation.
    """
    copy = stack
    count = 0
    while not copy.is_empty():
        copy.pop()
        count = count + 1
    return count


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    s.push(4)
    s.mysteryyy()
