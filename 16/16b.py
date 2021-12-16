#!/bin/env python3
import math
import operator
from dataclasses import dataclass
from functools import partial
from itertools import chain
from typing import Any, Union

from aocd import get_data

d_print = lambda *a, **kwargs: ...

int_ = partial(int, base=2)

TO_HEX = {hex(v)[2:].upper(): bin(v)[2:].rjust(4, '0') for v in range(16)}

TYPE_LITERAL = 4

OPS = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda v: operator.gt(*v),
    6: lambda v: operator.lt(*v),
    7: lambda v: operator.eq(*v),
}


@dataclass(frozen=True)
class Packet:
    version: int
    type_id: int

    value: Union[Any, tuple]

    @property
    def op(self):
        return OPS.get(self.type_id)

    def __call__(self):
        try:
            values = tuple(map(lambda v: v(), self))
        except TypeError as e:
            return self.value

        return self.op(values)

    def __iter__(self):
        return iter(self.value)


def load_literal(pkt: str) -> tuple[int, int]:
    i = 0
    value = []
    while True:
        flag, *part = pkt[i * 5:(i + 1) * 5]
        value.extend(part)
        i += 1

        if flag == '0':
            break

    d_print('?____' * i, end='')
    read = i * 5

    assert read % 5 == 0, "Literal has length 5n."

    return read, int_(''.join(value))


def parse_operator(pkt: str, version: int, type_id: int) -> tuple[int, Packet]:
    length_type_id = pkt[0]

    d_print('I', end='')

    if length_type_id == '0':
        # defined by bits
        bits_of_length = pkt[1:16]
        assert len(bits_of_length) == 15, "15 bits of value"

        count_of_bits_to_read = int_(bits_of_length)
        d_print(f'{count_of_bits_to_read:.>15}', end='')

        total_read = 1 + 15 + count_of_bits_to_read

        pkt = pkt[16:]

        values = []
        while count_of_bits_to_read:
            read_bits, value = parse_pkt(pkt)

            pkt = pkt[read_bits:]
            values.append(value)
            count_of_bits_to_read -= read_bits

        return total_read, Packet(version, type_id, tuple(values))

    else:
        # defined by count
        sub_packets_count = int_(pkt[1:12])
        assert len(pkt[1:12]) == 11

        d_print(f'{sub_packets_count:#>11}', end='')
        pkt = pkt[12:]

        values = []
        total_read = 1 + 11  # for length value

        for _ in range(sub_packets_count):
            read_bits, value = parse_pkt(pkt)
            pkt = pkt[read_bits:]
            values.append(value)
            total_read += read_bits

        return total_read, Packet(version, type_id, tuple(values))


def parse_pkt(pkt: str) -> tuple[int, Packet]:
    version = int_(pkt[0:3])
    type_id = int_(pkt[3:6])

    pkt = pkt[6:]

    if type_id == 4:
        d_print('VVV===', end='')
        read, value = load_literal(pkt)
        return read + 6, Packet(version, type_id, value)

    else:
        d_print('VVV+++', end='')
        read, value = parse_operator(pkt, version, type_id)
        # assert read % 4 == 0
        return read + 6, value


def main(code: str):
    binary = ''.join(tuple(chain.from_iterable(map(TO_HEX.__getitem__, code))))

    d_print(binary)
    read, tree = parse_pkt(binary)

    return tree()


if __name__ == '__main__':
    lines_ = get_data().strip().splitlines()[0]
    assert main('C200B40A82') == 3
    d_print()
    assert main('04005AC33890') == 54
    d_print()
    assert main('880086C3E88112') == 7
    d_print()
    assert main('CE00C43D881120') == 9
    d_print()
    assert main('D8005AC2A8F0') == 1
    d_print()
    assert main('F600BC2D8F') == 0
    d_print()
    assert main('9C005AC2F8F0') == 0
    d_print()
    assert main('9C0141080250320F1802104A08') == 1
    d_print()

    print(main(lines_))
