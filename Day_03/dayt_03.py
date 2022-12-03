#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 

import argparse
import string

from pathlib import Path

PRIORITIES = dict(zip(string.ascii_letters, range(1,53)))

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day XX')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    rucksacks = inpt.splitlines()
    rucksacks = [(sack[:len(sack)//2], sack[len(sack)//2:])
                 for sack in rucksacks]
    return rucksacks

def common_item(*sacks):
    sacks = [set(sack) for sack in sacks]
    common = set.intersection(*sacks)
    assert len(common) == 1, common
    return common.pop()

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    rucksacks = parse_input(puzzle_input)
    
    print('Part 1:')
    
    common_items = [common_item(*sack) for sack in rucksacks]
    print(sum(PRIORITIES[ci] for ci in common_items))
    
    print('Part 2:')
    rucksacks = [''.join(sack) for sack in rucksacks]
    groups = [rucksacks[i:i+3] for i in range(0,len(rucksacks),3)]
    badges = [common_item(*group) for group in groups]
    print(sum(PRIORITIES[badge] for badge in badges))
    
