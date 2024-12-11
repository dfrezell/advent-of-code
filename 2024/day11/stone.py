#!/usr/bin/env python3

import sys
import math
import collections

def process_line(line:str, cycles:int) -> int:
    stones = line.split()
    stones = [int(c) for c in stones]
    stonemap = collections.defaultdict(int)
    for s in stones:
        stonemap[s] += 1

    for _ in range(cycles):
        newstonemap = collections.defaultdict(int)
        for stone in stonemap.keys():
            length = 1
            if stone > 9:
                length = math.floor(math.log10(stone)) + 1
                factor = 10**(length//2)
            if stone == 0:
                newstonemap[1] += stonemap[stone]
            elif length % 2 == 0:
                left = stone // factor
                right = stone % factor
                newstonemap[left] += stonemap[stone]
                newstonemap[right] += stonemap[stone]
            else:
                newstonemap[stone * 2024] += stonemap[stone]
        stonemap = newstonemap

    sum = 0
    for n in stonemap.values():
        sum += n
    return sum

def main():
    if len(sys.argv) < 3:
        print("missing file arg and cycles arg")
        return -1

    fname = sys.argv[1]
    cycles = int(sys.argv[2])

    sum = 0
    with open(fname) as fd:
        sum = process_line(fd.read(), cycles)
    print(sum)
    return 0

if __name__ == "__main__":
    sys.exit(main())