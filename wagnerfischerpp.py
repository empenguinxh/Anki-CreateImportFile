#!/usr/bin/env python
#
# Copyright (c) 2013-2014 Kyle Gorman
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# wagnerfischerpp.py: efficient computation of Levenshtein distance and
# all optimal alignments with arbitrary edit costs. The algorithm for
# computing the dynamic programming table used has been discovered many
# times, but most notably by Wagner & Fischer:
#
# R.A. Wagner & M.J. Fischer. 1974. The string-to-string correction
# problem. Journal of the ACM, 21(1): 168-173.
#
# Wagner & Fischer also describe an algorithm ("Algorithm Y") to find the
# alignment path (i.e., list of edit operations involved in the optimal
# alignment), but it it is specified such that in fact it only generates
# one such path, whereas many such paths may exist, particularly when
# multiple edit operations have the same cost. For example, when all edit
# operations have the same cost, there are two equal-cost alignments of
# "TGAC" and "GCAC":
#
#     TGAC     TGxAC
#     ss==     d=i==
#     GCAC     xGCAC
#
# However, all such paths can be generated efficiently, as follows. First,
# the dynamic programming table "cells" are defined as tuples of (partial
# cost, set of all operations reaching this cell with minimal cost). As a
# result, the completed table can be thought of as an unweighted, directed
# graph (or FSA). The bottom right cell (the one containing the Levenshtein
# distance) is the start state and the origin as end state. The set of arcs
# are the set of operations in each cell as arcs. (Many of the cells of the
# table, those which are not visited by any optimal alignment, are under
# the graph interpretation unconnected vertices, and can be ignored. Every
# path between the bottom right cell and the origin cell is an optimal
# alignment. These paths can be efficiently enumerated using breadth-first
# traversal. The trick here is that elements in deque must not only contain
# indices but also partial paths. Averaging over all such paths, we can
# come up with an estimate of the number of insertions, deletions, and
# substitutions involved as well; in the example above, we say S = 1 and
# D, I = 0.5.

from __future__ import division

from pprint import PrettyPrinter
from collections import deque, namedtuple, Counter

# default costs

INSERTION = 1
DELETION = 1
SUBSTITUTION = 1

Trace = namedtuple("Trace", ["cost", "ops"])


