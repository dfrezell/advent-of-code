
#!/usr/bin/env python3

import sys
import re
import collections

class Robots(object):
    def __init__(self, xdim=101, ydim=103):
        self.xdim = xdim
        self.ydim = ydim
        self.bot = []
        self.vel = []
        self.pos = collections.defaultdict(list)
        self.time = 0
    
    def __str__(self) -> str:
        field = []
        for j in range(self.ydim):
            for i in range(self.xdim):
                if (i, j) in self.pos and len(self.pos[(i, j)]) > 0:
                    field.append(f"{len(self.pos[(i, j)])}")
                else:
                    field.append(".")
            field.append("\n")
        return f"t={self.time}\n-----------\n" + "".join(field) + "-----------"

    def add(self, pos, vel):
        self.bot.append(pos)
        self.vel.append(vel)
        self.pos[pos].append(len(self.bot)-1)

    def step(self):
        self.time += 1
        for i in range(len(self.bot)):
            self.pos[self.bot[i]].remove(i)
            self.bot[i] = ((self.bot[i][0] + self.vel[i][0]) % self.xdim, (self.bot[i][1] + self.vel[i][1]) % self.ydim)
            self.pos[self.bot[i]].append(i)

    def quads(self) -> tuple:
        mid_x = self.xdim // 2
        mid_y = self.ydim // 2
        
        # count the number of bots in each quadrant
        #  Q1 | Q2
        #  ---+---
        #  Q4 | Q3
        q1, q2, q3, q4 = 0, 0, 0, 0
        for keys in self.pos.keys():
            if keys[0] < mid_x and keys[1] < mid_y:
                q1 += len(self.pos[keys])
            elif keys[0] > mid_x and keys[1] < mid_y:
                q2 += len(self.pos[keys])
            elif keys[0] > mid_x and keys[1] > mid_y:
                q3 += len(self.pos[keys])
            elif keys[0] < mid_x and keys[1] > mid_y:
                q4 += len(self.pos[keys])

        return q1 * q2 * q3 * q4

def process_line(line:str, robots:Robots):
    lrex = r"p=(?P<x>\d+),(?P<y>\d+) v=(?P<vx>\-?\d+),(?P<vy>\-?\d+)"
    m = re.match(lrex, line)
    robots.add((int(m.group("x")), int(m.group("y"))), (int(m.group("vx")), int(m.group("vy"))))
    return 0

def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]
    xdim = int(sys.argv[2]) if len(sys.argv) > 2 else 101
    ydim = int(sys.argv[3]) if len(sys.argv) > 3 else 103

    robots = Robots(xdim, ydim)
    with open(fname) as fd:
        lines = fd.read().splitlines()
        for line in lines:
            process_line(line, robots)

    print(robots)
    for _ in range(100):
        robots.step()
    print(robots.quads())
    return 0

if __name__ == "__main__":
    sys.exit(main())