#!/usr/bin/env python3

import sys
from tqdm import tqdm
import concurrent.futures
import itertools
import re
import math
import numpy

def process_line(a:str, b:str, coord:str) -> int:
    mincost = 0
    btn_A_regx = r'Button A: X\+(?P<x1>\d+), Y\+(?P<y1>\d+)'
    btn_B_regx = r'Button B: X\+(?P<x2>\d+), Y\+(?P<y2>\d+)'
    prize_regx = r'Prize: X=(?P<px>\d+), Y=(?P<py>\d+)'
    btn_a_match = re.findall(btn_A_regx, a)
    btn_b_match = re.findall(btn_B_regx, b)
    prize_match = re.findall(prize_regx, coord)

    print("--------------------")
    print("A button:", btn_a_match)
    print("B button:", btn_b_match)
    print("Prize:", coord)
    if btn_a_match and btn_b_match and prize_match:
        btn_a = btn_a_match[0]
        btn_b = btn_b_match[0]
        prize = prize_match[0]
        x1, y1 = int(btn_a[0]), int(btn_a[1])
        x2, y2 = int(btn_b[0]), int(btn_b[1])
        px, py = int(prize[0]) + 10000000000000, int(prize[1]) + 10000000000000
        
        btn_vec = numpy.array([[x1, x2], [y1, y2]])
        prize = numpy.array([px, py])
        btn_press, _, _, _ = numpy.linalg.lstsq(btn_vec, prize)

        # Rounding with the floor fuction doesn't work as expected.
        # even though we have a floating point value of 80.0 and 40.0
        # the floor function will return 79 and 39. This is because
        # of the floating point representation in python.
        # To overcome this, we will use the floor and ceil functions
        # to get the nearest integer value.
        a_press_low = int(numpy.floor(btn_press[0]))
        b_press_low = int(numpy.floor(btn_press[1]))
        a_press_high = int(numpy.ceil(btn_press[0]))
        b_press_high = int(numpy.ceil(btn_press[1]))
        
        # We will iterate over the possible values of a_press and b_press
        # and calculate the cost for each combination. We will then
        # store the minimum cost.
        for a_press in [a_press_low, a_press_high]:
            for b_press in [b_press_low, b_press_high]:
                if a_press < 0 or b_press < 0:
                    continue
                # this will catch the exact values of a_press and b_press because
                # the values we stored are approximations.
                if a_press * x1 + b_press * x2 == px and a_press * y1 + b_press * y2 == py:
                    cost = 3 * a_press + b_press
                    if mincost == 0 or cost < mincost:
                        mincost = cost

    return mincost


def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]

    sum = 0
    with open(fname) as fd:
        lines = fd.read().splitlines()
        for prize in itertools.batched(lines, 4, strict=False):
            sum += process_line(prize[0], prize[1], prize[2])
    print(sum)
    return 0

if __name__ == "__main__":
    sys.exit(main())