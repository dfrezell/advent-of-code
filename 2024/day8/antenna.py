#!/usr/bin/env python3

import sys
from tqdm import tqdm
import concurrent.futures
import numpy
import itertools

def process_line(line:str) -> int:
    return 0

def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]

    with open(fname) as fd:
        lines = fd.read().splitlines()
        arr = numpy.array([list(itertools.chain(line)) for line in lines])
        antinodes = numpy.full(arr.shape, '.', dtype=str)
        shape = arr.shape
        antinode = {}
        frequencies = numpy.unique(arr)

        for freq in frequencies:
            if freq == '.':
                continue
            antenna = numpy.argwhere(arr == freq[0]).tolist()
            for idx, pos in enumerate(antenna):
                others = antenna[0:idx] + antenna[idx+1:]
                distance = list(map(lambda x: (x[0] - pos[0], x[1] - pos[1]), others))
                candidates = list(map(lambda n, d: (n[0] + d[0], n[1] + d[1]), others, distance))
                # filter out of range nodes
                antinode[tuple(pos)] = [x for x in candidates if x[0]>=0 and x[0]<shape[0] and x[1]>=0 and x[1]<shape[0]]
        for pos, nodes in antinode.items():
            for p in nodes:
                if antinodes[p[0],p[1]] != '#':
                    antinodes[p[0],p[1]] = '#'
    print(numpy.count_nonzero(antinodes == '#'))
    return 0

if __name__ == "__main__":
    sys.exit(main())