#!/usr/bin/env python3

import sys
import logging
import numpy
import itertools
import math


OPERATORS = {'+','*','||'}
# OPERATORS = {'+','*'}

def perform_operation(x:int, y:int, op:str) -> str:
    """Perform the operation on the two operands and return the result.

    >>> perform_operation(100, 99, '||')
    10099
    >>> perform_operation(100, 99, '+')
    199
    >>> perform_operation(100, 99, '*')
    9900
    """
    if op == '+':
        return x + y
    elif op == '*':
        return x * y
    elif op == '||':
        # this is ever so slightly faster than the str -> int concat version
        return x * 10**(math.floor(math.log10(y))+1) + y
        # return int(str(x) + str(y))
    raise ValueError
    

def compute(infix) -> int:
    """Compute the equation, which is representing in infix notation.  There is no operator
    precedence, just compute left to right.  This uses a modified shunting yard algorithm
    to parse each operator/operand.
    """
    p_operator = None
    p_operand = None
    for op in infix:
        if op in OPERATORS:
            p_operator = op
        else:
            # We have a number, next check if we have an operator pushed on the stack.
            # If so, then we should be guaranteed this is our second operand and we can
            # compute a value.
            if p_operator is not None:
                p_operand = perform_operation(p_operand, op, p_operator)
            else:
                p_operand = op
    return p_operand


def gen_operators(num_operands) -> list:
    """Return the complete set of operators for a number of operands.
    We want a list of length num_operands - 1 with a value in the set
    of possible operators: { '+', '*', '||' }
    
    >>> gen_operators(2)
    [('||',), ('+',), ('*',)]

    >>> gen_operators(3)
    [('||', '||'), ('||', '+'), ('||', '*'), ('+', '||'), ('+', '+'), ('+', '*'), ('*', '||'), ('*', '+'), ('*', '*')]
    """
    return list(itertools.product(OPERATORS, repeat=num_operands-1))

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        pos = 0
        for line in fd:
            print("working", pos)
            line = line.strip()
            total, operands = line.split(":")
            total = int(total)
            operands = numpy.array(operands.split(), int)
            operators = gen_operators(len(operands))
            for oper in operators:
                infix = [x for x in itertools.chain.from_iterable(itertools.zip_longest(operands, oper)) if x is not None]
                val = compute(infix)
                if val == total:
                    sum += total
                    break
            pos += 1
            
        print(sum)

    return 0

if __name__ == "__main__":
    sys.exit(main())