#!/usr/bin/env python3

import sys
import itertools

def checksum(disk:list) -> list:
    chksum = 0
    for idx, id in enumerate(disk):
        if id == '.':
            continue
        chksum += idx * id
    return chksum

def defrag(disk:list) -> list:
    front = 0
    back = len(disk) - 1

    while front < back:
        if disk[back] == '.':
            back -= 1
            continue
        if disk[front] != '.':
            front += 1
            continue
        disk[front] = disk[back]
        disk[back] = '.'
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
    print(layout)
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