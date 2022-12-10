#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 10: Cathode-Ray Tube

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 10')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    inpt = inpt.splitlines()
    commands = []
    for line in inpt:
        match line.split():
            case ['noop']:
                commands.append(0)
            case ['addx', x]:
                commands.append(int(x))
    return commands

def command_for_cycle(commands, cycle):
    consumed_cycles = 0
    for i, command in enumerate(commands):
        if command == 0:
            consumed_cycles += 1
        else:
            consumed_cycles += 2
        if consumed_cycles >= cycle:
            return i
    else:
        return None

def value_in_cycle(commands, cycle):
    command_num = command_for_cycle(commands, cycle)
    return sum(commands[:command_num]) + 1

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    commands = parse_input(puzzle_input)

    interesting_cycles = [20, 60, 100, 140, 180, 220]
    
    print('Part 1:')
    print(sum(cycle * value_in_cycle(commands, cycle)
              for cycle in interesting_cycles))

    print('Part 2:')
    crt_output = []
    for cycle in range(1, 241):
        cursor = (cycle - 1) % 40
        if abs(cursor - value_in_cycle(commands, cycle)) > 1:
            crt_output.append('.')
        else:
            crt_output.append('#')
    print('\n'.join(''.join(crt_output[i:i+40])
                            for i in range(0, 241, 40)))
