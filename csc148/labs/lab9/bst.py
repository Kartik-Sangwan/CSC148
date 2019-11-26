"""Lab 9: Binary Search Trees

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few BinarySearchTree methods that you will implement.
Make sure you understand the *BST Property*; it will play an important role
in several of these methods.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple, Dict


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every item, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    # -------------------------------------------------------------------------
    # Standard Container methods (search)
    # -------------------------------------------------------------------------
    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left   # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    # ------------------------------------------------------------------------
    # Deletion code from lecture (profiled in Task 3)
    # ------------------------------------------------------------------------
    def delete(self, item: Any) -> None:
        """Remove *one* occurrence of item from this BST.

        Do nothing if <item> is not in the BST.
        """
        if self.is_empty():
            pass
        elif self._root == item:
            self.delete_root()
        elif item < self._root:
            self._left.delete(item)
        else:
            self._right.delete(item)

    def delete_root(self) -> None:
        """Remove the root of this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
            self._left = None
            self._right = None
        elif self._left.is_empty():
            # "Promote" the right subtree.
            # Note that self = self._right does NOT work!
            self._root, self._left, self._right = \
                self._right._root, self._right._left, self._right._right
        elif self._right.is_empty():
            # "Promote" the left subtree.
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
        else:
            # Both subtrees are non-empty. Can shooe to replace the root
            # from either the max value of the left subtree, or the min value
            # of the right subtree. (Implementations are very similar.)
            self._root = self._left.extract_max()

    def extract_max(self) -> Any:
        """Remove and return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._right.is_empty():
            max_item = self._root
            # "Promote" the left subtree.
            # Alternate approach: call self.delete_root()!
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
            return max_item
        else:
            return self._right.extract_max()

    # -------------------------------------------------------------------------
    # Additional BST methods
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    # ------------------------------------------------------------------------
    # Task 1
    # ------------------------------------------------------------------------
    # TODO: implement this method!
    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        if self.is_empty():
            return 0
        else:
            local_h_l = self._left.height()
            local_h_r = self._right.height()
            return 1 + max(local_h_l, local_h_r)

    # TODO: implement this method!
    def items_in_range(self, start: Any, end: Any) -> List:
        """Return the items in this BST between <start> and <end>, inclusive.

        Precondition: all items in this BST can be compared with <start> and
        <end>.
        The items should be returned in sorted order.

        As usual, use the BST property to minimize the number of recursive
        calls.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items_in_range(4, 11)
        [5, 7, 9, 11]
        >>> bst.items_in_range(10, 13)
        [11, 13]
        """
        if self.is_empty():
            return []
        elif self._root < start:
            return self._right.items_in_range(start, end)
        elif self._root > end:
            return self._left.items_in_range(start, end)
        else:
            return self._left.items_in_range(start, end) + [self._root] + \
                   self._right.items_in_range(start, end)

    # ------------------------------------------------------------------------
    # Task 2
    # ------------------------------------------------------------------------
    # TODO: implement this method!
    def insert(self, item: Any) -> None:
        """Insert <item> into this BST, maintaining the BST property.

        Do not change positions of any other nodes.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            self._root = item
            self._right = BinarySearchTree(None)
            self._left = BinarySearchTree(None)
        elif self._root > item:
            self._left.insert(item)
        else:
            self._right.insert(item)


    # ------------------------------------------------------------------------
    # Task 4
    # ------------------------------------------------------------------------
    def rotate_right(self) -> None:
        """Rotate the BST clockwise, i.e. make the left subtree the root.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> right = BinarySearchTree(11)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> bst._left = left
        >>> bst._right = right
        >>> print(bst)
        7
          3
            2
            5
          11
        <BLANKLINE>
        >>> bst.rotate_right()
        >>> print(bst)
        3
          2
          7
            5
            11
        <BLANKLINE>
        >>> bst.rotate_right()
        >>> print(bst)
        2
          3
            7
              5
              11
        <BLANKLINE>
        """
        if self.is_empty():
            pass
        else:
            left_subtree_1 = self._left._right
            left_subtree_2 = self._left._left
            right_subtree = BinarySearchTree(self._right._root)
            right_subtree._right = self._right._right
            right_subtree._left = self._right._left
            self._root, self._right._root = self._left._root, self._root
            self._right._right = right_subtree
            self._right._left = left_subtree_1
            self._left = left_subtree_2


    def rotate_left(self) -> None:
        """Rotate the BST counter-clockwise,
        i.e. make the right subtree the root.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> print(bst)
        7
          3
            2
            5
          11
            9
            13
        <BLANKLINE>
        >>> bst.rotate_left()
        >>> print(bst)
        11
          7
            3
              2
              5
            9
          13
        <BLANKLINE>
        >>> bst.rotate_left()
        >>> print(bst)
        13
          11
            7
              3
                2
                5
              9
        <BLANKLINE>
        """
        # TODO: implement this method!
        if self.is_empty():
            pass
        else:
            right_subtree_1 = self._right._right
            right_subtree_2 = self._right._left
            left_subtree = BinarySearchTree(self._left._root)
            left_subtree._right = self._left._right
            left_subtree._left = self._left._left
            self._root, self._left._root = self._right._root, self._root
            self._left._right = right_subtree_2
            self._left._left = left_subtree
            self._right = right_subtree_1

    def closest(self, item) -> Optional[int]:
        """Return the value whose absolute value with the item is minimum.
        If there is a tie return the smaler value.
        Return None if the BST is empty.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.closest(12)
        11
        """
        if self.is_empty():
            return None
        if self._root == item:
            return self._root
        elif self._root > item:
            if self._right.is_empty() and self._left.is_empty():
                return self._root
            closest = self._root
            new_closest = self._left.closest(item)
            if abs(new_closest - item) < abs(closest - item):
                return new_closest
            else:
                return closest
        else:
            if self._right.is_empty() and self._left.is_empty():
                return self._root
            closest = self._root
            new_closest = self._right.closest(item)
            if abs(new_closest - item) < abs(closest - item):
                return new_closest
            else:
                return closest


    def one_childs(self) -> int:
        """Return the number of trees in this bst which only have one child.
        """
        if self.is_empty():
            return 0
        elif (self._left.is_empty() and not self._right.is_empty()) or \
                (self._right.is_empty() and not self._left.is_empty()):
            return 1
        else:
            return self._left.one_childs() + self._right.one_childs()

    def inorder(self) -> str:
        """Return a string representation of the binary search tree in
        inorder order.
        Pre and post order are exact same just change where self._root is.
        """
        if self.is_empty():
            return ' '
        else:
            return self._left.inorder() + str(self._root) + self._right.inorder()

    def min_max(self) -> Tuple[int, int]:
        """Return the min and max in this bst.
        """
        return self.min_bst(), self.max_bst()

    def min_bst(self) -> int:
        if self._left.is_empty():
            return self._root
        else:
            return self._left.min_bst()

    def max_bst(self) -> int:
        if self._right.is_empty():
            return self._root
        else:
            return self._right.max_bst()

    def is_bst(self) -> bool:
        """Check whether the tree is a valid bst.
        """
        if self.is_empty():
            return True
        else:

            tup2 = self._left.min_max()
            tup3 = self._right.min_max()

            if not tup2[0] <= self._root or not tup2[1] <= self._root:
                return False
            if not tup3[0] >= self._root or not tup3[1] >= self._root:
                return False

            return self._left.is_bst() and self._right.is_bst()

    def levels(self) -> List[Tuple[int, List]]:
        """Return a list of items in the tree seperated by levels.
        """
        if self.is_empty():
            return []
        # elif self._left.is_empty() and self._right.is_empty():
        #     return [(1, [self._root])]
        else:
            lst = []
            lst.append((1, [self._root]))
            left = self._left.levels()
            right = self._right.levels()
            for i in range(len(left)):
                lst.append((i + 2, left[i][1] + right[i][1]))
            return lst

    def distribution(self) -> Dict[int, int]:
        """"Return the distribution of values in this binary search tree.
        """
        if self.is_empty():
            return {}
        else:
            dic = {}
            dic[self._root] = 1
            d1 = self._left.distribution()
            d2 = self._right.distribution()
            _adsorb(d1, d2)
            _adsorb(d1, dic)
            return d1

    def all_bigger(self, val: int) -> bool:
        """Return if all item in the bst are greater than val.
        """
        if self.is_empty():
            return True
        elif self._root <= val:
            return False
        else:
            if not self._left.all_bigger(val):
                return False
            return True

