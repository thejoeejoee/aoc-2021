#!/bin/env python3
import operator
from dataclasses import dataclass
from functools import partial, reduce
from itertools import product
from operator import attrgetter
from typing import NamedTuple

from aocd import get_data


class Pixel(NamedTuple):
    x: int
    y: int


@dataclass(frozen=True)
class Image:
    data: frozenset[Pixel]
    infinite: str = '.'

    def __post_init__(self):
        for what, how in product(('x', 'y'), (min, max)):
            object.__setattr__(
                self,
                f'{what}_{how.__name__}',
                how(map(attrgetter(what), self.data))
            )

    def is_pixel_on(self, pixel: Pixel) -> bool:
        return (pixel in self.data) if (
                self.x_min <= pixel.x <= self.x_max and
                self.y_min <= pixel.y <= self.y_max
        ) else (self.infinite == '#')

    def algorithm_step(self, code: str) -> 'Image':
        return Image(
            data=frozenset(filter(
                compose(
                    partial(operator.eq, '#'),
                    code.__getitem__,
                    self.get_code_index_for_pixel
                ),
                map(
                    pixel_from_tuple,
                    product(
                        range(self.x_min - 1, self.x_max + 2),
                        range(self.y_min - 1, self.y_max + 2)
                    )
                )
            )),
            infinite=code[0 if self.infinite == '.' else -1]
        )

    def get_code_index_for_pixel(self, pixel: Pixel) -> int:
        return int(''.join(
            ('0', '1')[self.is_pixel_on(Pixel(x, y))]
            for x, y in (
                (pixel.x - 1, pixel.y - 1),
                (pixel.x, pixel.y - 1),
                (pixel.x + 1, pixel.y - 1),
                (pixel.x - 1, pixel.y),
                (pixel.x, pixel.y),
                (pixel.x + 1, pixel.y),
                (pixel.x - 1, pixel.y + 1),
                (pixel.x, pixel.y + 1),
                (pixel.x + 1, pixel.y + 1),
            )
        ), base=2)


pixel_from_tuple = lambda t: Pixel(*t)


def compose(*fs):
    return reduce(lambda f, g: lambda *x: f(g(*x)), fs, lambda x: x)


def print_image(image: Image):
    for y in range(image.y_min - 1, image.y_max + 1 + 1):
        print(''.join(
            ('.', '#')[Pixel(x, y) in image.data] for x in range(image.x_min - 1, image.x_max + 1 + 1)
        ))


def main(lines: list[str]) -> int:
    lines_iterator = iter(lines)
    code = ''.join(iter(partial(next, lines_iterator), ''))

    assert len(code) == 2 ** 9

    image_lines = tuple(iter(partial(next, lines_iterator), ''))

    image = Image(frozenset({
        Pixel(x, y)
        for y, line in enumerate(image_lines)
        for x, c in enumerate(line)
        if c == '#'
    }))

    return len(
        reduce(
            lambda i, _: i.algorithm_step(code=code),
            range(50),
            image
        ).data
    )


if __name__ == '__main__':
    lines = get_data(day=20).strip().splitlines()

    print(main(lines))
