"""Lab 5: Linked List Exercises

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from __future__ import annotations
from typing import Any, List, Optional


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.
            The first node contains the first item from items list.
        """
        self._first = None
        curr = None
        for item in items:
            new_node = _Node(item)
            if curr is None:
                self._first = new_node
                curr = new_node
            else:
                curr.next = new_node
                curr = new_node
    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        assert curr is None or curr_index == index

        if curr is None:
            raise IndexError
        else:
            return curr.item
        # if curr_index == index:
        #     return curr.item
        # else:
        #     raise IndexError

    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first # this self._first is actually None
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next

    # ------------------------------------------------------------------------
    # Lab Task 1
    # ------------------------------------------------------------------------
    # TODO: implement this method
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        curr = self._first
        length = 0
        while curr is not None:
            length += 1
            curr = curr.next
        return length

    # TODO: implement this method
    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        # this even takes care of empty linked List
        appear = 0
        curr = self._first
        while curr is not None:
            if curr.item == item:
                appear += 1
            curr = curr.next
        return appear

    # TODO: implement this method
    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        curr = self._first
        index_item = 0
        while curr is not None:
            if curr.item == item:
                return index_item
            index_item += 1
            curr = curr.next
        if curr is None:
            raise ValueError

    # TODO: implement this method
    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 3])
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        """
        # curr = self._first
        # i = 0
        # if index < len(self):
        #     while curr is not None:
        #         if i == index:
        #             curr.item = item
        #         i += 1
        #         curr = curr.next
        # else:
        #     raise IndexError
        # OR

        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            curr.item = item


    def swap(self, i: int, j: int) -> None:
        """Swap the items at index i and index j in the linked list.
        linky = LinkedList([10, 20, 30, 40, 50])

        >>> linky = LinkedList([10, 20, 30, 40, 50])
        >>> linky.swap(0, 3)
        >>> str(linky)
        '[40 -> 20 -> 30 -> 10 -> 50]'
        """
        if self._first is None:
            raise IndexError
        else:
            curr_i, curr_j = 0, 0
            curr1, curr2 = self._first, self._first
            while curr1 is not None and curr_i < i:
                curr1 = curr1.next
                curr_i += 1
            while curr2 is not None and curr_j < j:
                curr2 = curr2.next
                curr_j += 1
            if curr1 is None or curr2 is None:
                raise IndexError
            else:
                temp = curr1.item
                curr1.item = curr2.item
                curr2.item = temp

    def delete_index(self, index: int) -> Any:
        """Delete the item at index <<index>> and return the item.
        """
        if self.is_empty():
            raise IndexError
        elif index == 0:
            item = self._first.item
            self._first = self._first.next
            return item
        else:
            curr = self._first
            curr_index = 0

            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            # In deletion curr.next is None check is important as we stop
            # before the last node and it may be the last node of the user
            # enters index == length of our list

            if curr is None or curr.next is None:
                raise IndexError
            else:
                item = curr.next.item
                curr.next = None
                return item


    def average(self) -> float:
        """Return the average of all the values in a linked list.
        """
        curr = self._first
        total = 0
        length = 0
        while curr is not None:
            total += curr.item
            length += 1
            curr = curr.next
        return total/length

    def intersperse(self, other: LinkedList) -> None:
        """Insert the elements of other in this linked list in corresponding
        positions.
        """
        curr1 = self._first
        curr2 = other._first
        while curr1 is not None:
            value = curr2.item
            new_node = _Node(value)
            temp = curr1.next
            curr1.next = new_node
            new_node.next = temp
            curr1 = curr1.next.next
            curr2 = curr2.next

    # def bisect(self, i: int) -> None:
    #
    #     curr = self._first
    #     index = 0
    #     while curr is not None and index < i:
    #         index += 1
    #         curr = curr.next
    #     if curr is None:
    #         raise IndexError
    #     else:
    #         # if curr.next is not None:
    #         curr.next = None

    def bisect_return(self, i: int) -> LinkedList:
        """Bisect at index i including i and return the rest of the linked list
        as a new linked list.
        """
        curr = self._first
        index = 0
        if i == 0:
            new = LinkedList([])
            new._first = self._first
            self._first = None
            return new
            # this is wrong as aliasing happens hence initial temp gets changed
            # [] empty linked list.
            # temp = self
            # self._first = None
            # return temp

        while curr is not None and index < i - 1:
            index += 1
            curr = curr.next
        if curr is None:
            raise IndexError
        else:
            temp = curr.next
            curr.next = None
            new = LinkedList([])
            new._first = temp
            return new

    def remove(self, item: Any) -> None:
        """Remove the first occurrence of the item in this linked list.
        """
        # see there were many aspects to look into carefully.
        curr = self._first
        if curr is None:
            return
        if curr.item == item:
            self._first = self._first.next
            return
        while curr is not None:
            if curr.next is not None and curr.next.item == item:
                curr.next = curr.next.next
                return
            # NEVER EVER FORGET THIS CURR = CURR.NEXT STATEMENT.
            curr = curr.next

    def insert_whole(self, other: LinkedList, i: int) -> None:
        """Insert immediately after i th index.
        """
        if not other.is_empty():
            curr1 = other._first
            lst = []
            while curr1 is not None:
                lst.append(curr1.item)
                curr1 = curr1.next
            copy = LinkedList(lst)
            curr = copy._first
            while curr.next is not None:
                curr = curr.next
            if i == 0:
                self._first, curr.next = copy._first, self._first
            else:
                curr2 = self._first
                index = 0
                while curr2 is not None and index < i:
                    curr2 = curr2.next
                    index += 1

                if curr2 is None:
                    raise IndexError
                else:
                    temp = curr2.next
                    curr2.next = copy._first
                    curr.next = temp

    def mystery(self):
        if len(self) < 2:
            return None
        else:
            previous = self._first
            current = previous.next
            while current is not None and current.item >= previous.item:
                previous = current
                current = current.next
            if current is not None:
                return current.item
            else:
                return None


def bar(list_: list) -> None:
    bigger = []
    for item in list_:
        bigger.append(item + 100)
    list_, bigger = bigger, list_


if __name__ == '__main__':

    import doctest
    doctest.testmod()
    lst = LinkedList([1, 2, 10, 200, 10, 1])
    a = lst.bisect_return(0)
