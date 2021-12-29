#!/usr/bin/env python3

import os
import sys

class Point:
    __slots__ = ('_x', '_y')
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

class Line:
    __slots__ = ('_p1', '_p2')
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self):
        return self._p1
    @property
    def p2(self):
        return self._p2
    @property
    def horizontal(self):
        return self._p1.y == self._p2.y
    @property
    def vertical(self):
        return self._p1.x == self._p2.x


def parse():
    assert len(sys.argv) == 2
    lines = []
    xmax = 0
    ymax = 0

    def maxx(x):
        nonlocal xmax
        if x > xmax: xmax = x
    def maxy(y):
        nonlocal ymax
        if y > ymax: ymax = y

    with open(sys.argv[1], 'rt') as f:
        for text in f:
            text = text.strip()
            if len(text) == 0:
                continue
            p1, to, p2 = text.split()
            assert to == '->'
            p1 = Point(*(int(n) for n in p1.split(',')))
            p2 = Point(*(int(n) for n in p2.split(',')))
            maxx(p1.x)
            maxx(p2.x)
            maxy(p1.y)
            maxy(p2.y)
            lines.append(Line(p1, p2))
    return lines, Point(xmax, ymax)

def paint(field, pmax, silent):
    danger = 0
    for y in range(pmax.y + 1):
        for x in range(pmax.x + 1):
            v = field[y][x]
            assert v >= 0
            if v > 1:
                danger += 1
            if not silent:
                if v == 0:
                    sys.stdout.write(' .')
                elif v == 1:
                    sys.stdout.write(' 1')
                else:
                    sys.stdout.write('\x1b[1m\x1b[31m{:>2d}\x1b[0m'.format(v))
        if not silent:
            sys.stdout.write('\n')
    return danger

def draw(lines, pmax, diagonal):
    cols = pmax.x + 1
    rows = pmax.y + 1
    row = [0] * cols
    field = []
    for x in range(rows + 1):
        field.append(row.copy())
    for line in lines:
        if line.horizontal:
            y = line.p1.y
            x1 = min(line.p1.x, line.p2.x)
            x2 = max(line.p1.x, line.p2.x)
            for x in range(x1, x2 + 1):
                field[y][x] += 1
        elif line.vertical:
            x = line.p1.x
            y1 = min(line.p1.y, line.p2.y)
            y2 = max(line.p1.y, line.p2.y)
            for y in range(y1, y2 + 1):
                field[y][x] += 1
        elif diagonal:
            if line.p1.x < line.p2.x:
                p1 = line.p1
                p2 = line.p2
            else:
                p1 = line.p2
                p2 = line.p1
            assert p2.x - p1.x == abs(p2.y - p1.y)
            y = p1.y
            for x in range(p1.x, p2.x + 1):
                field[y][x] += 1
                if p1.y < p2.y:
                    y += 1
                else:
                    y -= 1
    return field


def one():
    lines, pmax = parse()
    field = draw(lines, pmax, False)
    danger = paint(field, pmax, True)
    print(danger)

def two():
    lines, pmax = parse()
    field = draw(lines, pmax, True)
    danger = paint(field, pmax, True)
    print(danger)

if __name__ == '__main__':
    one()
    two()
