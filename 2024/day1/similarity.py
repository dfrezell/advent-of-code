#!/usr/bin/env python3

import sys
import logging
import collections

logger = logging.getLogger(__name__)

class Similarity(object):
    def __init__(self, filename):
        self.filename = filename
        self.sc = 0
        self.lt = []
        self.rt = collections.defaultdict(int)

    def parse(self):
        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                lt, rt = line.split()
                self.lt.append(lt)
                self.rt[rt] += 1

        for lt in self.lt:
            self.sc += int(lt) * self.rt[lt]
    
    def score(self):
        return self.sc

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
    
    for f in sys.argv[1:]:
        sim = Similarity(f)
        sim.parse()
        print("score: ", sim.score())
    return 0

if __name__ == "__main__":
    sys.exit(main())