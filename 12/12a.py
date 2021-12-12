#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict
from functools import reduce, partial
from itertools import chain

from aocd import get_data


class G:
    def __init__(self):
        self._g = defaultdict(set)

    def add_edge(self, e):
        for v1, v2 in (e, e[::-1]):
            self._g[v1].add(v2)

    def adjacencies(self, v):
        return self._g[v]

    def __str__(self):
        return ', '.join('-'.join((v1, v2)) for v1 in self._g for v2 in self._g[v1])


START = 'start'
END = 'end'

is_big = str.isupper


def main(lines):
    g = G()

    for line in lines:
        g.add_edge(line.split('-'))

    def go(from_: str, known: tuple):
        # print(f'On {from_}, {known=}')
        known = known + (from_,)

        if from_ == END:
            return known,

        possible = list()
        adjacency = g.adjacencies(from_)

        for v in (adjacency - set(known)) | set(filter(is_big, adjacency)):

            if path := go(v, known=known):
                possible.extend(path)

        return possible

    paths = go(START, ())
    # for pth in paths:
    #     print(','.join(pth))
    return len(paths)


if __name__ == '__main__':
    print(main(lines=get_data().strip().splitlines()))
