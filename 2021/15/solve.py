#!/usr/bin/env python3

import os
import sys


def parse():
    assert len(sys.argv) == 2
    w = None
    cave = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x = [int(c) for c in line]
            if w is None:
                w = len(x)
            assert w == len(x)
            cave.append(x)
    return cave

def N(v, cave, X, Y):
    x, y = v
    nbrs = set()
    if x > 0:
        nbrs.add(((x - 1, y), cave[y][x - 1]))
    if y > 0:
        nbrs.add(((x, y - 1), cave[y - 1][x]))
    if x < X - 1:
        nbrs.add(((x + 1, y), cave[y][x + 1]))
    if y < Y - 1:
        nbrs.add(((x, y + 1), cave[y + 1][x]))
    return nbrs

def H(n, cave):
    x, y = n
    return cave[y][x]

def aye_splat(cave):
    X = len(cave[0])
    Y = len(cave)
    start = (0, 0)
    stop = (X - 1, Y - 1)
    olist = set([start])
    clist = set([])
    g = {start: 0}
    parents = {start: start}

    while len(olist) > 0:
        n = None
        for v in olist:
            if n == None or g[v] + H(v, cave) < g[n] + H(n, cave):
                n = v;

        if n == None:
            return None

        if n == stop:
            path = []
            while parents[n] != n:
                path.append(n)
                n = parents[n]
            path.append(start)
            return reversed(path)

        for (m, weight) in N(n, cave, X, Y):
            if m not in olist and m not in clist:
                olist.add(m)
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n

                    if m in clist:
                        clist.remove(m)
                        olist.add(m)
        olist.remove(n)
        clist.add(n)
    return None

CAVE = parse()

def one():
    path = aye_splat(CAVE)
    if path is not None:
        print(sum(CAVE[y][x] for x, y in path) - CAVE[0][0])

def two():
    multicave = CAVE.copy()
    X = len(multicave[0])
    Y = len(multicave)

    def oneup(n, m):
        return (n - 1 + m) % 9 + 1

    for y in range(Y):
         for n in range(1, 5):
             multicave[y].extend([oneup(n, m) for m in multicave[y][:X]])

    for n in range(1, 5):
        for y in range(Y):
            multicave.append([oneup(n, m) for m in multicave[y]])

    # X = len(multicave[0])
    # Y = len(multicave)
    # print('multicave:', X, Y)

    path = aye_splat(multicave)
    if path is not None:
        print(sum(multicave[y][x] for x, y in path) - multicave[0][0])

if __name__ == '__main__':
    one()
    two()
