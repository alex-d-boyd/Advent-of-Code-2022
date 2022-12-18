#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 15: Beacon Exclusion Zone

import argparse
import re
import time

from collections import deque
from pathlib import Path

PATTERN =  r'^Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): '
PATTERN += r'closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)$'

class Sensor:
    def __init__(self, sensor_coords, beacon_coords):
        self.coords = sensor_coords
        self.x, self.y = sensor_coords
        self.beacon = beacon_coords
        self.distance = manhattan_distance(self.coords, self.beacon)

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 15')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    rex = re.compile(PATTERN)
    sensors = set()
    for line in inpt.splitlines():
        coords = rex.match(line).groupdict()
        sensor = (int(coords['sx']), int(coords['sy']))
        beacon = (int(coords['bx']), int(coords['by']))
        sensor = Sensor(sensor, beacon)
        sensors.add(sensor)
    return sensors

def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx + dy

def min_max(sensor, tgt_y):
    x, y = sensor.coords
    dy = abs(y - tgt_y)
    if dy > sensor.distance:
        return None
    min_x = x - (sensor.distance - dy)
    max_x = x + (sensor.distance - dy)
    return (min_x, max_x)

def tuning_freq(point):
    x, y = point
    return 4_000_000 * x + y

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    sensors = parse_input(puzzle_input)
    beacons = set(sensor.beacon for sensor in sensors)

    print('Part 1:')
    print('known good answer: 5166077')
    start = time.time()
    tgt = 10 if args.test else 2_000_000
    coverage = set()
    for sensor in sensors:
        coverage_on_tgt = min_max(sensor, tgt)
        if coverage_on_tgt:
            coverage.add(coverage_on_tgt)
    coverage = sorted(coverage)
    merged_coverage = [coverage[0]]
    for i in range(1, len(coverage)):
        min_x1, max_x1 = merged_coverage[-1]
        min_x2, max_x2 = coverage[i]
        if min_x2 <= max_x1 + 1: # ranges overlap
            merged_coverage[-1] = (min_x1, max(max_x1, max_x2))
        else: # ranges disjoint
            merged_coverage.append(coverage[i])
    covered = -len([b for b in beacons if b[1] == tgt])
    for r in merged_coverage:
        covered += r[1] - r[0] + 1
    print(covered)
    print(time.time()-start)

    print('Part 2:')
    start = time.time()
    max_x = max_y = 20 if args.test else 4_000_000
    for tgt_y in range(max_y + 1):
        coverage = set()
        for sensor in sensors:
            coverage_on_tgt = min_max(sensor, tgt_y)
            if coverage_on_tgt:
                coverage.add(coverage_on_tgt)
        coverage = sorted(coverage)
        merged_coverage = [coverage[0]]
        for i in range(1, len(coverage)):
            min_x1, max_x1 = merged_coverage[-1]
            min_x2, max_x2 = coverage[i]
            if min_x2 <= max_x1 + 1: # ranges overlap
                merged_coverage[-1] = (min_x1, max(max_x1, max_x2))
            else: # ranges disjoint
                merged_coverage.append(coverage[i])
        if len(merged_coverage) == 1:
            continue
        for r in merged_coverage:
            if r[0] <= 0 and r[1] >= max_x:
                continue
        else:
            x = merged_coverage[0][1] + 1
            assert x == merged_coverage[1][0] - 1
            break
    print(x * 4_000_000 + tgt_y)
    print(time.time()-start)
