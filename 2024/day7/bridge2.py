#!/usr/bin/env python3

import sys
import logging
import pandas
import numpy
import itertools


OPERATORS = {'+','*','||'}
# OPERATORS = {'+','*'}

def shunting_yard(infix:list) -> list:
    """Return the infix arithmetic equation in RPN notation for easier computations
    """
    

def perform_operation(x, y, op):
    if op == '+':
        return x + y
    if op == '*':
        return x * y
    if op == '||':
        return int(str(x) + str(y))
    

def compute(infix) -> int:
    """Compute the equation, which is representing in infix notation.  There is no operator
    precedence, just compute left to right.  This uses a modified shunting yard algorithm
    to parse each operator/operand.
    """
    operator_stack = []
    operands_stack = []
    for op in infix:
        if op in OPERATORS:
            operator_stack.append(op)
        else:
            # We have a number, next check if we have an operator pushed on the stack.
            # If so, then we should be guaranteed this is our second operand and we can
            # compute a value.
            if len(operator_stack) > 0:
                n = operands_stack.pop()
                operator = operator_stack.pop()
                operands_stack.append(perform_operation(n, op, operator))
            else:
                operands_stack.append(op)
    return operands_stack.pop()


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