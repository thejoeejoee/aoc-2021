#!/bin/env python3
import operator
from functools import reduce, partial, cache
from itertools import chain
from queue import PriorityQueue
from typing import Generator

from aocd import get_data


def compose(*fs):
    return reduce(lambda f, g: lambda x: f(g(x)), fs, lambda x: x)


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
        )
    )

@cache
def heuristic(i1, i2, width, height) -> float:
    (x1, y1) = divmod(i1, width)
    (x2, y2) = divmod(i2, width)
    return abs(x1 - x2) + abs(y1 - y2)

def main(data):
    height = len(data)
    width = len(data[0])
    START = 0
    END = width * height - 1
    terrain = tuple(chain.from_iterable(tuple(map(int, line)) for line in data))

    get_neighbors_ = partial(get_neighbors, width=width, height=height)
    heuristic_ = partial(heuristic, width=width, height=height)

    paths = dict()
    prices = dict()

    @cache
    def go(path: tuple[int, ...], price: int) -> Generator[tuple, None, None]:
        from_ = path[-1]
        paths[from_] = path
        prices[from_] = price

        for n in get_neighbors_(from_):
            n_price = price + terrain[n]
            n_path = path + (n,)

            known_price = prices.get(n)

            if known_price and known_price <= n_price:
                continue

            priority = n_price + 4 * heuristic_(n, END)
            yield (priority, (n_path, n_price))

    q = PriorityQueue()
    q.put((0, ((START, ), 0)))

    while not q.empty():
        _, args = q.get()

        for i in go(*args):
            q.put(i)

    print('\n'.join(
        ''.join(map(
            str,
            map(
                lambda t, r: '■' if i*width+r in paths[END] else t,
                terrain[i * width:(i + 1) * width],
                range(width),
            )
        )) for i in range(height)
    ))

    return prices[END]


if __name__ == '__main__':
    lines_ = get_data().strip().splitlines()
    lines__ = """
    1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
    """.strip().splitlines()
    print(main(data=lines_))
