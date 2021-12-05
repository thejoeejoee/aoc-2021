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

    if not (x1 == x2 or y1 == y2):
        continue

    x_line = range(min(x1, x2), max(x1, x2) + 1)
    y_line = range(min(y1, y2), max(y1, y2) + 1)
    for x, y in product(x_line, y_line):
        c.update({(x, y): 1})

print(len(tuple(filter(
    lambda t: t[1] >= 2,
    c.items()
))))
