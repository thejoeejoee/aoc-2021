#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict
from functools import reduce, partial
from itertools import chain

from aocd import get_data

lines = get_data().strip().splitlines()

BRACES = {
    '(': ')',
    '{': '}',
    '<': '>',
    '[': ']',
}

SCORES = {
    ')': 3,
    '}': 1197,
    '>': 25137,
    ']': 57,
}


def compute_score(line) -> int:
    stack = []

    for c in line:
        if c in BRACES.keys():
            stack.append(c)
            continue

        if not stack:
            return 0

        last = stack[-1]
        expected = BRACES[last]

        if expected == c:
            stack.pop()
            continue

        return SCORES[c]
    return 0


def main():
    return sum(map(compute_score, lines))


if __name__ == '__main__':
    print(main())
