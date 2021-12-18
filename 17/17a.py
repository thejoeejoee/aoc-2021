#!/bin/env python3
import re
from dataclasses import dataclass
from itertools import product
from operator import attrgetter
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


STARTING_POINT = Point(0, 0)

SPEC_RE = re.compile(r'x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')


def is_throw_great(
        throw: Throw,
        target_box: Box,
        position_notifier: Callable[[Point, Throw], None] = lambda *x: None
) -> bool:
    pos = STARTING_POINT

    position_notifier(pos, throw)

    while pos.y >= target_box.end.y:
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


def is_throw_horizontally_converging(
        throw: Throw,
        target_box: Box
) -> bool:
    pos = STARTING_POINT

    while throw.x:
        pos = pos + throw

        if pos.x >= target_box.end.x:
            # is over
            raise ThrowIsOver

        throw = Throw(
            max(throw.x - 1, 0),
            throw.y - 1
        )

    return target_box.start.x <= pos.x <= target_box.end.x


def find_suitable_horizontal_speeds(target_box: Box, x_speed_range: range):
    for x_speed in x_speed_range:
        try:
            is_ok = is_throw_horizontally_converging(
                Throw(x_speed, 0),
                target_box
            )
        except ThrowIsOver:
            return

        if not is_ok:
            continue
        yield x_speed


def main(spec: str):
    match = SPEC_RE.match(spec[13:])
    x1, x2 = sorted(map(int, match.groups()[0:2]))
    y1, y2 = sorted(map(int, match.groups()[2:4]))
    target_box = Box(
        Point(x1, y1),
        Point(x2, y2),
    )

    horizontal_speeds = tuple(find_suitable_horizontal_speeds(
        target_box=target_box,
        x_speed_range=range(-x2, x2)
    ))

    max_points = set()
    for x_speed, y_speed in product(
            horizontal_speeds,
            range(-abs(y2), abs(y2) * 10)
    ):
        t = Throw(x_speed, y_speed)
        positions: list[Point] = list()

        is_fine = is_throw_great(
            t,
            target_box,
            position_notifier=lambda p, _: positions.append(p)
        )
        if not is_fine:
            continue

        max_points.add(max(map(attrgetter('y'), positions)))
        # pprint(positions)
    return max(max_points)


if __name__ == '__main__':
    spec = get_data().strip().splitlines()[0]

    # spec = "target area: x=20..30, y=-10..-5"
    print(main(spec))
