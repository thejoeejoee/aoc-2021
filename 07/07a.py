#!/bin/env python3
from _operator import attrgetter, itemgetter
from collections import defaultdict

from aocd import get_data

get_data()

levels = tuple(map(int, get_data().strip().split(',')))

possible_aligns = defaultdict(int)

for tested in range(min(levels), max(levels) + 1):
    # median, innit?
    possible_aligns[tested] = sum(abs(l - tested) for l in levels)

print(min(
    possible_aligns.items(),
    key=itemgetter(1)
))