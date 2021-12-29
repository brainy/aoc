#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    with open(sys.argv[1], 'rt') as f:
        return [int(n) for n in f.readline().strip().split(',')]


def one():
    fish = parse()
    for n in range(80):
        for i in range(len(fish)):
            if not fish[i]:
                fish[i] = 6
                fish.append(8)
            else:
                fish[i] -= 1
    print(len(fish))

def two():
    fish = parse()
    N = max(*fish)
    if N < 8:
        N = 8
    steps = [0] * (N + 1)
    for n in fish:
        steps[n] += 1

    for n in range(256):
        next = steps[0]
        steps[0] = 0
        for x in range(N):
            steps[x] += steps[x + 1]
            steps[x + 1] = 0
        steps[6] += next
        steps[8] += next

    print(sum(steps))

if __name__ == '__main__':
    one()
    two()
