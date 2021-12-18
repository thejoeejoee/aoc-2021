#!/bin/env python3
import re
from dataclasses import dataclass
from functools import partial
from itertools import product
from typing import Callable

from aocd import get_data


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, (self.__class__, Throw)):
            return self.__class__(
                self.x + other.x,
                self.y + other.y,
            )

        raise TypeError(f'Cannot add point to {other}')


@dataclass(frozen=True)
class Throw:
    x: int
    y: int


@dataclass(frozen=True)
class Box:
    start: Point
    end: Point

    def __contains__(self, item):
        if isinstance(item, Point):
            return (
                    self.start.x <= item.x <= self.end.x
                    and
                    self.start.y <= item.y <= self.end.y
            )

    def __post_init__(self):
        assert self.start.x < self.end.x
        assert self.start.y < self.end.y


STARTING_POINT = Point(0, 0)

SPEC_RE = re.compile(r'x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')


def is_throw_great(
        throw: Throw,
        target_box: Box,
        position_notifier: Callable[[Point, Throw], None] = lambda *x: None
) -> bool:
    pos = STARTING_POINT

    position_notifier(pos, throw)

    lowest_y = min(target_box.start.y, target_box.end.y)

    while pos.y >= lowest_y:
        pos = pos + throw

        position_notifier(pos, throw)

        if pos in target_box:
            return True

        throw = Throw(
            max(throw.x - 1, 0),
            throw.y - 1
        )

    return False


class ThrowIsOver(StopIteration):
    pass


def does_throw_hits_target_vertical_strip(
        throw: Throw,
        target_box: Box
) -> bool:
    pos = STARTING_POINT

    while throw.x:
        pos = pos + throw

        throw = Throw(
            max(throw.x - 1, 0),
            throw.y - 1
        )

        if target_box.start.x <= pos.x <= target_box.end.x:
            return True


def find_suitable_horizontal_speeds(target_box: Box, x_speed_range: range):
    for x_speed in x_speed_range:
        is_ok = does_throw_hits_target_vertical_strip(
            Throw(x_speed, 0),
            target_box
        )

        if not is_ok:
            continue

        yield x_speed


def load_target_box(spec: str) -> Box:
    match = SPEC_RE.match(spec[13:])
    x1, x2 = sorted(map(int, match.groups()[0:2]))
    y1, y2 = sorted(map(int, match.groups()[2:4]))
    return Box(
        Point(x1, y1),
        Point(x2, y2),
    )


def main(target_box: Box):
    horizontal_speeds = tuple(find_suitable_horizontal_speeds(
        target_box=target_box,
        x_speed_range=range(0, target_box.end.x * 5)
    ))

    assert target_box.start.x >= 0

    def is_possible(t: Throw, box: Box) -> bool:
        lowest = min(box.start.y, box.end.y)
        leftest = min(box.start.x, box.end.x)
        rightest = max(box.start.x, box.end.x)

        p = Point(rightest, lowest) if lowest > 0 else Point(leftest, lowest)

        dx = p.x
        ratio = t.y / t.x

        return (dx * ratio) >= p.y

    possible_throws = set()
    all_possible = map(
        lambda t: Throw(*t),
        product(
            horizontal_speeds,
            range(-5 * abs(target_box.end.y), abs(target_box.end.y) * 5)
        )
    )
    for t in filter(partial(is_possible, box=target_box), all_possible):
        is_fine = is_throw_great(
            t,
            target_box
        )
        if not is_fine:
            continue

        possible_throws.add(t)

        # pprint(positions)
    return possible_throws


if __name__ == '__main__':
    spec = get_data().strip().splitlines()[0]

    target = load_target_box(spec)

    # target = load_target_box("target area: x=20..30, y=-10..-5")

    computed = main(target)
    print(len(computed))

    exit()

    target = load_target_box("target area: x=20..30, y=-10..-5")
    tests = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7""".replace('\n', ' ').strip().split(' ')

    throws = set(Throw(*map(int, t.strip().split(','))) for t in filter(None, tests))
    assert throws == computed

    for throw in throws:
        positions = []
        is_ok = is_throw_great(
            throw,
            target,
            position_notifier=lambda p, _: positions.append(p)
        )
        assert is_ok, f'{throw} goes to target.'
