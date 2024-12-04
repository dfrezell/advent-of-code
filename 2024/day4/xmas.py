#!/usr/bin/env python3

import sys
import logging
import pandas
import numpy
import re

def count(needle:str, haystack:str) -> int:
    return len(re.findall(needle, haystack))

def count_rows(needle:str, haystack:numpy.ndarray) -> int:
    sum = 0
    for row in haystack:
        sum += count(needle, ''.join(row))
    for row in numpy.fliplr(haystack):
        sum += count(needle, ''.join(row))

    return sum

def count_cols(needle:str, haystack:numpy.ndarray) -> int:
    sum = 0
    for row in haystack.transpose():
        sum += count(needle, ''.join(row))
    for row in numpy.fliplr(haystack.transpose()):
        sum += count(needle, ''.join(row))

    return sum

def count_diagonals(needle:str, haystack:numpy.ndarray) -> int:
    sum = 0

    sum += 1 if ''.join(numpy.diagonal(haystack)) == needle else 0
    sum += 1 if ''.join(numpy.diagonal(numpy.fliplr(haystack))) == needle else 0
    sum += 1 if ''.join(numpy.diagonal(numpy.flipud(haystack))) == needle else 0
    sum += 1 if ''.join(numpy.diagonal(numpy.fliplr(numpy.flipud(haystack)))) == needle else 0

    return sum

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
        
    fname = sys.argv[1]
    df = pandas.read_fwf(fname, header=None, sep=None)
    df = pandas.read_fwf(fname, header=None, widths=[1 for c in range(0, len(df.iloc[0][0]))])

    arr = df.to_numpy()
    row, col = arr.shape
    word = "XMAS"
    wl = len(word)

    # print(arr)
    total = 0
    for c in range(0, col - wl + 1):
        for r in range(0, row - wl + 1):
            total += count_diagonals(word, arr[r:r+wl, c:c+wl])

    total += count_rows(word, arr)
    total += count_cols(word, arr)

    print(total)

    return 0

if __name__ == "__main__":
    sys.exit(main())