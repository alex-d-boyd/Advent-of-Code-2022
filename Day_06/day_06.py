#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 6: Tuning Trouble

import argparse

from collections import deque
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 06')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def all_unique(iter):
    return all(iter.count(elem) == 1 for elem in iter)


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    stream = in_file.read_text(encoding='utf-8')

    print('Part 1:')
    buffer = deque(stream[:4], maxlen=4) # prime buffer with first 4 chars
    i = 4 # last char appended (base 1) / next char (base 0)
    while not all_unique(buffer):
        buffer.append(stream[i])
        i += 1
    print(i)

    print('Part 2:')
    buffer = deque(stream[:4], maxlen=14) # prime buffer with first 4 chars
    i = 4 # last char appended (base 1) / next char (base 0)
    while not all_unique(buffer):
        buffer.append(stream[i])
        i += 1
    print(i)
