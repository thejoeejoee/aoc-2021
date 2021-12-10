#!/bin/env python3
import operator
from _operator import attrgetter, itemgetter
from collections import defaultdict
from functools import reduce, partial
from itertools import chain
from statistics import median
from typing import Optional

from aocd import get_data

lines = get_data().strip().splitlines()

lines_ = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip().splitlines()

BRACES = {
    '(': ')',
    '{': '}',
    '<': '>',
    '[': ']',
}

SCORES = {
    '(': 1,
    '{': 3,
    '<': 4,
    '[': 2,
}


def score_of_missing(stack) -> int:
    total = 0

    for c in stack[::-1]:
        total *= 5
        total += SCORES[c]
    return total


def compute_score(line) -> Optional[int]:
    stack = []

    for c in line:
        if c in BRACES.keys():
            stack.append(c)
            continue

        assert stack

        last = stack[-1]
        expected = BRACES[last]

        if expected == c:
            stack.pop()
            continue

        return None

    return score_of_missing(stack=stack)


def main():
    return median(filter(None, map(compute_score, lines)))


if __name__ == '__main__':
    print(main())
