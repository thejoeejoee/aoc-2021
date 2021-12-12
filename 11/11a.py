#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict
from functools import reduce, partial, cache
from itertools import chain
from typing import Generator, Callable

from aocd import get_data
from aocd.get import get_day_and_year


def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


def compose(*fs):
    return reduce(lambda f, g: lambda x: f(g(x)), fs, lambda x: x)


inc_by_one: Callable[[int], int] = partial(operator.add, 1)


def find_flashing(state: list[int]) -> Generator[int, None, None]:
    i = -1
    while True:
        try:
            yield (i := state.index(10, i + 1))
        except ValueError:
            return


def get_neighbors(i, width, height):
    top = (i // width) == 0
    bottom = (i // width) == height - 1
    left = (i % width) == 0
    right = (i % width) == width - 1

    yield from filter(
        partial(operator.ne, None),
        (
            (i + 1) if not right else None,
            (i - 1) if not left else None,
            (i + width) if not bottom else None,
            (i - width) if not top else None,
            (i + width + 1) if not (bottom or right) else None,
            (i + width - 1) if not (bottom or left) else None,
            (i - width + 1) if not (top or right) else None,
            (i - width - 1) if not (top or left) else None,
        )
    )


def print_state(state):
    print('\n'.join(
        ''.join(map(str, state[i * 10:(i + 1) * 10])) for i in range(10)
    ))


def main(lines):
    height = len(lines)
    width = len(lines[0])

    state = tuple(chain.from_iterable(tuple(map(int, line)) for line in lines))

    total = 0
    for _ in range(100):
        flashed = set()

        state = list(map(inc_by_one, state))

        while 10 in state:
            for flashing_i in find_flashing(state=state):
                if flashing_i in flashed:
                    continue

                flashed.add(flashing_i)
                state[flashing_i] = 0

                neighbors = tuple(get_neighbors(flashing_i, width, height))

                for neighbor in neighbors:
                    if neighbor in flashed:
                        continue

                    state[neighbor] = min(10, state[neighbor] + 1)

        total += len(flashed)
    return total


if __name__ == '__main__':
    d, y = get_day_and_year()
    lines = get_data(day=d, year=y).strip().splitlines()
    print(main(lines=lines))
