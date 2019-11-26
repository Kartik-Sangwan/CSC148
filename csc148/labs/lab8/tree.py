"""Lab 8: Trees and Recursion

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains starter code for Lab 8.
Make sure you understand both the theoretical idea of trees, as well as how
we represent them in our Tree class.
"""
from __future__ import annotations

import random
from typing import Any, Optional, List, Tuple, Union


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: List[Tree]
    # the total length of this tree.
    _size: int
    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty tree.
    #
    #   Note: self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def __init__(self, root: Optional[Any], subtrees: List[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees
        # if self._subtrees == []:
        #     self._size = 1
        # for subtree in self._subtrees:
        #     self._size += subtree._size

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> 1 in t  # Same as t.__contains__(1)
        True
        >>> 5 in t
        True
        >>> 4 in t
        False
        """
        if self.is_empty():
            return False

        # item may in root, or subtrees
        if self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if item in subtree:
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s

    def average(self) -> float:
        """Return the average of all the values in this tree.

        Return 0 if this tree is empty.

        Precondition: this is a tree of numbers.

        >>> Tree(None, []).average()
        0.0
        >>> t = Tree(13, [Tree(2, []), Tree(6, [])])
        >>> t.average()
        7.0
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.average()
        5.5
        """
        if self.is_empty():
            return 0.0

        total, count = self._average_helper()
        return total / count

    def _average_helper(self) -> Tuple[int, int]:
        """Return a tuple (x,y) where:

        x is the total values in this tree, and
        y is the size of this tree.
        """
        if self.is_empty():
            return 0, 0
        else:
            total = self._root
            number = 1
            for subtree in self._subtrees:
                child_total, child_number = subtree._average_helper()
                total += child_total
                number += child_number
            return total, number

    def delete_item(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Return True if <item> was deleted, and False otherwise.
        Do not modify this tree if it does not contain <item>.

        **NOTE**
        This code is incomplete in one subtle way: it leaves empty trees
        in the list self._subtrees! This might cause some unexpected behaviour
        in some other tree methods. We'll discuss this more on Friday's lecture.
        """
        if self.is_empty():
            # The item is not in the tree.
            return False
        elif self._root == item:
            # We've found the item: now delete it.
            self._delete_root()
            return True
        else:
            # Loop through each subtree, and stop the first time
            # the item is deleted. (This is why a boolean is returned!)
            for subtree in self._subtrees:
                deleted = subtree.delete_item(item)
                if deleted:
                    return True
                else:
                    # No item was deleted. Continue onto the next subtree.
                    # Note that this branch is unnecessary; we've only shown
                    # it to write comments.
                    pass

            # If we don't return inside the loop, the item is not deleted
            # from any of the subtrees. In this case, the item does not
            # appear in this tree.
            return False

    def _delete_root(self) -> None:
        """Delete the root of this tree.

        Precondition: this tree is non-empty.
        """
        if self._subtrees == []:
            # This is a leaf. Deleting the root gives and empty tree.
            self._root = None
        else:
            # This tree has more than one value!
            # Can't just set self._root = None, need to REPLACE it.

            # Strategy 1: "Promote" a subtree.
            # 1. Remove the rightmost subtree.
            last_subtree = self._subtrees.pop()

            # 2. Update self._root
            self._root = last_subtree._root

            # 3. Update self._subtrees
            # can also use extend same thing.
            self._subtrees += last_subtree._subtrees

            # Strategy 2: Replace with a leaf.
            # 1. Extract the leftmost leaf (using another helper).
            # leaf = self._extract_leaf()
            #
            # 2. Update self._root. (Note that self._subtrees remains the same.)
            # self._root = leaf

    def _extract_leaf(self) -> Any:
        """Remove and return the leftmost leaf's root in a tree.

        Precondition: this tree is non-empty.
        """
        if self._subtrees == []:
            old_root = self._root
            self._root = None
            return old_root
        else:
            return self._subtrees[0]._extract_leaf()

    def delete_all_item(self, item: Any) -> None:
        """Delete all occurences of item in the tree.
        """
        if self.is_empty():
            return
        # elif self._subtrees == [] and self._root == item:
        #     self._delete_root()
        else:
            if self._root == item:
                self._delete_root()
                self.delete_all_item(item)
            for subtree in self._subtrees:
                subtree.delete_all_item(item)

    def leaves(self) -> List[int]:
        """Return the leaves in this tree.
        """
        if self.is_empty():
            return []
        elif self._subtrees == []:
            return [self._root]
        else:
            lst = []
            for subtree in self._subtrees:
                lst.extend(subtree.leaves())
            return lst

    # ------------------------------------------------------------------------
    # Lab Task 1: Non-mutating tree methods
    # ------------------------------------------------------------------------
    # TODO: implement this method!
    def branching_factor(self) -> float:
        """Return the average branching factor of this tree's internal values.

        Return 0.0 if this tree does not have internal values.

        >>> Tree(None, []).branching_factor()
        0.0
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.branching_factor()
        2.0
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.branching_factor()
        3.0
        """
        if self.is_empty():
            return 0.0

        total_nodes, internal_nodes = self.helper()
        return (total_nodes - 1)/internal_nodes

    def helper(self) -> Tuple[int, int]:
        """Return the number of internal nodes and total nodes.
        """
        if self.is_empty():
            return 0, 0
        else:
            internal_nodes = 1
            total_nodes = 1
            for subtree in self._subtrees:
                total, internal = subtree.helper()
                total_nodes += total
                if not subtree._subtrees == []:
                    internal_nodes += internal
            return total_nodes, internal_nodes

    # TODO: implement this method!
    def items_at_depth(self, d: int) -> List:
        """Return a list of the values in this tree at the given depth.

        Precondition: d >= 1. (Depth 1 is the root of the tree.)

        We've provided some doctests for the empty and size-one tree cases.
        You'll want to write more doctests when working on the recursive case.

        >>> t1 = Tree(None, [])
        >>> t1.items_at_depth(2)
        []
        >>> t2 = Tree(5, [])
        >>> t2.items_at_depth(1)
        [5]
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, [Tree(5, [])]), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.items_at_depth(1)
        [1]
        >>> t.items_at_depth(2)
        [2, 3]
        >>> t.items_at_depth(3)
        [4, 5, 6, 7, 8, 9, 10]
        >>> t.items_at_depth(4)
        [5]
        """
        if self.is_empty():
            return []
        elif d == 1:
            return [self._root]
        else:
            lst = []
            for subtree in self._subtrees:
                lst.extend(subtree.items_at_depth((d - 1)))
            return lst
    # ------------------------------------------------------------------------
    # Lab Task 2: Tree insertion
    # ------------------------------------------------------------------------
    # TODO: implement this method!
    def insert(self, item: Any) -> None:
        """Insert <item> into this tree using the following algorithm.

            1. If the tree is empty, <item> is the new root of the tree.
            2. If the tree has a root but no subtrees, create a
               new tree containing the item, and make this new tree a subtree
               of the original tree.
            3. Otherwise, pick a random number between 1 and 3 inclusive.
                - If the random number is 3, create a new tree containing
                  the item, and make this new tree a subtree of the original.
                - If the random number is a 1 or 2, pick one of the existing
                  subtrees at random, and *recursively insert* the new item
                  into that subtree.

        >>> t = Tree(None, [])
        >>> t.insert(1)
        >>> 1 in t
        True
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.insert(100)
        >>> 100 in t
        True
        """
        if self.is_empty():
            self._root = item
        elif self._subtrees == []:
            t = Tree(item, [])
            self._subtrees.append(t)
        else:
            num = random.randint(1, 3)
            if num == 3:
                t = Tree(item, [])
                self._subtrees.append(t)
            else:
                l = len(self._subtrees)
                num = random.randint(0, l - 1)
                random_tree = self._subtrees[num]
                random_tree.insert(item)

    def insert_child(self, child: Any, parent: Any)->bool:
        """Insert <item> into this tree as a child of <parent>.If successful,
        return True. If <parent> is not in this tree, return False.If <parent>
        appears more than once in this tree, <item> should onlybe inserted once
        (you can pick where to insert it)."""
        if self.is_empty():
            return False
        else:
            if self._root == parent:
                t = Tree(child, [])
                self._subtrees.append(t)
                return True
            else:
                for subtree in self._subtrees:
                    if subtree.insert_child(child, parent):
                        return True
                return False


    def preorder(self) -> str:
        """Return a string representation of the tree items in preorder order.
        """
        if self.is_empty():
            return ''
        else:
            s = str(self._root)
            for subtree in self._subtrees:
                s += ' ' + subtree.preorder()
            return s

    def postorder(self) -> str:
        """Return a string representation of the tree items in postorder order.
        """
        if self.is_empty():
            return ''
        else:
            s = ' '
            for subtree in self._subtrees:
                s += subtree.preorder() + ' '
            return s + str(self._root)

    # def inorder(self) -> str:
    #     """Return a string representation of the tree items in inorder order.
    #     Inorder for a normal tree isnt possible I think as what will be the mid
    #     way of the subtree (many).
    #     """


    def to_nested_list(self) -> List[str]:
        """return a nested list version of the tree.
        """
        # this case if never reached as we only
        # recurse to the leaf an return [self._root]
        # if self.is_empty():
        #     return []
        # if self._subtrees == []:
        #     return [self._root]
        # else:
        lst = []
        lst.append(self._root)
        for subtree in self._subtrees:
            lst.append(subtree.to_nested_list())
        return lst


def to_tree(l: List[Union[int, List]]) -> Optional[Tree]:
    """Return a tree representation of a nested list.
    """
    if isinstance(l, int):
        return l
    else:
        subtrees = []
        for sublist in l:
            subtrees.append(to_tree(sublist))
            t = Tree(sublist, subtrees)
        return t


def duplicate(matrix: List[List[int]]) -> List[List[int]]:
    """Return a duplicate of the matrix.
    """
    answer = []
    for item in matrix:
        answer.append(item)
    return answer

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #
    # import python_ta
    # python_ta.check_all(config={'extra-imports': ['random']})
    lt = Tree(2, [Tree(89, []), Tree(2, [])])
    rt = Tree(2, [Tree(2, []), Tree(6, []), Tree(20, []), Tree(9, []), Tree(10, [])])
    t = Tree(1, [lt, rt])
    # # t.delete_all_item(9)
    # # print(t)
    # print(t.leaves())

