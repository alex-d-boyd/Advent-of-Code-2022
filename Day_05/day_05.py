#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 5: Supply Stacks

import argparse
import copy
import re

from collections import namedtuple
from pathlib import Path

Step = namedtuple('Step', 'qty src dst')
STEP_REX = re.compile(r'move (?P<qty>\d+) from (?P<src>\d+) to (?P<dst>\d+)')

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 05')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    def parse_step(step):
        return Step(*map(int, STEP_REX.match(step).groups()))
    lines = inpt.splitlines()
    stack_lines = []
    while line := lines.pop(0):
        stack_lines.append(line)
    method_lines = lines

    stack_lists = []
    for line in stack_lines:
        stack_list = list(map(str.strip, (line[i:i+4][1]
                                          for i in range(0, len(line), 4))))
        stack_lists.append(stack_list)
    stacks = {int(s): None for s in stack_lists.pop()}
    for stack in stacks:
        stacks[stack] = [crate for stack_list in reversed(stack_lists)
                         if (crate := stack_list[stack-1])]
    

    steps = [parse_step(step) for step in method_lines]
    return stacks, steps

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    stacks, steps = parse_input(puzzle_input)
    pt2_stacks = copy.deepcopy(stacks)

    print('Part 1:')
    for step in steps:
        for _ in range(step.qty):
            stacks[step.dst].append(stacks[step.src].pop())
    print(''.join(stack[-1] for stack in stacks.values()))

    print('Part 2:')
    stacks = pt2_stacks
    for step in steps:
        stacks[step.dst].extend(stacks[step.src][-step.qty:])
        stacks[step.src] = stacks[step.src][:-step.qty]
    print(''.join(stack[-1] for stack in stacks.values()))
