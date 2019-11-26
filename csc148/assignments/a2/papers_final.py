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
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'
AUTHOR_INDEX = 0
TITLE_INDEX = 1
YEAR_INDEX = 2
CATEGORY_INDEX = 3
URL_INDEX = 4
CITATION_INDEX = 5
PAPER_TITLE_INDEX = 0
PAPER_AUTHOR_INDEX = 1
PAPER_DOI_INDEX = 2
PAPER_YEAR_INDEX = 3
PAPER_CITATION_INDEX = 4


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    These should store information about this paper's <authors> and <doi>.
    _author:
        The author(s) of the Computer Science Education research paper.
    _doi:
        The Digital Object Identifier of the Computer Science Education
        research paper.

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

    _author: str
    _doi: str

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
        self._author = authors
        self._doi = doi
        if all_papers:
            dic = _load_papers_to_dict(by_year)
            lst = _build_tree_from_dict(dic)
            TMTree.__init__(self, name, lst, citations)
        else:
            TMTree.__init__(self, name, subtrees, citations)

    def get_separator(self) -> str:
        """Return the file separator for this Research Paper.
        """
        return '/'

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (paper)'
        else:
            return ' (category)'


def _make_list(data: List, by_year: bool = True) -> List:
    """Creates a dictionary with each key a category and its value is a tuple
    with 2 elements such that fist element is a list of papers in that category
    and the second element is a dictionary with other sub-categories of the same
    format."""
    lst = []
    for paper in data:
        title = paper[TITLE_INDEX]
        author = paper[AUTHOR_INDEX]
        doi = paper[URL_INDEX]
        year = paper[YEAR_INDEX]
        citation = paper[CITATION_INDEX]
        categories = paper[CATEGORY_INDEX].split(':')
        index = len(categories)
        dic = {}
        if by_year:
            dic[year.strip()] = ([], {})
            lst.append(dic)
            i = 0
            temp_dic = dic[year][1]
        else:
            dic[categories[0].strip()] = ([], {})
            lst.append(dic)
            i = 1
            temp_dic = dic[categories[0].strip()][1]
        while i != index:
            if i != index - 1:
                temp_dic[categories[i].strip()] = ([], {})
            else:
                temp_dic[categories[i].strip()] = ([[title, author, doi, year,
                                                     citation]], {})
            temp_dic = temp_dic[categories[i].strip()][1]
            i += 1
    return lst


def _combine(dic1: Dict, dic2: Dict) -> None:
    """Combine the individual dictionaries of the list into a single dictionary.
    """
    key = list(dic2.keys())[0]
    val = list(dic2.values())[0]
    if key not in dic1:
        dic1[key] = val
    elif key in dic1 and val[1] == {}:
        dic1[key][0].extend(val[0])
    else:
        _combine(dic1[key][1], dic2[key][1])


def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    file = open(DATA_FILE, 'r')
    lst_file = csv.reader(file)
    data = []
    for line in lst_file:
        if line != '':
            data.append(line)
    data = data[1:]
    lst = _make_list(data, by_year)
    dic = {}
    for item in lst:
        _combine(dic, item)
    file.close()
    return dic


def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    lst = []
    for item in nested_dict:
        if nested_dict[item][1] == {}:
            subtrees = []
            for paper in nested_dict[item][0]:
                tree = PaperTree(paper[PAPER_TITLE_INDEX], [],
                                 paper[PAPER_AUTHOR_INDEX],
                                 paper[PAPER_DOI_INDEX],
                                 int(paper[PAPER_CITATION_INDEX]))
                subtrees.append(tree)
            cat = PaperTree(item, subtrees)
            lst.append(cat)
        else:
            subtrees = []
            for paper in nested_dict[item][0]:
                tree = PaperTree(paper[PAPER_TITLE_INDEX], [],
                                 paper[PAPER_AUTHOR_INDEX],
                                 paper[PAPER_DOI_INDEX],
                                 int(paper[PAPER_CITATION_INDEX]))
                subtrees.append(tree)
            subtrees.extend(_build_tree_from_dict(nested_dict[item][1]))
            cat = PaperTree(item, subtrees)
            lst.append(cat)
    return lst


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
