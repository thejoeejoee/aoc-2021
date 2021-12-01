#!/bin/env python3

import fileinput

input_stream = fileinput.input()

last = int(next(input_stream))

out = 0
for level in map(int, input_stream):
    if level > last:
        out += 1
    last = level

print(out)