#!/usr/bin/env python3

import sys
import logging
import pandas
import re

class Multiply(object):
    regx = r"mul\((?P<d1>\d{1,3}),(?P<d2>\d{1,3})\)|do\(\)|don't\(\)"
    def __init__(self, mul:str):
        self.mulstr = mul

    def multiply(self) -> int:
        val = 0
        pat = re.compile(self.regx)
        matches = pat.finditer(self.mulstr)
        skip = False
        for m in matches:
            if m.group() == "do()":
                skip = False
            elif m.group() == "don't()":
                skip = True
            elif m.group().startswith("mul"):
                if not skip:
                    x, y = m.groups()
                    val += int(x) * int(y)
        return val

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
    
    for f in sys.argv[1:]:
        with open(f, 'r') as file:
            content = file.read()
            m = Multiply(content)
            val = m.multiply()
            print(val)
    return 0

if __name__ == "__main__":
    sys.exit(main())