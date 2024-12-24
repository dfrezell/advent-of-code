
#!/usr/bin/env python3

import sys

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
        for line in lines:
            sum += process_line(line)
    print(sum)
    return 0

if __name__ == "__main__":
    sys.exit(main())