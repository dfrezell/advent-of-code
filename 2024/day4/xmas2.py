#!/usr/bin/env python3

import sys
import logging
import pandas
import numpy

def match_diagonals(needle:str, haystack:numpy.ndarray) -> int:
    sum = 0

    sum += 1 if ''.join(numpy.diagonal(haystack)) == needle else 0
    sum += 1 if ''.join(numpy.diagonal(numpy.fliplr(haystack))) == needle else 0
    sum += 1 if ''.join(numpy.diagonal(numpy.flipud(haystack))) == needle else 0
    sum += 1 if ''.join(numpy.diagonal(numpy.fliplr(numpy.flipud(haystack)))) == needle else 0

    return 1 if sum == 2 else 0

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
        
    fname = sys.argv[1]
    df = pandas.read_fwf(fname, header=None, sep=None)
    df = pandas.read_fwf(fname, header=None, widths=[1 for _ in range(0, len(df.iloc[0][0]))])

    arr = df.to_numpy()
    row, col = arr.shape
    word = "MAS"
    wl = len(word)

    total = 0
    for c in range(0, col - wl + 1):
        for r in range(0, row - wl + 1):
            total += match_diagonals(word, arr[r:r+wl, c:c+wl])

    print(total)

    return 0

if __name__ == "__main__":
    sys.exit(main())