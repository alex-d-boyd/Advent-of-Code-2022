#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 1: Calorie Counting

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(puzzle_input):
    data = puzzle_input.splitlines()
    elves = []
    elf = []
    for line in data:
        if line:
            elf.append(int(line))
        else:
            elves.append(elf)
            elf = []
    if elf:
        elves.append(elf)
    return elves

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    elves = parse_input(puzzle_input)
    totals = sorted((sum(elf) for elf in elves), reverse=True)

    print('Part 1:')
    print(totals[0])
    
    print('Part 2:')
    print(sum(totals[:3]))
