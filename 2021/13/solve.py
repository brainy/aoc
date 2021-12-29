#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    with open(sys.argv[1], 'rt') as f:
        dots = set()
        for line in f:
            line = line.strip()
            if not line:
                break
            x, y = line.split(',')
            dots.add((int(x), int(y)))

        fa = 'fold along '
        folds = []
        for line in f:
            if not line.startswith(fa):
                continue
            d, n = line[len(fa):].split('=')
            assert d in 'xy'
            folds.append((d, int(n)))

        # print(dots)
        # print(folds)
        return dots, folds

DOTS, FOLDS = parse()

def foldy(dots, n):
    D = dots.copy()
    for x, y in dots:
        if y < n:
            continue
        newy = 2 * n - y
        # print('({}, {}) -> ({}, {})'.format(x, y, x, newy))
        D.discard((x, y))
        D.add((x, newy))
    return D

def foldx(dots, n):
    D = dots.copy()
    for x, y in dots:
        if x < n:
            continue
        newx = 2 * n - x
        # print('({}, {}) -> ({}, {})'.format(x, y, newx, y))
        D.discard((x, y))
        D.add((newx, y))
    return D

def one():
    dots = DOTS.copy()
    firstfold = True
    for d, n in FOLDS:
        if d == 'x':
            dots = foldx(dots, n)
            # print('{}={} {}'.format(d, n, len(dots)))
        elif d == 'y':
            dots = foldy(dots, n)
            # print('{}={} {}'.format(d, n, len(dots)))
        else:
            assert False, 'wrong direction'
        if firstfold:
            print(len(dots))
            firstfold = False
    return dots

def two(dots):
    a = {}
    for x, y in dots:
        line = a.setdefault(y, [' '] * 200)
        line[x] = '#'

    for y in sorted(a):
        print(''.join(a[y]).strip())

if __name__ == '__main__':
    two(one())
