#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 11: Monkey in the Middle

import argparse
import operator

from functools import reduce
from pathlib import Path

class Monkey:
    _OPS = {'+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            }
    
    def __init__(self, name, items, operation, test_divisor,
                 true_monkey, false_monkey, part):
        self.name = name
        self._items = items
        self._operation = operation
        self._test_divisor = test_divisor
        self._true_monkey = true_monkey
        self._false_monkey = false_monkey
        self._part = int(part)
        self._inspection_count = 0
        self.inspect = self._build_inspect()
        self.throw_to = self._build_throw_to()
        self.supermodulo = None

    def __repr__(self):
        i = self._items
        o = self._operation
        d = self._test_divisor
        t = self._true_monkey
        f = self._false_monkey
        return f"Monkey('{self.name}', {i}, '{o}', {d}, {t}, {f})"

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value
        return None

    def __delitem__(self, index):
        del self._items[index]
        return None

    def __iter__(self):
        return iter(self._items)

    def _build_throw_to(self):
        def _throw_to():
            if self[0] % self._test_divisor == 0:
                return self._true_monkey
            else:
                return self._false_monkey
        return _throw_to

    def _build_inspect(self):
        match self._operation.split():
            case [op, 'old']:
                op = self._OPS[op]
                def _inspect():
                    self[0] = op(self[0], self[0])
                    if self._part == 1:
                        self[0] //= 3
                    self._inspection_count += 1
            case [op, x]:
                op = self._OPS[op]
                def _inspect():
                    self[0] = op(self[0], int(x))
                    if self._part == 1:
                        self[0] //= 3
                    self._inspection_count += 1
        return _inspect

    def append(self, value):
        self._items.append(value)
        return None

    def extend(self, items):
        self._items.extend(items)
        return None

    def pop(self, index):
        return self._items.pop(index)

    def take_turn(self):
        throws = {}
        while self._items:
            self.inspect()
            throws.setdefault(self.throw_to(), []).append(self.throw())
        return throws

    def throw(self):
        return self.pop(0)

    def catch(self, items):
        if self._part == 1:
            self.extend(items)
        elif self._part == 2:
            modded = list(map(lambda x: x % self.supermodulo, items))
            self.extend(modded)
        return None

    @property
    def inspected(self):
        return self._inspection_count

    @classmethod
    def parse_from_string(cls, string, part):
        for line in string.splitlines():
            line = line.strip()
            match line.partition(': '):
                case ('Starting items', _, item_list):
                    items = list(map(int, item_list.split(',')))
                case ('Operation', _, op):
                    operation = op.replace('new = old ', '')
                case ('Test', _, test):
                    test_divisor = int(test.split()[-1])
                case ('If true', _, action):
                    true_monkey = int(action.split()[-1])
                case ('If false', _, action):
                    false_monkey = int(action.split()[-1])
                case (str(name), '', ''):
                    name = name.strip(':')

        return cls(name, items, operation, test_divisor,
                   true_monkey, false_monkey, part)


def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 11')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(inpt, part):
    monkeys = [Monkey.parse_from_string(m, part) for m in inpt.split('\n\n')]
    return monkeys


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')


    print('Part 1:')
    monkeys = parse_input(puzzle_input, 1)
    for round_ in range(20):
        for monkey in monkeys:
            catches = monkey.take_turn()
            for catcher, items in catches.items():
                monkeys[catcher].catch(items)
    most_inspected = sorted(monkeys, key=lambda m: m.inspected, reverse=True)
    print(most_inspected[0].inspected * most_inspected[1].inspected)

    print('Part 2:')
    monkeys = parse_input(puzzle_input, 2)
    supermod = reduce(operator.mul, (m._test_divisor for m in monkeys))
    for m in monkeys:
        m.supermodulo = supermod
    for round_ in range(10_000):
        for monkey in monkeys:
            catches = monkey.take_turn()
            for catcher, items in catches.items():
                monkeys[catcher].catch(items)
    most_inspected = sorted(monkeys, key=lambda m: m.inspected, reverse=True)
    print(most_inspected[0].inspected * most_inspected[1].inspected)