class WagnerFischer(object):

    """
    An object representing a (set of) Levenshtein alignments between two
    iterable objects (they need not be strings). The cost of the optimal
    alignment is scored in `self.cost`, and all Levenshtein alignments can
    be generated using self.alignments()`.

    Basic tests:

    >>> WagnerFischer("god", "gawd").cost
    2
    >>> WagnerFischer("sitting", "kitten").cost
    3
    >>> WagnerFischer("bana", "banananana").cost
    6
    >>> WagnerFischer("bana", "bana").cost
    0
    >>> WagnerFischer("banana", "angioplastical").cost
    11
    >>> WagnerFischer("angioplastical", "banana").cost
    11
    >>> WagnerFischer("Saturday", "Sunday").cost
    3

    IDS tests:

    >>> WagnerFischer("doytauvab", "doyvautab").IDS() == {"S": 2.0}
    True
    >>> WagnerFischer("kitten", "sitting").IDS() == {"I": 1.0, "S": 2.0}
    True
    """

    # initialize pretty printer (shared across all class instances)
    pprint = PrettyPrinter(width=75)

    def __init__(self, A, B, insertion=INSERTION, deletion=DELETION,
                 substitution=SUBSTITUTION):
        # score operation costs in a dictionary, for programmatic access
        self.costs = {"I": insertion, "D": deletion, "S": substitution}
        # initialize table
        self.asz = len(A)
        self.bsz = len(B)
        self._table = [[None for _ in xrange(self.bsz + 1)] for
                       _ in xrange(self.asz + 1)]
        # from now on, all indexing done using self.__getitem__
        ## fill in edges
        self[0][0] = Trace(0, {"O"})  # start cell
        for i in xrange(1, self.asz + 1):
            self[i][0] = Trace(i * self.costs["D"], {"D"})
        for j in xrange(1, self.bsz + 1):
            self[0][j] = Trace(j * self.costs["I"], {"I"})
        ## fill in rest
        for i in xrange(len(A)):
            for j in xrange(len(B)):
                # clean it up in case there are more than one
                # check for match first, always cheapest option
                if A[i] == B[j]:
                    self[i + 1][j + 1] = Trace(self[i][j].cost, {"M"})
                # check for other types
                else:
                    costI = self[i + 1][j].cost + self.costs["I"]
                    costD = self[i][j + 1].cost + self.costs["D"]
                    costS = self[i][j].cost + self.costs["S"]
                    # determine min of three
                    min_val = min(costI, costD, costS)
                    # write that much in
                    trace = Trace(min_val, set())
                    # add _all_ operations matching minimum value
                    if costI == min_val:
                        trace.ops.add("I")
                    if costD == min_val:
                        trace.ops.add("D")
                    if costS == min_val:
                        trace.ops.add("S")
                    # write to table
                    self[i + 1][j + 1] = trace
        # store optimum cost as a property
        self.cost = self[-1][-1].cost

    def __repr__(self):
        return self.pprint.pformat(self._table)

    def __iter__(self):
        for row in self._table:
            yield row

    def __getitem__(self, i):
        """
        Returns the i-th row of the table, which is a list and so 
        can be indexed. Therefore, e.g.,  self[2][3] == self._table[2][3]
        """
        return self._table[i]

    # stuff for generating alignments

    def _stepback(self, i, j, trace, path_back):
        """
        Given a cell location (i, j) and a Trace object trace, generate
        all traces they point back to in the table
        """
        for op in trace.ops:
            if op == "M":
                yield i - 1, j - 1, self[i - 1][j - 1], path_back + ["M"]
            elif op == "I":
                yield i, j - 1, self[i][j - 1], path_back + ["I"]
            elif op == "D":
                yield i - 1, j, self[i - 1][j], path_back + ["D"]
            elif op == "S":
                yield i - 1, j - 1, self[i - 1][j - 1], path_back + ["S"]
            elif op == "O":
                return  # origin cell, we"re done iterating
            else:
                raise ValueError("Unknown op '{}'".format(op))

    def alignments(self, bfirst=False):
        """
        Generate all alignments with optimal cost by traversing the
        an implicit graph on the dynamic programming table. By default,
        depth-first traversal is used, since users seem to get tired
        waiting for their first results.
        """
        # each cell of the queue is a tuple of (i, j, trace, path_back)
        # where i, j is the current index, trace is the trace object at
        # this cell
        if bfirst:
            return self._bfirst_alignments()
        else:
            return self._dfirst_alignments()

    def _dfirst_alignments(self):
        """
        Generate alignments via depth-first traversal.
        """
        stack = list(self._stepback(self.asz, self.bsz, self[-1][-1], []))
        while stack:
            (i, j, trace, path_back) = stack.pop()
            if trace.ops == {"O"}:
                path_back.reverse()
                yield path_back
                continue
            stack.extend(self._stepback(i, j, trace, path_back))

    def _bfirst_alignments(self):
        """
        Generate alignments via breadth-first traversal.
        """
        queue = deque(self._stepback(self.asz, self.bsz, self[-1][-1], []))
        while queue:
            (i, j, trace, path_back) = queue.popleft()
            if trace.ops == {"O"}:
                path_back.reverse()
                yield path_back
                continue
            queue.extend(self._stepback(i, j, trace, path_back))

    def IDS(self):
        """
        Estimate insertions, deletions, and substitution _count_ (not 
        costs). Non-integer values arise when there are multiple possible
        alignments with the same cost.
        """
        npaths = 0
        opcounts = Counter()
        for alignment in self.alignments():
            # count edit types for this path, ignoring "M" (which is free)
            opcounts += Counter(op for op in alignment if op != "M")
            npaths += 1
        # average over all paths
        return Counter({o: c / npaths for (o, c) in opcounts.iteritems()})


if __name__ == "__main__":
    import doctest
    doctest.testmod()