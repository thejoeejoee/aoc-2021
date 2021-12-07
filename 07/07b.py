#!/bin/env python3

from _operator import attrgetter, itemgetter
from collections import defaultdict

from aocd import get_data

levels = tuple(map(int, get_data().strip().split(',')))
last_prices = [1 for _ in range(len(levels))]

possible_aligns = defaultdict(int)

for tested in range(min(levels), max(levels) + 1):
    for i, crab in enumerate(levels):
        move_length = abs(crab - tested)
        price = move_length * (1 + move_length) / 2

        possible_aligns[tested] += price
    # eeehe, mean?

print(min(
    possible_aligns.items(),
    key=itemgetter(1)
))
