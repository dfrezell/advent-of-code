#!/usr/bin/env python3

import sys
import logging
import collections
import functools

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

    def compare(item1, item2):
        if item1 in ordering:
            if item2 in ordering[item1]:
                return -1
        if item2 in ordering:
            if item1 in ordering[item2]:
                return 1
        return 0

    sum = 0
    for p in pages:
        ordered = is_ordered(p, ordering)
        if not ordered:
            new_p = sorted(p, key=functools.cmp_to_key(compare))
            sum += int(new_p[len(new_p) // 2])

        # print(p, ordered)

    print(sum)

    return 0

if __name__ == "__main__":
    sys.exit(main())