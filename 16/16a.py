#!/bin/env python3
from dataclasses import dataclass
from functools import partial
from itertools import chain
from typing import Any, Union

from aocd import get_data

TO_HEX = {hex(v)[2:].upper(): bin(v)[2:].rjust(4, '0') for v in range(16)}

TYPE_LITERAL = 4

int_ = partial(int, base=2)


@dataclass(frozen=True)
class Packet:
    version: int
    type_id: int

    value: Union[Any, tuple]

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

    print('?____' * i, end='')
    read = i * 5

    assert read % 5 == 0, "Literal has length 5n."

    return read, int_(''.join(value))


def parse_operator(pkt: str, version: int, type_id: int) -> tuple[int, Packet]:
    length_type_id = pkt[0]

    print('I', end='')

    if length_type_id == '0':
        # defined by bits
        bits_of_length = pkt[1:16]
        assert len(bits_of_length) == 15, "15 bits of value"

        count_of_bits_to_read = int_(bits_of_length)
        print(f'{count_of_bits_to_read:.>15}', end='')

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

        print(f'{sub_packets_count:#>11}', end='')
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
        print('VVV===', end='')
        read, value = load_literal(pkt)
        return read + 6, Packet(version, type_id, value)

    else:
        print('VVV+++', end='')
        read, value = parse_operator(pkt, version, type_id)
        # assert read % 4 == 0
        return read + 6, value


def main(code: str):
    binary = ''.join(tuple(chain.from_iterable(map(TO_HEX.__getitem__, code))))

    print(binary)
    read, tree = parse_pkt(binary)
    version_sum = 0

    to_go = [tree]
    while to_go:
        pkt = to_go.pop()
        version_sum += pkt.version
        try:
            to_go.extend(pkt)
        except TypeError:
            pass

    return version_sum


if __name__ == '__main__':
    lines_ = get_data().strip().splitlines()[0]
    assert main('8A004A801A8002F478') == 16
    print()
    assert main('EE00D40C823060') == 14
    print()
    assert main('620080001611562C8802118E34') == 12
    print()
    assert main('C0015000016115A2E0802F182340') == 23
    print()
    # is an operator packet that contains
    #   an operator packet that contains
    #       an operator packet that contains
    #           five literal values; it has a version sum of 31.
    assert main('A0016C880162017C3686B18A3D4780') == 31


    print(main(lines_))
