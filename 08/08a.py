#!/bin/env python3

from _operator import attrgetter, itemgetter
from collections import defaultdict

from aocd import get_data

measures = get_data().splitlines()

total = 0

for line in get_data().splitlines():
    measures = line.strip().split()

    first, second = measures[:10], measures[11:]

    lengths = tuple(map(len, second))

    total += lengths.count(2) + lengths.count(4) + lengths.count(3) + lengths.count(7)

print(total)
