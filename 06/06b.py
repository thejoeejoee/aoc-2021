#!/bin/env python3

import fileinput
from collections import Counter

from aocd import get_data

generation = Counter(map(int, get_data().strip().split(',')))

DAYS = 256

for _ in range(DAYS):
    # well, list would be enough (especially with pop() shifting)
    # hindsight is 20/20 ¯\_(ツ)_/¯
    new_generation = Counter()

    for i in range(1, 9):
        in_i_generation = generation.get(i, 0)

        new_generation.update({i - 1: in_i_generation})

    ready_to_spawn = generation.get(0, 0)

    new_generation.update({6: ready_to_spawn})
    new_generation.update({8: ready_to_spawn})

    generation = new_generation

print(sum(generation.values()))
