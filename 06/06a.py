#!/bin/env python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import product

from aocd import get_data

input_stream = map(int, get_data().strip().split(','))

generation = list(input_stream)

DAYS = 80

for _ in range(DAYS):

    for i, fish in enumerate(generation[:]):

        if fish == 0:
            generation[i] = 6
            generation.append(8)
        else:
            generation[i] -= 1

print(len(generation))



