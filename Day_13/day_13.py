#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 13: Distress Signal

import argparse

from itertools import zip_longest
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 13')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    inpt = list(filter(None, inpt.splitlines()))
    pairs = [(parse_packet(inpt[i]), parse_packet(inpt[i+1]))
             for i in range(0, len(inpt), 2)]    
    return pairs

def parse_packet(line):
    line = line.replace(' ','')
    packet = []
    i = 1
    while i < len(line):
        if line[i].isdigit():
            dig = line[i]
            while line[i+1].isdigit():
                i += 1
                dig += line[i]
            packet.append(int(dig))
            i += 1
        elif line[i] == ',':
            i += 1
            continue
        elif line[i] == '[':
            subpacket = parse_packet(line[i:])
            packet.append(subpacket)
            i += len(str(subpacket).replace(' ', ''))
        elif line[i] == ']':
            return packet
        else:
            raise ValueError('not sure how we got here')

def check_packet_order(packet1, packet2):
    for p1_elem, p2_elem in zip_longest(packet1, packet2):
        if p1_elem is None:
            return True
        if p2_elem is None:
            return False
        if isinstance(p1_elem, int) and isinstance(p2_elem, int):
            if p1_elem < p2_elem:
                return True
            elif p1_elem > p2_elem:
                return False
            else: #equal
                continue
        elif isinstance(p1_elem, int):
            sub_check = check_packet_order([p1_elem], p2_elem)
            if sub_check is not None:
                return sub_check
        elif isinstance(p2_elem, int):
            sub_check = check_packet_order(p1_elem, [p2_elem])
            if sub_check is not None:
                return sub_check
        else: # Both lists
            sub_check = check_packet_order(p1_elem, p2_elem)
            if sub_check is not None:
                return sub_check
    return None

def bubble_sort(collection):
    for i in range(len(collection)):
        flag = True
        for j in range(len(collection)-1):
            if not check_packet_order(collection[j], collection[j+1]):
                collection[j], collection[j+1] = collection[j+1], collection[j]
                flag = False
        if flag:
            break


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    pairs = parse_input(puzzle_input)

    print('Part 1:')
    ok_pairs = []
    for i, pair in enumerate(pairs, start=1):
        if check_packet_order(*pair):
            ok_pairs.append(i)
    print(sum(ok_pairs))

    print('Part 2:')
    stream = [p for pair in pairs for p in pair]
    stream.append([[2]])
    stream.append([[6]])
    bubble_sort(stream)
    d1 = stream.index([[2]]) + 1
    d2 = stream.index([[6]]) + 1
    print(d1 * d2)
    
