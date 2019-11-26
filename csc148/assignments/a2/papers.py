"""Assignment 2: Modelling CS Education research paper data

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.

TODO: (Task 6) Complete the steps below
Recommended steps:
1. Start by reviewing the provided dataset in cs1_papers.csv. You can assume
   that any data used to generate this tree has this format,
   i.e., a csv file with the same columns (same column names, same order).
   The categories are all in one column, separated by colons (':').
   However, you should not make assumptions about what the categories are, how
   many categories there are, the maximum number of categories a paper can have,
   or the number of lines in the file.

2. Read through all the docstrings in this file once. There is a lot to take in,
   so don't feel like you need to understand it all the first time.
   Draw some pictures!
   We have provided the headers of the initializer as well as of some helper
   functions we suggest you implement. Note that we will not test any
   private top-level functions, so you can choose not to implement these
   functions, and you can add others if you want to for your solution.
   For this task, we will be testing that you are building the correct tree,
   not that you are doing it in a particular way. We will access your class
   in the same way as in the client code in the visualizer.

3. Plan out what you'll need to do to implement the PaperTree initializer.
   In particular, think about how to use the boolean parameters to do different
   things in setting up the tree. You may also find it helpful to review the
   Python documentation about the csv module, which you are permitted and
   encouraged to use. You should have a good plan, including what your subtasks
   are, before you begin writing any code.

4. Write the code for the PaperTree initializer and any helper functions you
   want to use in your design. You should not make any changes to the public
   interface of this module, or of the PaperTree class, but you can add private
   attributes and helpers as needed.

5. Tidy and test your code, and try it with the visualizer client code. Make
   sure you have documented any new private attributes, and that PyTA passes
   on your code.
"""
import csv
from typing import List, Dict
from tm_trees_final import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    TODO: Add any of your new private attributes here.
    These should store information about this paper's <authors> and <doi>.
    _authors:
        The authors of this paper.
    _url:
        The URL of the paper.
    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - All TMTree RIs are inherited.
    """

    # TODO: Add the type contracts for your new attributes here
    _authors: str
    _url: str

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        # TODO: Complete this initializer. Your implementation must not
        # TODO: duplicate anything done in the superclass initializer.
        # shouldn't the parameter be Optional[str] so we know if the tree is
        # empty or not
        TMTree.__init__(self, name, subtrees, citations)
        self._authors = authors
        self._url = doi
        if all_papers:
            a = _load_papers_to_dict(by_year)
            lst = _build_tree_from_dict(a)
            TMTree.__init__(self, name, lst)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return ':'

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'

def _helper(categories: List, name: List) -> Dict:
    """Helper for _load_papers_to_dict which returns a dictionary for the given
    categories.
    """
    # what if category is only one.
    if len(categories) == 1:
        return {categories[0]: ([name], {})}
    else:
        dic = {}
        dic[categories[0]] = ([], _helper(categories[1:], name))
        return dic


def _combine(dic1: Dict, dic2: Dict, categories: List) -> Dict:
    """Combine the two dictionaries.
    """
    # check all cases.
    if categories[0] not in dic1:
        return {categories[0]: dic2[categories[0]]}
    elif len(categories) == 1:
        name = dic2[categories[0]][0][0]
        dic1[categories[0]][0].append(name)
        return dic1
    else:
        first = dic1[categories[0]][1]
        second = dic2[categories[0]][1]
        if len(categories[1:]) != 0:
            dic_to_add = _combine(first, second, categories[1:])
        else:
            dic_to_add = _combine(first, second, [categories[0]])
        dic1[categories[0]][1].update(dic_to_add)
        return dic1

def _load_papers_to_dict(by_year: bool = False) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    # TODO: Implement this helper, or remove it if you do not plan to use it
    dic = {}
    i = 0
    temp_file = open(DATA_FILE)
    file = csv.reader(temp_file)
    data = []
    for line in file:
        data.append(line)
    data = data[1:]
    for line in data:
        if by_year:
            category = [line[2]] + line[3].split(':')
            elements = [line[0], line[1], line[2], line[3], line[4], line[5]]
        else:
            category = line[3].split(':')
            elements = [line[0], line[1], line[2], line[3], line[4], line[5]]
        temp_dict = _helper(category, elements)
        if i == 0:
            dic = temp_dict
        elif category[0] in dic:
            dic = _combine(dic, temp_dict, category)
        else:
            dic[category[0]] = temp_dict[category[0]]
        i = 1

    temp_file.close()
    return dic

def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    # TODO: Implement this helper, or remove it if you do not plan to use it
    # if nested_dict == {}:
    #     return PaperTree('', [])
    # else:
    lst = []
    for subtree in nested_dict:
        if not nested_dict[subtree][1] == {}:
            subtrees = []
            size = 0
            for paper in nested_dict[subtree][0]:
                tree = PaperTree(paper[1], [], paper[0], paper[4], int(paper[5]))
                size += int(paper[5])
                subtrees.append(tree)
            subtrees.extend(_build_tree_from_dict(nested_dict[subtree][1]))
            category = PaperTree(subtree, subtrees, citations=size)
            lst.append(category)
        else:
            size = 0
            leaves = []
            for paper in nested_dict[subtree][0]:
                author, url, title = paper[0], paper[4], paper[1]
                citations = int(paper[5])
                size += int(paper[5])
                leaves.append(PaperTree(title, [], author, url, citations))
            category = PaperTree(subtree, leaves, author, url, size)
            lst.append(category)

    return lst


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
    #     'allowed-io': ['_load_papers_to_dict'],
    #     'max-args': 8
    # })
    # _load_papers_to_dict()
    paper_tree = PaperTree('CS1', [], all_papers=True, by_year=True)

