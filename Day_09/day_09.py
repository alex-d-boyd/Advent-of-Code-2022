#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 9: Rope Bridge

import argparse

from pathlib import Path

DELTAS = {'U': (0, 1),
          'R': (1, 0),
          'D': (0, -1),
          'L': (-1, 0),
          }

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Position({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        try:
            return self._hash
        except AttributeError:
            self._hash = hash((self.x, self.y))
            return self._hash

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self == other

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return self.__class__(self.x + other[0], self.y + other[1])
        else:
            return NotImplemented

    def is_adjacent(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 09')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    parser.add_argument('--test-2', help='use test data part 2', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    steps = []
    for line in inpt.splitlines():
        direction, num = line.split()
        steps.extend([direction] * int(num))
    return steps

def get_move(head, tail):
    if head.x == tail.x and head.y > tail.y: # directly above
        return (0, 1)
    elif head.x == tail.x and head.y < tail.y: # directly below
        return (0, -1)
    elif head.x > tail.x and head.y == tail.y: # directly right
        return (1, 0)
    elif head.x < tail.x and head.y == tail.y: # directly left
        return (-1, 0)
    elif head.x > tail.x and head.y > tail.y: # right and above
        return (1, 1)
    elif head.x > tail.x and head.y < tail.y: # right and below
        return (1, -1)
    elif head.x < tail.x and head.y > tail.y: # left and above
        return (-1, 1)
    elif head.x < tail.x and head.y < tail.y: # left and below
        return (-1, -1)
    else:
        raise ValueError('not sure how we got here!')
    

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    elif args.test_2:
        in_file = Path('test_2.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    steps = parse_input(puzzle_input)

    print('Part 1:')
    head = Position(0, 0)
    tail = Position(0, 0)
    tail_trail = {tail}
    for step in steps:
        head = head + DELTAS[step]
        if not head.is_adjacent(tail):
            tail = tail + get_move(head, tail)
            tail_trail.add(tail)
    print(len(tail_trail))

    print('Part 2:')
    rope = [Position(0, 0)] * 10
    tail_trail = {rope[-1]}
    for step in steps:
        rope[0] = rope[0] + DELTAS[step]
        for knot in range(1, len(rope)):
            if not rope[knot].is_adjacent(rope[knot-1]):
                rope[knot] = rope[knot] + get_move(rope[knot-1], rope[knot])
            else:
                break
        tail_trail.add(rope[-1])
    print(len(tail_trail))
