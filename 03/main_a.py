#!/bin/env python3

import fileinput
from collections import defaultdict

input_stream = fileinput.input()

first_line = next(input_stream).strip()

mapping = {'1': 1, '0': -1}

values = list(map(mapping.__getitem__, first_line))

for line in input_stream:
    for i, new in enumerate(line.strip()):
        values[i] += mapping[new]


gamma = [i > 0 for i in values]
epsilon = [i < 0 for i in values]

print(
    int(f'{"".join(map(str, map(int, gamma)))}', base=2) *
    int(f'{"".join(map(str, map(int, epsilon)))}', base=2)
)