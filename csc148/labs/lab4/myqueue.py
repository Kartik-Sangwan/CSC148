"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will develop an implementation of the Queue ADT.
It will be helpful to review the stack implementation from lecture.

After you've implemented the Queue, you'll write two different functions that
operate on a queue, paying attention to whether or not the queue should be
modified.
"""
from typing import Any, List, Optional, Callable


# TODO: implement this class! Note that you'll need at least one private
# attribute to store items.
class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.
    """
    _items: List[int]

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        if len(self._items) == 0:
            return True
        else:
            return False

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        self._items.append(item)

    def dequeue(self) -> Optional[Any]:
        """Remove and return the item at the front of this queue.

        Return None if this Queue is empty.
        (We illustrate a different mechanism for handling an erroneous case.)

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        if self.is_empty():
            return None
        else:
            return self._items.pop(0)

    def helper(self):
        if self.is_empty():
            return 0
        item = self.dequeue()
        val = self.helper() + 1
        self.enqueue(item)
        return val

def mystery(q: Queue):
    # val = q.helper()
    val = q.helper()
    return val

class DoubleQueue(Queue):
    """A Double Queue.
    """
    def __init__(self, is_special: Callable) -> None:

        Queue.__init__(self)
        self.is_special = is_special

def is_special(a: int) -> bool:
    """aa"""
    return a == 5


def product(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Remove all items from the queue.

    Precondition: integer_queue contains only integers.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> q.enqueue(6)
    >>> product(q)
    48
    >>> q.is_empty()
    True
    """
    product = 1
    while not integer_queue.is_empty():
        product = product * integer_queue.dequeue()

    return product


def product_star(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Precondition: integer_queue contains only integers.

    >>> primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> prime_line = Queue()
    >>> for prime in primes:
    ...     prime_line.enqueue(prime)
    ...
    >>> product_star(prime_line)
    6469693230
    >>> prime_line.is_empty()
    False
    """
    side_q = Queue()
    product = 1
    while not integer_queue.is_empty():
        a = integer_queue.dequeue()
        product = product * a
        side_q.enqueue(a)
    while not side_q.is_empty():
        integer_queue.enqueue(side_q.dequeue())

    return product


def filter_queue(q: Queue(), minimum: int) -> None:
    """
    Remove all items from <q> that are less than <minimum>.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(21)
    >>> q.enqueue(5)
    >>> q.enqueue(1)
    >>> filter_queue(q, 10)
    >>> q.dequeue()
    21
    >>> q.is_empty()
    True
    """
    temp_queue = Queue()
    while not q.is_empty():
        value = q.dequeue()
        if value >= minimum:
            temp_queue.enqueue(value)

    while not temp_queue.is_empty():
        q.enqueue(temp_queue.dequeue())

def mystery2(n: int):
    if n == 0:
        return False
    if n == 1:
        return True
    return mystery2(n-2)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
