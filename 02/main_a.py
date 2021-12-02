#!/bin/env python3

import fileinput
from collections import defaultdict

input_stream = fileinput.input()

commands = defaultdict(int)

for line in input_stream:
    cmd, value = line.split(' ')
    commands[cmd] += int(value)

print(commands['forward'] * (commands['down'] - commands['up']))