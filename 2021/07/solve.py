#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    with open(sys.argv[1], 'rt') as f:
        positions = [int(n) for n in f.readline().strip().split(',')]
    crabs = [0] * (max(positions) + 1)
    for i in positions:
        crabs[i] += 1
    return crabs


def one():
    def value(crabs, index):
        cost = 0
        for i in range(len(crabs)):
            distance = i > index and i - index or index - i
            cost += crabs[i] * distance
        return cost

    crabs = parse()
    mincost = min(value(crabs, i) for i in range(len(crabs)))
    print(mincost)

def two():
    def value(crabs, index):
        cost = 0
        for i in range(len(crabs)):
            distance = i > index and i - index or index - i
            cost += crabs[i] * (distance * (distance + 1) // 2)
        return cost

    crabs = parse()
    mincost = min(value(crabs, i) for i in range(len(crabs)))
    print(mincost)

if __name__ == '__main__':
    one()
    two()