def _adsorb(d1: Dict, d2: Dict) -> None:
    """combine two dictionaries.
    """
    for key in d2:
        if key in d1:
            d1[key] += d2[key]
        else:
            d1[key] = d2[key]


def binary_search(lst: List, i: int, j: int, item: int) -> bool:
    """Recursive binary search.
    Precondition: lst must be sorted.
    """
    if i == j - 1:
        return False
    else:
        mid = (i + j)//2
        if item == lst[mid]:
            return True
        elif item < lst[mid]:
            return binary_search(lst, i, mid, item)
        else:
            return binary_search(lst, mid, j, item)

# to add an element in a tuple we use tuple concatenation.
# as tuples are immutable and mutating methods are not given to us.
# (1, 2, 3, 4, 5) + (6, ) = (1, 2, 3, 4, 5, 6)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #
    # import python_ta
    # python_ta.check_all()
    # see this Binary search tree that you modiefied doesn;t follow the
    # representation invariant and thus you wont get correct result of a
    # correctly implemented method(eg inorder).
    bst = BinarySearchTree(7)
    left = BinarySearchTree(3)
    left._left = BinarySearchTree(2)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(11)
    right._left = BinarySearchTree(9)
    right._right = BinarySearchTree(13)
    bst._left = left
    bst._right = right
    bst.all_bigger(0)
    # bst = BinarySearchTree(None)
    # bst.insert(39)
    # bst.insert(39)
    # bst.insert(-4)
    # bst.insert(39)
    # bst.insert(105)
    # bst.insert(-4)

