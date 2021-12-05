#!/bin/env python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import product

input_stream = fileinput.input()

c = Counter()

RE_SPLITTER = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')

for line in input_stream:
    x1, y1, x2, y2 = map(int, RE_SPLITTER.match(line).groups())

    x_up = x1 < x2
    y_up = y1 < y2

    x_line = range(x1, x2 + (1 if x_up else -1), 1 if x_up else -1)
    y_line = range(y1, y2 + (1 if y_up else -1), 1 if y_up else -1)

    f = product if x1 == x2 or y1 == y2 else zip

    for x, y in f(x_line, y_line):
        c.update({(x, y): 1})

print(len(tuple(filter(
    lambda t: t[1] >= 2,
    c.items()
))))
