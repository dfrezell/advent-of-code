#!/usr/bin/env python3

import sys
import logging
import pandas
import numpy

UP = "^"
DN = "v"
LF = "<"
RG = ">"

def turn_90(dir):
    if dir == UP:
        return RG
    if dir == RG:
        return DN
    if dir == DN:
        return LF
    if dir == LF:
        return UP

def get_next_pos(pos, dir) -> tuple:
    if dir == UP:
        npos = (pos[0] - 1, pos[1])
    elif dir == DN:
        npos = (pos[0] + 1, pos[1])
    elif dir == LF:
        npos = (pos[0], pos[1] - 1)
    elif dir == RG:
        npos = (pos[0], pos[1] + 1)

    return npos

def check_bounds(arr:numpy.ndarray, pos):
    w, h = arr.shape
    if pos[0] < 0 or pos[0] >= w:
        raise IndexError
    if pos[1] < 0 or pos[1] >= h:
        raise IndexError

def has_loop(arr, pos, dir):
    visited = []
    try:
        while True:
            npos = get_next_pos(pos, dir)
            check_bounds(arr, npos)

            if (npos, dir) in visited:
                return True

            if arr[npos] == '.':
                visited.append((pos, dir))
                pos = npos
            elif arr[npos] == '#':
                dir = turn_90(dir)
    except IndexError:
        visited.append((pos, dir))

    return False

def check_loop(arr, pos, dir, visited:list):
    looper = []
    visited.pop(0)
    checked = []
    for lpos, _ in visited:
        if lpos in checked:
            continue
        checked.append(lpos)
        arr[lpos] = "#"
        if has_loop(arr, pos, dir):
            looper.append(lpos)
            print("checking", lpos, "loops")
        else:
            print("checking", lpos,"no loop")
        arr[lpos] = "."

    return set(looper)

def record_moves(arr, pos, dir):
    visited = []
    
    try:
        while True:
            npos = get_next_pos(pos, dir)
            check_bounds(arr, npos)

            if arr[npos] == '.':
                visited.append((pos, dir))
                pos = npos
            elif arr[npos] == '#':
                dir = turn_90(dir)
    except IndexError:
        visited.append((pos, dir))

    return visited

def find_guard(arr: numpy.ndarray) -> tuple:
    for idx, val in numpy.ndenumerate(arr):
        if val in (UP, DN, LF, RG):
            return (idx, val)

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1

    fname = sys.argv[1]
    df = pandas.read_fwf(fname, header=None, sep=None)
    df = pandas.read_fwf(fname, header=None, widths=[1 for c in range(0, len(df.iloc[0][0]))])

    arr = df.to_numpy()
    
    pos, dir = find_guard(arr)
    arr[pos] = '.'
    visited = record_moves(arr, pos, dir)
    loops = check_loop(arr, pos, dir, visited)

    print(len(loops))

    return 0

if __name__ == "__main__":
    sys.exit(main())