#!/usr/bin/env python3

class ColumnFile(object):
    def __init__(self, filename:str, num_cols:int = 2):
        self.filename = filename
        self.columns = [num_cols]

    def parse(self):
        with open(self.filename) as fd:
            for line in fd:
                line = line.rstrip()
                

