#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict
from functools import partial
from itertools import filterfalse

from aocd import get_data

measures = get_data().splitlines()


def decode(parts: list[str]) -> int:
    parts.pop(10)
    lengths = tuple(map(len, parts))
    parts = tuple(map(set, parts))

    one = parts[lengths.index(2)]
    seven = parts[lengths.index(3)]
    # top segment is basically 7 - 1 (segments related)
    top = (seven - one).pop()

    four = parts[lengths.index(4)]
    # almost_nine is 4 + top segment
    almost_nine: set[str] = four | {top}

    six_lengths = tuple(filter(lambda p: len(p) == 6, parts))
    nine = next(filter(almost_nine.issubset, six_lengths))
    six_or_zeros = tuple(filter(
        partial(operator.ne, nine),
        six_lengths
    ))
    six = next(filter(lambda p: (nine - p) & one, six_or_zeros))

    zero = next(filter(
        partial(operator.ne, six),
        six_or_zeros
    ))

    center = (nine - zero).pop()
    bottom = (nine - almost_nine).pop()

    three = seven | {center, bottom}
    eight = zero | {center}

    two_or_fives = tuple(filter(
        lambda p: len(p) == 5 and p != three,
        parts
    ))

    bottom_right = (six & one).pop()

    five = next(filter(
        partial(operator.and_, {bottom_right}),
        two_or_fives
    ))
    two = next(filter(
        partial(operator.ne, five),
        two_or_fives
    ))
    mapping = tuple(map(
        frozenset,
        (zero, one, two, three, four, five, six, seven, eight, nine)
    ))
    return int(''.join(map(
        str,
        (mapping.index(v) for v in parts[10:])
    )))


print(sum(
    decode(parts=line.strip().split())
    for line in get_data().splitlines()
))
