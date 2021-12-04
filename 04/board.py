import operator
from dataclasses import dataclass, field
from itertools import repeat, chain, islice, compress
from typing import Iterable, Optional

from more_itertools import windowed

BOARD_SIZE = 5


@dataclass
class Board:
    matrix: tuple[int, ...]
    marks: list[bool, ...] = field(
        default_factory=lambda: list(repeat(False, BOARD_SIZE ** 2))
    )
    last: Optional[int] = field(init=False)

    @classmethod
    def boards_from_input_stream(cls, stream):
        while True:
            try:
                next(stream)
            except StopIteration:
                return
            yield cls.from_input_lines(islice(stream, BOARD_SIZE))

    @classmethod
    def from_input_lines(cls, lines: Iterable[str]):
        return cls(tuple(int(v) for line in lines for v in line.strip().split()))

    def draw(self, value):
        self.last = value
        try:
            idx = self.matrix.index(value)
        except ValueError:
            return
        self.marks[idx] = True

    @property
    def score(self):
        return self.last * sum(compress(self.matrix, map(operator.not_, self.marks)))

    @property
    def is_finished(self):
        windows = (
            *windowed(self.marks, n=BOARD_SIZE, step=BOARD_SIZE),
            *windowed(self.marks_transposed, n=BOARD_SIZE, step=BOARD_SIZE),
        )
        return (True,) * BOARD_SIZE in windows

    @property
    def marks_transposed(self):
        return tuple(
            chain.from_iterable(self.marks[i::BOARD_SIZE] for i in range(BOARD_SIZE))
        )

    def __str__(self):
        return '\n'.join(
            ' '.join(f'{m: 3}{"." if v else " "}' for m, v in zip(
                self.matrix[i * BOARD_SIZE:(i + 1) * BOARD_SIZE],
                self.marks[i * BOARD_SIZE:(i + 1) * BOARD_SIZE],
            ))
            for i in range(BOARD_SIZE)
        )

    def __hash__(self):
        return hash(
            tuple(self.matrix),
        )