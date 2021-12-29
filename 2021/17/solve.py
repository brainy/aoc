#!/usr/bin/env python3

import os
import sys


# Example:
XMIN = 20
XMAX = 30
YMIN = -10
YMAX = -5

# Input:
# XMIN = 143
# XMAX = 177
# YMIN = -106
# YMAX = -71

def dist(x):
    return x * (x + 1) // 2


def one():
    steps = 1
    while dist(steps) < XMIN:
        steps += 1

    xset = []
    while dist(steps) <= XMAX:
        xset.append(steps)
        print('x', steps, dist(steps))
        steps += 1

    minstep = min(xset)
    maxstep = max(xset)

    heights = {}

    for x0 in range(minstep, maxstep + 1):
        for y0 in range(1, 200):
            h = y = y0 * (y0 + 1) // 2
            v = 0
            while y >= YMIN:
                y -= v
                v += 1
                if y >= YMIN and y <= YMAX:
                    heights.setdefault(h, [])
                    heights[h].append((x0, y0, h, y))
                if y < YMIN:
                    break

    h = max(n for n in heights)
    print(repr(heights[h]))


def shot(vx, vy):
    x = y = 0
    while x <= XMAX and y >= YMIN:
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        vy -= 1
        if x >= XMIN and x <= XMAX and y >= YMIN and y <= YMAX:
            return 1
    return 0

def two():
    target = 0
    for x0 in range(1, XMAX + 1):
        for y0 in range(YMIN, 200):
            target += shot(x0, y0)
    print(target)

if __name__ == '__main__':
    one()
    two()
