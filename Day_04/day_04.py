#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 4: Camp Cleanup

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day XX')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    def parse_line(line):
        ranges = [list(map(int, r.split('-'))) for r in line.split(',')]
        ranges = [set(range(r[0], r[1]+1)) for r in ranges]
        return ranges
    ranges = [parse_line(line) for line in inpt.splitlines()]
    return ranges


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    ranges = parse_input(puzzle_input)

    print('Part 1:')
    overlaps = sum((r[0] <= r[1]) + (r[0] > r[1]) for r in ranges)
    print(overlaps)
    
    print('Part 2:')
    has_overlap = sum(bool(r[0].intersection(r[1])) for r in ranges)
    print(has_overlap)
