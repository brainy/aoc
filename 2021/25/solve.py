#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    east = set()
    south = set()
    X = None
    with open(sys.argv[1], 'rt') as f:
        Y = 0
        for line in f:
            x = 0
            line = line.strip()
            for c in line:
                assert c in ('v>.')
                if c == '>':
                    east.add((x, Y))
                elif c == 'v':
                    south.add((x, Y))
                x += 1
            if X is not None:
                assert X == x
            else:
                X = x
            Y += 1
    return east, south, X, Y

EAST, SOUTH, X, Y = parse()

def show(east, south):
    for y in range(Y):
        for x in range(X):
            c = (x, y)
            if c in east:
                sys.stdout.write(' >')
            elif x in south:
                sys.stdout.write(' v')
            else:
                sys.stdout.write(' .')
        sys.stdout.write('\n')

def onestep(east, south):
    moved = False
    neweast = set()
    for x, y in east:
        c = ((x + 1) % X, y)
        if c in east or c in south:
            neweast.add((x, y))
        else:
            neweast.add(c)
            moved = True
    newsouth = set()
    for x, y in south:
        c = (x, (y + 1) % Y)
        if c in neweast or c in south:
            newsouth.add((x, y))
        else:
            newsouth.add(c)
            moved = True
    return moved, neweast, newsouth

def one():
    steps = 0
    east = EAST
    south = SOUTH
    moved = True
    while moved:
        steps += 1
        # print(steps)
        # show(east, south)
        # print()
        moved, east, south = onestep(east, south)
    print(steps)

if __name__ == '__main__':
    one()
