#!/usr/bin/env python3

import sys
import numpy
import itertools

def add(n:tuple, m:tuple):
    return tuple(a + b for a, b in zip(n, m))

def inbounds(n, bounds):
    return all([p>=0 and p<b for p, b in zip(n, bounds)])

def raycast(node, dist, bounds):
    """generate a list of nodes along the vector until we reach the bounds
    """
    ray = []
    while True:
        x = add(node, dist)
        if not inbounds(x, bounds):
            break
        ray.append(x)
        node = x
    return ray

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
                candidates = list(map(lambda n, d: raycast(n, d, shape), others, distance))
                # add current pos as a antinode array
                candidates.append([pos])
                # flatten the list of lists to just a list of tuples
                antinode[tuple(pos)] = [n for c in candidates for n in c]
        for pos, nodes in antinode.items():
            for p in nodes:
                antinodes[p[0],p[1]] = '#'
    
    print(numpy.count_nonzero(antinodes == '#'))
    return 0

if __name__ == "__main__":
    sys.exit(main())