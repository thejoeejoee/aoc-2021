#!/bin/env python3
import functools
import json
import operator
from copy import deepcopy
from functools import partial
from itertools import starmap, permutations
from math import floor, ceil
from operator import attrgetter
from typing import Optional, Iterable

from aocd import get_data
from binarytree import Node as BTreeNode, NodeValue

LEVEL_TO_EXPLODE = 4


class Node(BTreeNode):
    NONE = -1
    parent: "Node" = None

    def __init__(self, value: NodeValue, left: Optional["BTreeNode"] = None,
                 right: Optional["BTreeNode"] = None) -> None:
        super().__init__(value, left, right)

        if right:
            right.parent = self

        if left:
            left.parent = self

    @property
    def valid_nodes(self):
        return list(filter(compose(
            partial(operator.ne, Node.NONE),
            attrgetter('value')
        ), self.inorder))

    @property
    def as_tuples(self):
        if self.value != self.NONE:
            return self.value

        return [self.left.as_tuples, self.right.as_tuples]

    @property
    def magnitude(self):
        if self.value != self.NONE:
            return self.value

        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()
        assert self.value == self.NONE == other.value

        return Node(self.NONE, self, other)


def windowed(seq, n):
    for i in range(len(seq) - n + 1):
        yield seq[i: i + n]


def to_tree(n) -> Node:
    if isinstance(n, int):
        return Node(n)
    return Node(Node.NONE, to_tree(n[0]), to_tree(n[1]))


def compose(*fs):
    return functools.reduce(lambda f, g: lambda *x: f(g(*x)), fs, lambda x: x)


def split(root: Node) -> bool:
    nodes = root.valid_nodes

    for node in filter(
            compose(
                partial(operator.le, 10),
                attrgetter('value')
            ),
            nodes
    ):
        node.left, node.right = Node(floor(half := node.value / 2)), Node(ceil(half))

        node.value = Node.NONE
        node.left.parent = node.right.parent = node
        return True

    return False


def explode(root: Node) -> bool:
    nodes = root.valid_nodes

    try:
        level_to_explore = root.levels[LEVEL_TO_EXPLODE + 1]
    except IndexError:
        return False

    for left, right in filter(
            compose(
                # same level is fine, but it has to have same parent
                partial(starmap, operator.eq),
                partial(map, attrgetter('parent'))
            ),
            windowed(level_to_explore, 2)
    ):  # type: Node, Node

        l_i = nodes.index(left)
        if l_i > 0:
            nodes[l_i - 1].value += left.value

        r_i = nodes.index(right)
        if r_i + 1 < len(nodes):
            nodes[r_i + 1].value += right.value

        parent = left.parent
        parent.left = None
        parent.right = None

        parent.value = 0

        return True

    return False


def reduce(tree: Node):
    while True:
        if explode(tree):
            continue
        if split(tree):
            continue

        return tree


def sum_with_reduce(to_sum: Iterable[Node]):
    return functools.reduce(
        compose(reduce, operator.add),
        to_sum,
    )


def from_spec_to_tree(spec: str) -> Node:
    return to_tree(json.loads(spec))


def main(lines: list[str]):
    trees = tuple(map(from_spec_to_tree, lines))

    return max(map(
        compose(attrgetter('magnitude'), sum_with_reduce, deepcopy),
        permutations(trees, 2))
    )


if __name__ == '__main__':
    lines = get_data().strip().splitlines()
    print(main(lines))
