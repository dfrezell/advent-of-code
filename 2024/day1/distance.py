#!/usr/bin/env python3

import sys
import logging

logger = logging.getLogger(__name__)

class Distance(object):
    def __init__(self, filename):
        self.filename = filename
        self.dist = 0
        self.lt = []
        self.rt = []

    def parse(self):
        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                lt, rt = line.split()
                logging.info("lt: %s, rt: %s", lt, rt)
                self.lt.append(lt)
                self.rt.append(rt)

        if len(self.lt) != len(self.rt):
            raise IndexError("left and right list mismatch length")
        
        self.lt.sort()
        self.rt.sort()

        for lt, rt in zip(self.lt, self.rt):
            logging.info("read: %s, %s", lt, rt)
            self.dist += abs(int(lt) - int(rt))
    
    def distance(self):
        return self.dist

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
    
    for f in sys.argv[1:]:
        distance = Distance(f)
        logging.info(distance)
        distance.parse()
        logging.info(distance.distance())
    return 0

if __name__ == "__main__":
    sys.exit(main())