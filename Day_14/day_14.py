#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 14: Regolith Reservoir

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 14')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    parser.add_argument('-v', '--visualise', help='print visualisation',
                        action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt):
    rock_points = set()
    for line in inpt.splitlines():
        rock_points.update(build_wall(line))
    return rock_points

def build_wall(line):
    end_points = [tuple(map(int,c.split(','))) for c in line.split(' -> ')]
    wall_points = set()
    for i in range(len(end_points) - 1):
        x1, y1 = end_points[i]
        x2, y2 = end_points[i+1]
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2+1):
                wall_points.add((x1, y))
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2+1):
                wall_points.add((x, y1))
        else:
            raise ValueError('not sure how we got here - bad input?')
    return wall_points

def rest_point(x, start_y, rock, sand, floor=None):
    impassable = rock.union(sand)
    points = (point for point in impassable if point[0]==x and point[1]>start_y)
    try:
        xb, yb = min(points, key=lambda x: x[1])
    except ValueError:
        if floor is None:
            return None
        else:
            return x, floor-1
    if (xb-1, yb) in impassable and (xb+1, yb) in impassable:
        return (xb, yb-1)
    elif (xb-1, yb) not in impassable:
        return rest_point(xb-1, yb, rock, sand, floor)
    elif (xb+1, yb) not in impassable:
        return rest_point(xb+1, yb, rock, sand, floor)
    else:
        raise ValueError('something went weird somewhere')

def drop_from(x, y, rock, sand, floor):
    if (x, y) in rock or (x, y) in sand or y == floor:
        return None
    for dx in [0, -1, 1]:
        drop_from(x+dx, y+1, rock, sand, floor)
    sand.add((x, y))

def visualise(rock, sand, floor=None):
    impassable = rock.union(sand)
    min_x = min(impassable, key = lambda p: p[0])[0]
    max_x = max(impassable, key = lambda p: p[0])[0] + 1
    min_y = 0
    max_y = max(impassable, key = lambda p: p[1])[1] + 1
    if floor is not None:
        min_x -= 2
        max_x += 2
        max_y = floor
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) in rock_points:
                print('#', end='')
            elif (x, y) in sand_points:
                print('o', end='')
            else:
                print('.', end='')
        print()
    if floor is not None:
        print('#' * (max_x - min_x))
    print()


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    rock_points = parse_input(puzzle_input)
    sand_points = set()

    print('Part 1:')
    while (rp := rest_point(500, 0, rock_points, sand_points)) is not None:
        sand_points.add(rp)
    print(len(sand_points))
    if args.visualise:
        visualise(rock_points, sand_points)
    
    print('Part 2:')
    sand_points = set()
    floor = max(rock_points, key = lambda p: p[1])[1] + 2
    drop_from(500, 0, rock_points, sand_points, floor)
    print(len(sand_points))
    if args.visualise:
        visualise(rock_points, sand_points, floor=floor)
