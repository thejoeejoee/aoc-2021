#!/bin/env python3

import fileinput
from collections import defaultdict
from functools import reduce
from typing import Callable

input_stream = fileinput.input()

State = tuple[int, int, int]

commands: dict[str, Callable[[int, int, int, int], State]] = dict(
    forward=lambda di, de, aim, v: (di + v, de + v * aim, aim),
    down=lambda di, de, aim, v: (di, de, aim + v),
    up=lambda di, de, aim, v: (di, de, aim - v),
)

distance, depth, _ = reduce(
    lambda state, v: commands[v[0]](*state, int(v[1])),
    map(lambda l: l.split(' '), input_stream),
    (0, 0, 0),
)

print(distance * depth)
