#!/usr/bin/env python3

import sys
from tqdm import tqdm
import concurrent.futures

def isclimb(map, cur, next):
    cx, cy = cur
    nx, ny = next
    if map[nx][ny] == '.':
        return False
    return int(map[cx][cy])+1 == int(map[nx][ny])


def traverse(map, x, y, matches):
    if map[x][y] == '9':
        matches.add((x,y))
        return

    up = None if x - 1 < 0 or not isclimb(map, (x, y), (x-1, y)) else traverse(map, x - 1, y, matches)
    dn = None if x + 1 >= len(map) or not isclimb(map, (x, y), (x+1, y)) else traverse(map, x + 1, y, matches)
    lf = None if y - 1 < 0 or not isclimb(map, (x, y), (x, y-1)) else traverse(map, x, y - 1, matches)
    rg = None if y + 1 >= len(map[x]) or not isclimb(map, (x, y), (x, y+1)) else traverse(map, x, y + 1, matches)

def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        zeroes = []
        lines = fd.read().splitlines()
        map=[]
        for x, line in enumerate(lines):
            map.append([])
            for y, c in enumerate(line):
                map[x].append(c)
                if c == '0':
                    zeroes.append((x,y))
        
        for x, y in zeroes:
            matches = set()
            traverse(map, x, y, matches)
            sum += len(matches)

    print(sum)
    return 0

if __name__ == "__main__":
    sys.exit(main())