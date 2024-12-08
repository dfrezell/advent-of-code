#!/usr/bin/env python3

import sys
from tqdm import tqdm
import concurrent.futures

BAG = {"red": 12, "green": 13, "blue": 14}

def process_line(line:str) -> int:
    game, rounds = line.split(":")
    _, num = game.split()
    num = int(num)
    rounds = [{y: int(x) for x, y in choice} for choice in [[val.split() for val in round] for round in list(map(lambda s: str.split(s, ','), rounds.split(";")))]]
    red = 0
    green = 0
    blue = 0
    for round in rounds:
        red = max(red, round.get("red", 0))
        green = max(green, round.get("green", 0))
        blue = max(blue, round.get("blue", 0))
    return red * green * blue

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