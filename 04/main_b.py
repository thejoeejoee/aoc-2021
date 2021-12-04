#!/bin/env python3

import fileinput

from board import Board

def play(boards: set[Board], drawn_numbers: tuple[int]) -> int:
    for drawn in drawn_numbers:
        for b in tuple(boards):
            b.draw(drawn)

            if b.is_finished:
                if len(boards) == 1:
                    return boards.pop().score

                boards.discard(b)


def main():
    input_stream = fileinput.input()
    drawn_numbers = tuple(map(int, next(input_stream).strip().split(',')))
    boards: set[Board] = set(Board.boards_from_input_stream(stream=input_stream))

    print(play(boards=boards, drawn_numbers=drawn_numbers))


if __name__ == '__main__':
    main()
