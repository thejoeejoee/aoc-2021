#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict
from functools import reduce, partial
from itertools import chain

from aocd import get_data

heights = get_data().strip().splitlines()


def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


def compose(*fs):
    return reduce(lambda f, g: lambda x: f(g(x)), fs, lambda x: x)


height = len(heights) + 2
width = len(heights[0]) + 2

EMPTY = type('EMPTY', (int,), dict(__repr__=(f := lambda s: 'EMPTY'), __str__=f))(10)

data = tuple(chain(
    (EMPTY for _ in range(width)),
    *(((EMPTY,) + tuple(int(c) for c in line) + (EMPTY,)) for line in heights),
    (EMPTY for _ in range(width)),
))

risk_level = 0
for triplet_i, triplet in filter(
        compose(partial(operator.ne, EMPTY), itemgetter(1), itemgetter(1)),
        enumerate(windowed(data, 3), start=1)  # wtf dunno why to start at 1
):
    row = triplet_i // width
    col = triplet_i % width
    left, center, right = triplet
    top = data[(row - 1) * width + col]
    bottom = data[(row + 1) * width + col]

    if all(map(partial(operator.lt, center), (left, right, top, bottom))):
        risk_level += center + 1

print(risk_level)
