#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2022
# Day 7: No Space Left On Device

import argparse

from pathlib import Path

class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self._folders = []
        self._files = []
        self._files_size = 0
        self._parent = parent

    def __repr__(self):
        return self.name

    @property
    def size(self):
        return sum(folder.size for folder in self._folders) + self._files_size

    def add_folder(self, folder):
        folder._parent = self
        self._folders.append(folder)

    def add_file(self, file):
        self._files.append(file)
        self._files_size += file.size

    @property
    def parent(self):
        return self._parent

    def sub_folder(self, name):
        sub = [folder for folder in self._folders if folder.name == name][0]
        return sub

    def flatten_folders(self):
        flat_list = [f for folder in self._folders
                     for f in folder.flatten_folders()]
        flat_list.append(self)
        return flat_list
        

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2022 Day 07')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    root = Folder('root')
    current_folder = root

    for line in puzzle_input.splitlines():
        # print(line)
        match line.split():
            case ['$', 'cd', '/']:
                current_folder = root
            case ['$', 'cd', '..']:
                current_folder = current_folder.parent
            case ['$', 'cd', folder]:
                current_folder = current_folder.sub_folder(folder)
            case ['$', _]:
                pass
            case ['dir', name]:
                # print(f'Adding folder {name}')
                current_folder.add_folder(Folder(name))
            case [size, name]:
                # print(f'Adding file {name} ({size})')
                current_folder.add_file(File(name, int(size)))
            case _:
                raise ValueError("Shouldn't get here")

    print('Part 1:')
    tgts = [folder for folder in root.flatten_folders()
            if folder.size <= 100_000]
    print(sum(tgt.size for tgt in tgts))

    print('Part 2:')
    free_space = 70_000_000 - root.size
    tgt_size = 30_000_000 - free_space
    tgt = min((folder for folder in root.flatten_folders()
               if folder.size >= tgt_size), key=lambda x: x.size)
    print(tgt, tgt.size)
