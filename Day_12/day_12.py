#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 12: Hill Climbing Algorithm

import argparse
import itertools

from heapq import heapify, heappop, heappush
from pathlib import Path
from string import ascii_lowercase

HEIGHT_VALS = dict(zip(ascii_lowercase, range(26)))

class Priority_Queue:
    def __init__(self):
        self._elements = []
        self._element_finder = {}
        self._counter = itertools.count()

    def __len__(self):
        return len(self._elements)

    def __bool__(self):
        return bool(self._elements)

    def add_node(self, node, priority=0):
        if node in self._element_finder:
            element = self._element_finder.pop(node)
            self._elements.remove(element)
            heapify(self._elements)
        count = next(self._counter)
        element = [priority, count, node]
        self._element_finder[node] = element
        heappush(self._elements, element)

    def get_node(self):
        cost, count, node = heappop(self._elements)
        return node

class Heightmap:
    def __init__(self, mapstring):
        self._grid = [list(line) for line in mapstring.splitlines()]
        self.height = len(self._grid)
        self.width = len(self._grid[0])
        self.low_points = []
        for row in range(self.height):
            for col in range(self.width):
                height_val = self._grid[row][col]
                if height_val == 'S':
                    self.start_node = (row, col)
                    self._grid[row][col] = 'a'
                elif height_val == 'E':
                    self.end_node = (row, col)
                    self._grid[row][col] = 'z'

                if self._grid[row][col] == 'a':
                    self.low_points.append((row, col))

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self._grid)

    def __call__(self, node):
        r, c = node
        return self._grid[r][c]

    def _in_bounds(self, node):
        r, c = node
        return 0 <= r < self.height and 0 <= c < self.width

    def height_val(self, node):
        return HEIGHT_VALS[self(node)]

    def neighbours(self, node):
        r, c = node
        h = self.height_val(node)
        adjacents = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        adjacents = filter(self._in_bounds, adjacents)
        adjacents = filter(lambda n: self.height_val(n) - h <= 1, adjacents)
        return adjacents

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 12')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def manhattan_distance(node_1, node_2):
    dr = abs(node_1[0] - node_2[0])
    dc = abs(node_1[1] - node_2[1])
    return dr + dc

def minimum_path(heightmap, start_node=None, end_node=None, first_valid=False):
    if start_node is None: start_node = heightmap.start_node
    if end_node is None: end_node = heightmap.end_node
    frontier = Priority_Queue()
    came_from = {}
    cost_to_node = {}

    frontier.add_node(start_node)
    came_from[start_node] = None
    cost_to_node[start_node] = 0

    while frontier:
        current_node = frontier.get_node()

        if current_node == end_node:
            break
        if first_valid and heightmap.height_val(current_node) == 0:
            break

        for next_node in heightmap.neighbours(current_node):
            cost_to_next = cost_to_node[current_node] + 1 # fixed cost
            if (next_node not in cost_to_node or
                    cost_to_next < cost_to_node[next_node]):
                cost_to_node[next_node] = cost_to_next
                priority = (cost_to_next +
                            manhattan_distance(next_node, end_node))
                frontier.add_node(next_node, priority)
                came_from[next_node] = current_node
    return came_from, cost_to_node

def construct_path(came_from, start_node, end_node):
    current_node = end_node
    path = []
    if end_node not in came_from:
        return []
    while current_node != start_node:
        path.append(current_node)
        current_node = came_from[current_node]
    path.reverse()
    return path

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    heightmap = Heightmap(puzzle_input)

    print('Part 1:')
    came_from, _ = minimum_path(heightmap)
    first_path = construct_path(came_from, heightmap.start_node, heightmap.end_node)
    print(len(first_path))

    print('Part 2:')
    path_lengths = {}
    path_lengths[heightmap.start_node] = len(first_path)
    for start_node in heightmap.low_points:
        if start_node in path_lengths:
            continue
        elif start_node in first_path:
            try:
                path = construct_path(came_from, start_node, heightmap.end_node)
            except:
                continue
            path_lengths[start_node] = len(path)
            
        else:
            cf, _ = minimum_path(heightmap, start_node)
            path = construct_path(cf, start_node, heightmap.end_node)
            if path:
                path_lengths[start_node] = len(path)
    print(min(path_lengths.values()))
