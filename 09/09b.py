#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict, Counter
from functools import reduce, partial
from itertools import chain

from aocd import get_data

EMPTY = type('EMPTY', (int,), dict(__repr__=(f := lambda s: 'EMPTY'), __str__=f))(10)


def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


def compose(*fs):
    return reduce(lambda f, g: lambda x: f(g(x)), fs, lambda x: x)


heights = get_data().strip().splitlines()

HEIGHT = len(heights) + 2
WIDTH = len(heights[0]) + 2


def get_neighbors(data, pos):
    row, col = pos
    for p in (
            (row, col + 1),
            (row, col - 1),
            (row + 1, col),
            (row - 1, col),
    ):
        r, c = p
        if 0 <= r < HEIGHT and 0 <= c < WIDTH:
            yield p, data[r * WIDTH + c]


def find_low_points(levels):
    for triplet_i, triplet in filter(
            # turbo magic to get triples (with indexes) with center item which is NOT EMPTY
            compose(partial(operator.ne, EMPTY), itemgetter(1), itemgetter(1)),
            enumerate(windowed(levels, 3), start=1)  # wtf dunno why to start at 1
    ):
        row = triplet_i // WIDTH
        col = triplet_i % WIDTH
        left, center, right = triplet
        top = levels[(row - 1) * WIDTH + col]
        bottom = levels[(row + 1) * WIDTH + col]

        if all(map(partial(operator.lt, center), (left, right, top, bottom))):
            yield row, col


def main():
    data = tuple(chain(
        (EMPTY for _ in range(WIDTH)),
        *(((EMPTY,) + tuple(int(c) for c in line) + (EMPTY,)) for line in heights),
        (EMPTY for _ in range(WIDTH)),
    ))

    basins = Counter()

    for low_point in find_low_points(data):
        known = set()
        to_explore = {low_point}
        # not BFS, dot DFS? just JoeFS
        while to_explore:
            exploring = to_explore.pop()
            known.add(exploring)

            r, c = exploring
            current = data[r * WIDTH + c]

            for neighbor, level in get_neighbors(data, exploring):
                if level in known:
                    continue

                if level > current and level not in (EMPTY, 9):
                    to_explore.add(neighbor)

        basins[low_point] = len(known)

    return reduce(
        operator.mul,
        map(itemgetter(1), basins.most_common(3))
    )


if __name__ == '__main__':
    print(main())
