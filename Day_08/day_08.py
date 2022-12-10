#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 8: Treetop Tree House

import argparse

from itertools import takewhile
from functools import reduce
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 08')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    return [list(map(int,line)) for line in inpt.splitlines()]

def is_visible(r, c, height_map):
    rows, cols = len(height_map), len(height_map[0])
    height = height_map[r][c]
    if r == 0 or r == rows-1 or c == 0 or c == cols -1:
        return True
    elif (all(h < height for h in height_map[r][:c]) or
          all(h < height for h in height_map[r][c+1:]) or
          all(height_map[i][c] < height for i in range(r)) or
          all(height_map[i][c] < height for i in range(r+1, rows))):
        return True
    else:
        return False

def view_distance(r, c, direction, height_map):
    rows, cols = len(height_map), len(height_map[0])
    height = height_map[r][c]
    match direction.lower():
        case 'up':
            if r == 0:
                return 0
            path = [height_map[i][c] for i in range(r-1,-1,-1)]
        case 'right':
            if c == cols-1:
                return 0
            path = height_map[r][c+1:]
        case 'down':
            if r == rows-1:
                return 0
            path = [height_map[i][c] for i in range(r+1,rows)]
        case 'left':
            if c == 0:
                return 0
            path = height_map[r][c-1::-1]
    if all(h < height for h in path):
        return len(path)
    else:
        path = list(takewhile(lambda x: x < height, path))
        return len(path)+1

def senic_score(r, c, height_map):
    return reduce(lambda x,y: x*y,
                 (view_distance(r, c, direction, height_map)
                  for direction in ('up down left right'.split())))

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    height_map = parse_input(puzzle_input)

    print('Part 1:')
    print(sum(is_visible(r, c, height_map)
              for r in range(len(height_map))
              for c in range(len(height_map[0]))
              ))


    print('Part 2:')
    print(max(senic_score(r, c, height_map)
              for r in range(len(height_map))
              for c in range(len(height_map[0]))
              ))
