#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    field = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            row = [999]
            for c in line:
                row.append(int(c))
            row.append(999)
            field.append(row)
        for row in field:
            assert len(row) == len(field[0])
        field.insert(0, [999] * len(field[0]))
        field.append([999] * len(field[0]))
    return len(field[0]) - 2, len(field) - 2, field

W, H, FIELD = parse()
def localmin(x, y):
    v = FIELD[y][x]
    n = FIELD[y - 1][x]
    s = FIELD[y + 1][x]
    e = FIELD[y][x + 1]
    w = FIELD[y][x - 1]
    return v < n and v < s and v < e and v < w
localmins = None

def printfield(marks):
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            if (x, y) in marks:
                sys.stdout.write('\x1b[1m\x1b[31m{:d}\x1b[0m'.format(FIELD[y][x]))
            else:
                sys.stdout.write(str(FIELD[y][x]))
        sys.stdout.write('\n')


def one():
    mins = set()
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            if localmin(x, y):
                mins.add((x, y))

    # printfield(mins)

    print(sum(1 + FIELD[y][x] for x, y in mins))
    global localmins
    localmins = frozenset(mins)

def two():
    basins = []

    def rowscan(x, y):
        if FIELD[y][x] >= 9:
            return None
        h = x - 1
        while FIELD[y][h] < 9:
            h -= 1
        while FIELD[y][x] < 9:
            x += 1
        assert h < x
        return (h + 1, x)

    def scan(here, x0, x1, y):
        sections = []
        for x in range(x0, x1):
            if (x, y) in here:
                continue
            p = rowscan(x, y)
            if p is not None:
                sections.append(p)
        for x0, x1 in sections:
            for x in range(x0, x1):
                here.add((x, y))
        for x0, x1 in sections:
            scan(here, x0, x1, y - 1)
            scan(here, x0, x1, y + 1)

    def basin(x, y):
        here = set()
        p = rowscan(x, y)
        if p is None:
            return here
        x0, x1 = p

        for x in range(x0, x1):
            here.add((x, y))

        scan(here, x0, x1, y - 1)
        scan(here, x0, x1, y + 1)
        return here

    for x, y in localmins:
        basins.append(basin(x, y))

    # all = set()
    # for b in basins:
    #     all |= b
    # printfield(all)

    sizes = list(sorted(len(b) for b in basins))
    assert len(sizes) >= 3
    print(sizes[-1] * sizes[-2] * sizes[-3])


if __name__ == '__main__':
    one()
    two()
