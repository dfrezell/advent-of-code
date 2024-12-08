#!/usr/bin/env python3

import sys
from tqdm import tqdm
import concurrent.futures

def process_line(line:str) -> int:
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