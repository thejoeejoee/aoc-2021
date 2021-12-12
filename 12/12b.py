#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict, Counter
from functools import reduce, partial, cache
from itertools import chain, filterfalse

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


@cache
def can_go(known: tuple[str], to: str) -> bool:
    if to == START:
        return False

    if to == END:
        return True

    if to.isupper():
        return True

    c = Counter(filterfalse(is_big, known))
    most_common, most_common_count = c.most_common()[0]

    if most_common_count == 2 and c[to] == 0:
        return True
    elif most_common_count == 1:
        return True

    return False


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
        adjacencies = g.adjacencies(from_)

        for v in filter(partial(can_go, known), adjacencies):
            if path := go(v, known=known):
                possible.extend(path)

        return possible

    paths = go(START, ())
    # for pth in paths:
    #     print(','.join(pth))
    return len(paths)


if __name__ == '__main__':
    lines = """
    start-A
start-b
A-c
A-b
b-d
A-end
b-end""".strip().splitlines()
    # print(main(lines=lines))#get_data().strip().splitlines()))
    print(main(lines=get_data().strip().splitlines()))
