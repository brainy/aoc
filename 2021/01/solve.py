#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    scan = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if len(line):
                scan.append(int(line))
    return scan

SCAN = parse()

def solve(scan):
    prev = None
    count = 0
    for depth in scan:
        if prev is not None:
            if depth > prev:
                count += 1
        prev = depth
    return count

def one():
    print(solve(SCAN))

def two():
    assert len(SCAN) >= 3
    slide = []
    for i in range(len(SCAN) - 2):
        slide.append(SCAN[i] + SCAN[i+1] + SCAN[i+2])
    print(solve(slide))

if __name__ == '__main__':
    one()
    two()
