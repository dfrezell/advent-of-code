#!/usr/bin/env python3

import sys
import logging
import re

valmap = {
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 0,
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
}

def get_digit(val):
    return valmap[val]
    

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        for line in fd:
            line = line.strip()
            match = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line, )
            val = (get_digit(match[0]) * 10 + get_digit(match[-1]))
            print(val, (match[0], match[-1]), match, line)
            sum += val
    print(sum)


if __name__ == "__main__":
    sys.exit(main())