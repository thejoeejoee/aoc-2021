#!/bin/env python3
import operator
from operator import attrgetter, itemgetter
from collections import defaultdict, Counter
from functools import reduce, partial
from itertools import chain
from pprint import pprint

from aocd import get_data


def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


def main(lines: list[str]):
    loader = iter(lines)
    word = list(next(loader))

    rules = {
        line[0:2]: line[6]
        for line in lines[2:]
    }

    for _ in range(10):
        inserts = []
        for i, w in enumerate(windowed(word[:], 2)):
            inserts.append((i + 1, rules.get(''.join(w)) or ''))

        for i, what in inserts[::-1]:
            word.insert(i, what)

    c = Counter(word)
    return max(c.values()) - min(c.values())


if __name__ == '__main__':
    print(main(lines=get_data(day=14).strip().splitlines()))
