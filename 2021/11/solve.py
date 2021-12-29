#!/usr/bin/env python3

import os
import sys

class Dumbo:
    def __init__(self, e):
        self.e = e
        self.adj = None

    def __str__(self):
        if self.adj is not None:
            return str(self.e)
        return '\x1b[1m\x1b[31m{}\x1b[0m'.format(self.e)


def parse(N = 10):
    assert len(sys.argv) == 2
    with open(sys.argv[1], 'rt') as f:
        field = []
        for y in range(N):
            ln = f.readline().strip()
            assert len(ln) == N
            field.append([Dumbo(int(e)) for e in ln])

    # for ln in field:
    #     for octo in ln:
    #         sys.stdout.write(str(octo))
    #     sys.stdout.write('\n')

    for y in range(N):
        for x in range(N):
            adj = set()
            if y > 0:
                adj.add(field[y - 1][x])
                if x > 0:
                    adj.add(field[y - 1][x - 1])
                if x < N - 1:
                    adj.add(field[y - 1][x + 1])
            if y < N - 1:
                adj.add(field[y + 1][x])
                if x > 0:
                    adj.add(field[y + 1][x - 1])
                if x < N - 1:
                    adj.add(field[y + 1][x + 1])
            if x > 0:
                adj.add(field[y][x - 1])
            if x < N - 1:
                adj.add(field[y][x + 1])
            field[y][x].adj = frozenset(adj)

    # for ln in field:
    #     for octo in ln:
    #         sys.stdout.write(str(octo))
    #     sys.stdout.write('\n')

    return field


field = parse(10)

def step():
    charged = set()
    for ln in field:
        for octo in ln:
            octo.e += 1
            if octo.e > 9:
                charged.add(octo)

    flashed = set()
    while len(charged):
        octo = charged.pop()
        if octo in flashed:
            continue
        for adj in octo.adj:
            adj.e += 1
            if adj.e > 9:
                charged.add(adj)
        flashed.add(octo)

    for octo in flashed:
        octo.e = 0

    return len(flashed)


def solve():
    flashed = 0
    sync = None
    for n in range(100):
        f = step()
        flashed += f
        if f == 100 and sync is None:
            sync = n + 1

    while sync is None:
        n += 1
        if step() == 100:
            sync = n + 1

    print(flashed)
    print(sync)


if __name__ == '__main__':
    solve()
