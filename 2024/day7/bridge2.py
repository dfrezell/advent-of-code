#!/usr/bin/env python3

import os
import sys
import itertools
import math
from tqdm import tqdm
from functools import lru_cache
import concurrent.futures

@lru_cache(maxsize=8192)
def cat(x:int, y:int) -> int:
    """cat takes two numbers and concatenates them so that y is appended to x.
    This function is _slow_, so we add an aggressive cache to help speed things
    up.  For very large inputs, it reduces the time by more than half.
    """
    # this is ever so slightly faster than the str -> int concat version
    return x * 10**(math.floor(math.log10(y))+1) + y
    # return int(str(x) + str(y))

def add(x:int, y:int) -> int:
    return x+y

def mul(x:int, y:int) -> int:
    return x*y

# OPERATORS = {lambda x,y: x+y, lambda x,y: x*y, lambda x,y: cat(x,y)}
OPERATORS = {add, mul, cat}
# OPERATORS = {add, mul}

def compute(operands, operators) -> int:
    # pop off the first item in operands to have an initial value for x
    x = next(operands)
    for op, y in zip(operators, operands):
        x = op(x,y)
    return x

def process_line(line:str) -> int:
    total, operands = line.split(":")
    total = int(total)
    operands = list(map(int, operands.split()))
    for operators in itertools.product(OPERATORS, repeat=len(operands)-1):
        val = compute(iter(operands), operators)
        if val == total:
            return val
    return 0

def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        lines = fd.read().splitlines()
        with tqdm(total=len(lines)) as pbar:
            with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
                futures = []
                for line in lines:
                    futures.append(executor.submit(process_line, line))
                for future in concurrent.futures.as_completed(futures):
                    sum += future.result()
                    pbar.update(1)

    print(sum)

    return 0

if __name__ == "__main__":
    sys.exit(main())