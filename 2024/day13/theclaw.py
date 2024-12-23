#!/usr/bin/env python3

import sys
from tqdm import tqdm
import concurrent.futures
import itertools
import re

def process_line(a:str, b:str, coord:str) -> int:
    mincost = 0
    btn_A_regx = r'Button A: X\+(?P<x1>\d+), Y\+(?P<y1>\d+)'
    btn_B_regx = r'Button B: X\+(?P<x2>\d+), Y\+(?P<y2>\d+)'
    prize_regx = r'Prize: X=(?P<px>\d+), Y=(?P<py>\d+)'
    btn_a_match = re.findall(btn_A_regx, a)
    btn_b_match = re.findall(btn_B_regx, b)
    prize_match = re.findall(prize_regx, coord)

    print("--------------------")
    print(btn_a_match)
    print(btn_b_match)
    print(coord)
    if btn_a_match and btn_b_match and prize_match:
        btn_a = btn_a_match[0]
        btn_b = btn_b_match[0]
        prize = prize_match[0]
        x1, y1 = int(btn_a[0]), int(btn_a[1])
        x2, y2 = int(btn_b[0]), int(btn_b[1])
        px, py = int(prize[0]), int(prize[1])

        min_a = min(px // x1, py // y1, 100)
        candidates = []
        for i in range(min_a, 0, -1):
            cx, cy = x1 * i, y1 * i
            j = min((px - cx) // x2, (py - cy) // y2)
            dx = x2 * j
            dy = y2 * j
            if (cx + dx == px) and (cy + dy == py):
                candidates.append((i, j))
        print(candidates)

        
        for c in candidates:
            cost = 3 * c[0] + c[1]
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
            
        # with tqdm(total=len(lines)) as pbar:
        #     with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        #         futures = []
        #         for line in lines:
        #             futures.append(executor.submit(process_line, line))
        #         for future in concurrent.futures.as_completed(futures):
        #             sum += future.result()
        #             pbar.update(1)
    print(sum)
    return 0

if __name__ == "__main__":
    sys.exit(main())