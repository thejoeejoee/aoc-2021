#!/bin/env python3
from collections import Counter

from aocd import get_data


def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


def main(lines: list[str]):
    loader = iter(lines)
    word = Counter(windowed(initial := next(loader), 2))
    ends = {initial[0], initial[-1]}

    rules = {
        line[0:2]: line[6]
        for line in lines[2:]
    }

    for _ in range(40):
        for pair, count in tuple(word.items()):
            if not count:
                continue
            if not (to_insert := rules.get(pair)):
                continue

            left, right = pair
            # cannot be merged since it could contain duplicities
            word.update({pair: -1 * count})
            word.update({f'{left}{to_insert}': 1 * count})
            word.update({f'{to_insert}{right}': 1 * count})

    c = Counter(ends)
    for pair, count in word.items():
        c.update({pair[0]: count})
        c.update({pair[1]: count})

    def correct(v: int) -> int:
        if v == 1:
            return 1
        elif v % 2 == 0:
            return v // 2
        raise ValueError('Should not happen')

    counts = tuple(map(correct, c.values()))

    return max(counts) - min(counts)


if __name__ == '__main__':
    print(main(lines=get_data(day=14).strip().splitlines()))
