#!/usr/bin/env python3

import sys
import logging
import re

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        for line in fd:
            match = re.findall(r"(\d)", line)
            sum += (int(match[0]) * 10 + int(match[-1]))
    print(sum)


if __name__ == "__main__":
    sys.exit(main())