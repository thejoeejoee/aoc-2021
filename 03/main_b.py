#!/bin/env python3

import fileinput
from collections import defaultdict, Counter
from operator import itemgetter
from typing import Iterable, Sequence, Callable

input_stream = fileinput.input()

data = list(map(str.strip, input_stream))


def find_data(values: Sequence[str], index: int, cmp: Callable) -> str:
    if len(values) == 1:
        return values[0]

    c = Counter(map(lambda v: v[index], values))
    to_filter, _ = cmp(
        c.items(),
        key=lambda t: (t[1], t[0])
    )

    filtered = tuple(filter(
        lambda line: line[index] == to_filter,
        values
    ))
    return find_data(filtered, index=index + 1, cmp=cmp)


print(
    int(find_data(data, 0, max), base=2) *
    int(find_data(data, 0, min), base=2)
)
