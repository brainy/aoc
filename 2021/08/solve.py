#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    display = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if not len(line):
                continue
            pre, out = line.split('|')
            pre = tuple(pre.strip().split())
            out = tuple(out.strip().split())
            assert len(out) == 4
            display.append((pre, out))
    return display

UNIQUE = {2:1, 4:4, 3:7, 7:8}
DISPLAY = tuple(parse())

def one():
    known = 0
    for p, o in DISPLAY:
        for d in o:
            if len(d) in UNIQUE:
                known += 1
    print(known)

def decode(p, o):
    key = {}
    for d in p:
        k = UNIQUE.get(len(d), None)
        if k is not None:
            s = frozenset(d)
            assert k not in key or key[k] == s
            key[k] = s

    BD = key[4] - key[1]
    CF = key[1]
    BCDF = key[4]

    r = 0
    def append(n):
        nonlocal r
        r = 10 * r + n

    for d in o:
        k = UNIQUE.get(len(d), None)
        if k is not None:
            append(k)
            continue

        s = frozenset(d)
        if len(s) == 5:       # 2, 3, 5
            if len(s & BD) == 2:
                append(5)
            elif len(s & CF) == 2:
                append(3)
            else:
                assert len(CF - s) == 1
                append(2)
        else:                 # 0, 6, 9
            assert len(s) == 6
            if len(s | CF) == 7:
                append(6)
            elif len(s | BD) == 7:
                append(0)
            else:
                assert len(s - BCDF) == 2
                append(9)
    return r

def two():
    print(sum(decode(p, o) for p, o in DISPLAY))

if __name__ == '__main__':
    one()
    two()
