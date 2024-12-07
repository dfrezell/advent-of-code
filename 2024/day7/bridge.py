#!/usr/bin/env python3

import sys
import logging
import pandas
import numpy
import itertools

def compute_operations(ops) -> int:
    acc = int(ops[0])
    oper = 0
    for o in ops[1:]:
        if o in ['+', '*']:
            oper = o
        else:
            if oper == '+':
                acc += int(o)
            else:
                acc *= int(o)
    return acc

def eval_operations(ops) -> int:
    return eval(''.join(ops))


def check_operators(total:int, operands:list) -> list:
    operators = []
    num_operators = len(operands) - 1
    for x in range(0, 2**num_operators):
        opers = list(numpy.binary_repr(x, num_operators))
        opers = ['+' if c == '0' else '*' for c in opers]
        xxx = [x for x in itertools.chain.from_iterable(itertools.zip_longest(operands, opers)) if x is not None]
        if compute_operations(xxx) == total:
            operators.append(xxx)
    return operators

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
            total, operands = line.split(":")
            total = int(total)
            operands = operands.split()
            operators = check_operators(total, operands)
            if len(operators) > 0:
                sum += total
        print(sum)

    return 0

if __name__ == "__main__":
    sys.exit(main())