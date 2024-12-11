#!/usr/bin/env python3

import sys
import itertools

def expand(disk:list) -> list:
    layout = []
    for c in disk:
        for _ in range(c[1]):
            layout.append('.' if c[0] is None else c[0])
    return layout

def checksum(disk:list) -> list:
    chksum = 0
    layout = expand(disk)
    for idx, id in enumerate(layout):
        if id == '.':
            continue
        chksum += idx * id
    return chksum

def defrag(disk:list) -> list:
    front = 0
    back = len(disk) - 1
    moved = []
    while front < back:
        if disk[back][0] == None:
            back -= 1
            continue
        if disk[front][0] != None:
            front += 1
            continue
        id = disk[back][0]

        if id not in moved:
            tomove = disk[back]
            for i in range(front, back):
                curblock = disk[i]
                if curblock[0] == None and curblock[1] >= tomove[1]:
                    disk[back] = (None, tomove[1])
                    disk[i] = tomove
                    if curblock[1] > tomove[1]:
                        disk.insert(i+1, (None, curblock[1] - tomove[1]))
                    break
            moved.append(id)
        back -= 1

    return disk

def process_line(line:str) -> int:
    disk = []
    for idx, pair in enumerate(itertools.batched(line, n=2)):
        disk.append((idx, int(pair[0])))
        if len(pair) == 2:
            disk.append((None, int(pair[1])))
    disk = defrag(disk)
    return checksum(disk)

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