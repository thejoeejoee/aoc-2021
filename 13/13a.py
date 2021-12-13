#!/bin/env python3
import operator
from operator import attrgetter, itemgetter
from collections import defaultdict
from functools import reduce, partial
from itertools import chain
from pprint import pprint

from aocd import get_data


def fold(data: set[tuple[int, int]], fold: tuple[str, int]) -> set[tuple[int, int]]:
    fold_axis, fold_value = fold

    def fld(*_):
        raise ValueError

    if fold_axis == 'x':
        def fld(p: tuple[int, int]) -> tuple[int, int]:
            x, y = p
            if x < fold_value:
                return p
            return fold_value - (x - fold_value), y

    elif fold_axis == 'y':
        def fld(p: tuple[int, int]) -> tuple[int, int]:
            x, y = p
            if y < fold_value:
                return p
            return x, fold_value - (y - fold_value)

    return set(map(fld, data))


def main(lines: list[str]):
    loader = partial(next, iter(lines))

    data = {
        (*map(int, line.split(',')),)
        for line in iter(loader, '')
    }
    folds = tuple(map(
        lambda t: (t[0], int(t[1])),
        (line[11:].split('=')
         for line in iter(loader, ''))
    ))

    return len(fold(data, folds[0]))


if __name__ == '__main__':
    print(main(lines=get_data().strip().splitlines()))
