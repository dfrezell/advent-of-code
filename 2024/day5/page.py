#!/usr/bin/env python3

import sys
import logging
import pandas
import numpy
import re
import collections

def read_order(fd):
    ordering = collections.defaultdict(list)
    for line in fd:
        line = line.rstrip()
        if line == "":
            break
        pb, pa = line.split("|")
        ordering[pb].append(pa)

    return ordering

def read_pages(fd):
    pages = list()
    for line in fd:
        line = line.rstrip()
        pages.append(line.split(","))

    return pages

def is_ordered(pages:list, ordering):
    for i in range(1, len(pages)):
        if any(item in pages[:i] for item in ordering[pages[i]]):
            return False
    return True

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
        
    fname = sys.argv[1]
    with open(fname) as fd:
        ordering = read_order(fd)
        pages = read_pages(fd)

    sum = 0
    for p in pages:
        ordered = is_ordered(p, ordering)
        if ordered:
            sum += int(p[len(p) // 2])
        print(p, ordered)

    print(sum)

    return 0

if __name__ == "__main__":
    sys.exit(main())