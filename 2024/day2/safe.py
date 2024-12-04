#!/usr/bin/env python3

import sys
import logging
import itertools

logger = logging.getLogger(__name__)

class SafetyReport(object):
    def __init__(self, filename):
        self.filename = filename
        self.sc = 0

    def parse(self):
        report_num = 0
        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                logging.info("===> report %d", report_num)
                report = line.split()
                if self.safe(*report):
                    self.sc += 1
                elif self.subreport(*report):
                    self.sc += 1
                report_num += 1

    def subreport(self, *report):
        for subrep in itertools.combinations(report, len(report) - 1):
            if self.safe(*subrep):
                return True
        return False
    
    def safe(self, *score) -> bool:
        prev = None
        direction = None
        initial_direction = None

        for sc in score:
            sc = int(sc)
            if prev is None:
                prev = sc
                continue

            direction = prev - sc
            prev = sc

            if  abs(direction) < 1 or abs(direction) > 3:
                logging.error("invalid delta: score=%s, sc=%d, prev=%d, direction=%d", score, sc, prev, direction)
                return False
            
            if initial_direction is None:
                initial_direction = direction
                continue

            if direction * initial_direction < 0:
                logging.error("not monotonic: score=%s, sc=%d, prev=%d, direction=%d, initial_direction=%d", score, sc, prev, direction, initial_direction)
                return False

        return True

    def score(self):
        return self.sc

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("missing file args")
        return -1
    
    for f in sys.argv[1:]:
        sim = SafetyReport(f)
        sim.parse()
        print("score: ", sim.score())
    return 0

if __name__ == "__main__":
    sys.exit(main())