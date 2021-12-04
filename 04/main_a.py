#!/bin/env python3

import fileinput

from board import Board

def play(boards: tuple[Board], drawn_numbers: tuple[int]) -> int:
    for drawn in drawn_numbers:
        print(f'Drawn {drawn}')
        for b in boards:
            b.draw(drawn)
            print(b)
            print()

            if b.is_finished:
                return b.score


def main():
    input_stream = fileinput.input()
    drawn_numbers = tuple(map(int, next(input_stream).strip().split(',')))
    boards: tuple[Board] = tuple(Board.boards_from_input_stream(stream=input_stream))

    print(play(boards=boards, drawn_numbers=drawn_numbers))


if __name__ == '__main__':
    main()
