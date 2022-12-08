#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 2: Rock Paper Scissors

import argparse

from enum import Enum
from pathlib import Path

class throw(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

THROWS = {
    'A': throw.ROCK,
    'X': throw.ROCK,
    'B': throw.PAPER,
    'Y': throw.PAPER,
    'C': throw.SCISSORS,
    'Z': throw.SCISSORS,
    }

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 02')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input_pt_1(inpt):
    hands = [tuple(map(THROWS.get, line.split())) for line in inpt.splitlines()]
    return hands

def win(them):
    if them == throw.ROCK:
        return throw.PAPER
    elif them == throw.PAPER:
        return throw.SCISSORS
    elif them == throw.SCISSORS:
        return throw.ROCK

def lose(them):
    if them == throw.ROCK:
        return throw.SCISSORS
    elif them == throw.PAPER:
        return throw.ROCK
    elif them == throw.SCISSORS:
        return throw.PAPER

def draw(them):
    return them

RESPONSES = {
    'X': lose,
    'Y': draw,
    'Z': win,
    }

def parse_input_pt_2(inpt):
    hands = []
    for line in inpt.splitlines():
        spl = line.split()
        them = THROWS[spl[0]]
        me = RESPONSES[spl[1]](them)
        hand = (them, me)
        hands.append(hand)
    return hands

def result(them, me):
    if them == me: # draw
        return 3
    elif ((me == throw.ROCK and them == throw.SCISSORS) or
          (me == throw.PAPER and them == throw.ROCK) or
          (me == throw.SCISSORS and them == throw.PAPER)):
        return 6
    else:
        return 0

def score(them, me):
    score = me.value
    score += result(them, me)
    return score


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    print('Part 1:')
    hands = parse_input_pt_1(puzzle_input)
    total = sum(score(them, me) for them, me in hands)
    print(total)
    
    print('Part 2:')
    hands = parse_input_pt_2(puzzle_input)
    total = sum(score(them, me) for them, me in hands)
    print(total)
