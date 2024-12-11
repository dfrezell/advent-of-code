#!/usr/bin/env python3

import sys
import itertools
import collections
import re

def checksum(disk:list) -> list:
    chksum = 0
    for idx, id in enumerate(disk):
        if id == '.':
            continue
        chksum += idx * id
    return chksum

def move_block(disk:list, idx:int, length:int) -> list:
    spn = 0
    pos = None
    # scan for the first available slot
    for i, c in enumerate(disk):
        # stop checking if we scan past our current position
        if i >= idx:
            return disk
        # we are done if we have a fit
        if spn >= length:
            break
        # start the first span
        if c == '.' and pos == None:
            pos = i
            spn = 1
        # continue the span
        elif c == '.':
            spn += 1
        else:
            spn = 0
            pos = None

    id = disk[idx]
    for n in range(length):
        disk[idx+n] = '.'
        disk[pos+n] = id
    return disk

def defrag(disk:list) -> list:
    front = 0
    back = len(disk) - 1

    # print(disk)
    moved = []
    while front < back:
        if disk[back] == '.':
            back -= 1
            continue
        if disk[front] != '.':
            front += 1
            continue

        id = disk[back]
        id_len = 1
        while id == disk[back-1]:
            id_len += 1
            back -= 1

        if id not in moved:
            disk = move_block(disk, back, id_len)
            moved.append(id)
        # print(disk)
        back -= 1
    print(moved)
    return disk

def process_line(line:str) -> int:
    layout = []
    for idx, pair in enumerate(itertools.batched(line, n=2)):
        for _ in range(int(pair[0])):
            layout.append(idx)
        if len(pair) == 2:
            for _ in range(int(pair[1])):
                layout.append('.')
    layout = defrag(layout)
    # print(layout)
    return checksum(layout)

def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        lines = fd.read().splitlines()
        for line in lines:
            sum += process_line(line)
    print(sum)
    return 0

if __name__ == "__main__":
    sys.exit(main())