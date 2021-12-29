#!/usr/bin/env python3

import os
import math
import re
import sys
from collections import defaultdict
from pprint import pprint, pformat

def parse():
    start = re.compile('^--- scanner (\d+) ---$')
    assert len(sys.argv) == 2
    scanners = {}
    points = None
    num = None
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = start.match(line)
            if m is not None:
                if num is not None and points is not None:
                    scanners[num] = Scanner(num, points)
                points = []
                num = int(m.group(1))
                assert num not in scanners
            else:
                x, y, z = line.split(',')
                points.append((int(x), int(y), int(z)))
    assert num is not None and points is not None
    scanners[num] = Scanner(num, points)
    for n in range(len(scanners)):
        assert n in scanners
    return scanners


class Vector:
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def manhattan(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def rotx(self):
        self.y, self.z = self.z, -self.y

    def roty(self):
        self.z, self.x = self.x, -self.z

    def roty2(self):
        self.z, self.x = -self.z, -self.x

    def rotz(self):
        self.x, self.y = self.y, -self.x

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, v):
        return self is v or (self.x == v.x and self.y == v.y and self.z == v.z)

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def __repr__(self):
        return str(self)


class Scanner:
    def __init__(self, num, points):
        self.num = num
        self.beacons = tuple(Vector(x, y, z) for x, y, z in points)
        self.__dist = None
        self.__R = None

    def copy(self):
        return Scanner(self.num, ((b.x, b.y, b.z) for b in self.beacons))

    def __distances(self):
        rel = defaultdict(lambda: set())
        for a in self.beacons:
            for b in self.beacons:
                if a is not b:
                    rel[a].add(b - a)
        return rel

    @property
    def distances(self):
        if self.__dist is None:
            self.__dist = self.__distances()
        return self.__dist

    @property
    def R(self):
        assert self.__R is not None
        return self.__R

    def move(self, r):
        assert self.__R is None
        self.__R = r
        for b in self.beacons:
            n = r + b
            b.x, b.y, b.z = n.x, n.y, n.z

    def rotx(self):
        self.__dist = None
        for b in self.beacons:
            b.rotx()

    def roty(self):
        self.__dist = None
        for b in self.beacons:
            b.roty()

    def roty2(self):
        self.__dist = None
        for b in self.beacons:
            b.roty2()

    def rotz(self):
        self.__dist = None
        for b in self.beacons:
            b.rotz()

    def __eq__(self, s):
        return self is s or (self.num == s.num and self.beacons == s.beacons)


def match(s1, s2):
    def check(s1, s2):
        matches = set()
        for a, aset in s1.distances.items():
            for b, bset in s2.distances.items():
                if len(aset & bset) >= 11:
                    matches.add((a, b))
            if len(matches):
                # print(len(matches), pformat(matches))
                return matches, s2
        return None, None

    def rotate(s1, s2):
        for zrot in range(4):
            matches, sentinel = check(s1, s2)
            if matches is not None:
                return matches, sentinel
            s2.rotz()
        return None, None

    sprime = s2.copy()
    for xrot in range(4):
        matches, sentinel = rotate(s1, sprime)
        if matches is not None:
            return matches, sentinel
        sprime.rotx()
    sprime.roty()
    matches, sentinel = rotate(s1, sprime)
    if matches is not None:
        return matches, sentinel
    sprime.roty2()
    matches, sentinel = rotate(s1, sprime)
    if matches is not None:
        return matches, sentinel
    sprime.roty()
    assert sprime == s2
    return None, None

SCANNERS = parse()

def onematch(done, todo, checked):
    nextcheck = list(sorted(set(done.keys()) - checked))
    print('done:', list(sorted(done.keys())))
    print('todo:', list(sorted(todo.keys())))
    print('next:', nextcheck)
    assert nextcheck
    for m in nextcheck:
        s0 = done[m]
        for n in list(sorted(todo.keys())):
            assert n != s0.num
            assert n not in done
            matches, s = match(s0, todo[n])
            if matches is None:
                continue
            R = None
            for a, b in matches:
                r = a - b
                if R is not None:
                    assert r == R
                R = r
            print(s0.num, '->', n, R, len(matches))
            s.move(R)
            assert sum(1 if b in s0.beacons else 0 for b in s.beacons) >= 12
            done[n] = s
            del todo[n]
        checked.add(m)

def one():
    todo = {k: s.copy() for k, s in SCANNERS.items()}
    done = {0: todo[0]}
    done[0].move(Vector(0, 0, 0))
    del todo[0]

    checked = set()
    while len(todo):
        onematch(done, todo, checked)

    assert len(done) == len(SCANNERS)
    beacons = set()
    for s in done.values():
        for b in s.beacons:
            beacons.add(b)
    print(len(beacons))
    two(done)

def two(done):
    taxi = set()
    for s in done.values():
        for t in done.values():
            if s is not t:
                taxi.add((t.R - s.R).manhattan())
    print(max(taxi))

if __name__ == '__main__':
    one()
