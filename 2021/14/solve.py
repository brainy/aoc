#!/usr/bin/env python3

import os
import sys
from collections import defaultdict

def parse():
    assert len(sys.argv) == 2
    with open(sys.argv[1], 'rt') as f:
        template = f.readline().strip()
        assert len(template) > 1
        assert len(f.readline().strip()) == 0
        rules = {}
        for line in f:
            line = line.strip()
            if not line:
                continue
            pair, sep, ins = line.strip().split()
            assert sep == '->'
            assert pair not in rules
            rules[pair] = ins
    return template, rules

TEMPLATE, RULES = parse()

def enpair(tpl):
    pairs = defaultdict(lambda: 0)
    for i in range(len(tpl) - 1):
        pairs[tpl[i:i+2]] += 1
    # print(repr(pairs))
    return pairs

def step(N):
    # print(TEMPLATE)
    pairs = enpair(TEMPLATE)
    count = defaultdict(lambda: 0)
    for c in TEMPLATE:
        count[c] += 1
    # print(repr(count))

    for _ in range(N):
        new = defaultdict(lambda: 0)
        for pair, cnt in pairs.items():
            c = RULES[pair]
            count[c] += cnt
            new[pair[0] + c] += cnt
            new[c + pair[1]] += cnt
        pairs = new

    # print(repr(pairs))
    # print(sum(pairs.values()))
    # print(repr(count))

    minc = ''
    mink = None
    maxc = ''
    maxk = None
    for c,n in count.items():
        if mink is None or n < mink:
            mink = n
            minc = c
        if maxk is None or n > maxk:
            maxk = n
            maxc = c

    # print('{} -> {}'.format(minc, mink))
    # print('{} -> {}'.format(maxc, maxk))
    print(maxk - mink)
    # print(sum(count.values()))

def one():
    step(10)

def two():
    step(40)

if __name__ == '__main__':
    one()
    two()
