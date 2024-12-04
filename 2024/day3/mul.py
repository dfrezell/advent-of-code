#!/usr/bin/env python3

import sys
import logging
import pandas
import re

class Multiply(object):
    regx = r"mul\((?P<d1>\d{1,3}),(?P<d2>\d{1,3})\)"
    def __init__(self, mul:str):
        self.mulstr = mul

    def multiply(self) -> int:
        val = None
        pat = re.compile(self.regx)
        matches = pat.findall(self.mulstr)
        if len(matches) > 0:
            val = 0
        for m in matches:
            val += int(m[0]) * int(m[1])
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
        # data = pandas.read_table(f, header=None)
        # for idx, row in data.iterrows():
        #     m = Multiply(row.to_list()[0])
        #     val = m.multiply()
        #     print(idx, ":", val)
    return 0

if __name__ == "__main__":
    sys.exit(main())