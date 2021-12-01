#!/bin/env python3

import fileinput

input_stream = fileinput.input()

levels = tuple(map(int, input_stream))

def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


measurement_stream = windowed(levels, 3)

out = 0
last = None
for levels in measurement_stream:
    together = sum(levels)
    if last and together > last:
        out += 1
    last = together

print(out)