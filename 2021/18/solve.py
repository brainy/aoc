#!/usr/bin/env python3

import sys
from copy import deepcopy
from io import StringIO


def parse():
    assert len(sys.argv) == 2
    trees = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            trees.append(eval(line))
    assert len(trees) > 1
    return tuple(trees)


B = '\x1b[1m\x1b[34m'
R = '\x1b[1m\x1b[31m'
X = '\x1b[0m'
def fmt(n):
    s = StringIO()
    c = None
    def f(d, x):
        nonlocal c, s
        if isinstance(x, int):
            if x > 9:
                s.write(B)
            s.write(str(x))
            if x > 9:
                s.write(c if c is not None else X)
        else:
            if d == 4:
                c = R
                s.write(c)
            s.write('[')
            f(d + 1, x[0])
            s.write(', ')
            f(d + 1, x[1])
            s.write(']')
            if d == 4:
                c = None
                s.write(X)
    f(0, n)
    return s.getvalue()


def xplode(d, n, x):
    if not isinstance(x, list):
        return False
    assert len(x) == 2

    if len(d) < 4:
        return xplode(d + [(0, x)], n, x[0]) or xplode(d + [(1, x)], n, x[1])

    i0 = d[0][0]
    i1 = d[1][0]
    i2 = d[2][0]
    i3 = d[3][0]
    assert n[i0][i1][i2][i3] is x
    assert d[3][1][i3] is x

    left = x[0]
    right = x[1]
    assert isinstance(left, int)
    assert isinstance(right, int)

    for i, m in reversed(d):
        if i == 1:
            j = 0
            z = m
            while not isinstance(z[j], int):
                z = z[j]
                j = 1
            # print(fmt(m), z[j], '+=', left)
            z[j] += left
            break

    for i, m in reversed(d):
        if i == 0:
            j = 1
            z = m
            while not isinstance(z[j], int):
                z = z[j]
                j = 0
            # print(fmt(m), z[j], '+=', right)
            z[j] += right
            break

    n[i0][i1][i2][i3] = 0
    # print('xplode:', fmt(n))
    return True

def split(d, n, x):
    if not isinstance(x, list):
        return False
    assert len(x) == 2

    def split_value(i):
        nonlocal x
        value = x[i]
        if isinstance(value, int) and value >= 10:
            left = value // 2
            x[i] = [left, value - left]
            # print('split: ', fmt(n))
            return True
        return False

    return (split_value(0) or split(d + [(0, x)], n, x[0])
            or split_value(1) or split(d + [(1, x)], n, x[1]))

def reduce(n):
    assert isinstance(n, list) and len(n) == 2
    while True:
        if xplode([], n, n): continue
        if split([], n, n): continue
        break

def add(a, b):
    print('add:', fmt(a))
    print('   +', fmt(b))
    n = [deepcopy(a), deepcopy(b)]
    print(' -->', fmt(n))
    reduce(n)
    print('   = {}\n'.format(fmt(n)))
    return n

def magnitude(n):
    assert isinstance(n, list) and len(n) == 2
    if isinstance(n[0], int):
        left = n[0]
    else:
        left = magnitude(n[0])
    if isinstance(n[1], int):
        right = n[1]
    else:
        right = magnitude(n[1])
    return 3 * left + 2 * right


TREES = parse()

def one():
    n = TREES[0]
    for i in range(1, len(TREES)):
        n = add(n, TREES[i])
    print(magnitude(n))

def two():
    def allmagnitudes():
        for i in range(0, len(TREES)):
            for j in range(0, len(TREES)):
                if i == j: continue
                n = add(TREES[i], TREES[j])
                yield magnitude(n)
    print(max(m for m in allmagnitudes()))

if __name__ == '__main__':
    one()
    two()
