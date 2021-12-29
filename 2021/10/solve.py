#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    nav = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            nav.append(line)
    return nav

RIGHT  = {')': '(', ']': '[', '}': '{', '>': '<'}
LEFT = dict((b, a) for a, b in RIGHT.items())
SCORE  = {')': 3, ']': 57, '}': 1197, '>': 25137}


NAVSYSTEM = parse()

def syntaxcheck(line):
    stack = []
    for c in line:
        if c in RIGHT:
            assert len(stack)
            if stack[-1] != RIGHT[c]:
                return SCORE[c], stack
            else:
                stack.pop()
        elif c in LEFT:
            stack.append(c)
        else:
            assert False, 'backtrace overflow'
    return 0, stack

def one():
    print(sum(syntaxcheck(n)[0] for n in NAVSYSTEM))

def two():
    score  = {')': 1, ']': 2, '}': 3, '>': 4}
    totals = []
    for line in NAVSYSTEM:
        n, stack = syntaxcheck(line)
        if n != 0:
            continue
        missing = ''.join(LEFT[c] for c in reversed(stack))
        # print('{} - complete by adding {}'.format(line, missing))
        total = 0
        for c in missing:
            total = 5 * total + score[c]
        totals.append(total)

    assert(len(totals) & 1)
    totals = list(sorted(totals))
    print(totals[len(totals) // 2])

if __name__ == '__main__':
    one()
    two()
