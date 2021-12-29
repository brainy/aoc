#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    sequence = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            xmin = xmax = None
            ymin = ymax = None
            zmin = zmax = None
            what, where = line.split()
            for interval in where.split(','):
                c, rest = interval.split('=')
                rmin, rmax = rest.split('..')
                if c == 'x':
                    xmin, xmax = int(rmin), int(rmax)
                elif c == 'y':
                    ymin, ymax = int(rmin), int(rmax)
                elif c == 'z':
                    zmin, zmax = int(rmin), int(rmax)
                else:
                    raise IndexError(c)
            where = Region(xmin, xmax, ymin, ymax, zmin, zmax)
            if what == 'on':
                sequence.append((True, where))
            elif what == 'off':
                sequence.append((False, where))
            else:
                raise ValueError(what)
    return sequence


class Region:
    __slots__ = ('xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax', 'volume')

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        assert xmin <= xmax and ymin <= ymax and zmin <= zmax
        self.volume = (xmax - xmin + 1) * (ymax - ymin + 1) * (zmax - zmin + 1)
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def copy(self):
        return Region(self.xmin, self.xmax,
                      self.ymin, self.ymax,
                      self.zmin, self.zmax)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '[[{}..{}, {}..{}, {}..{} = {}]]'.format(self.xmin, self.xmax,
                                                        self.ymin, self.ymax,
                                                        self.zmin, self.zmax,
                                                        self.volume)

    def __hash__(self):
        return hash((self.xmin, self.xmax,
                     self.ymin, self.ymax,
                     self.zmin, self.zmax))

    def __eq__(self, other):
        return (    self.xmin == other.xmin and self.xmax == other.xmax
                and self.ymin == other.ymin and self.ymax == other.ymax
                and self.zmin == other.zmin and self.zmax == other.zmax)

    def intersection(self, other):
        if (   other.xmax < self.xmin
            or other.xmin > self.xmax
            or other.ymax < self.ymin
            or other.ymin > self.ymax
            or other.zmax < self.zmin
            or other.zmin > self.zmax):
            return None, None

        sct = Region(max(self.xmin, other.xmin), min(self.xmax, other.xmax),
                     max(self.ymin, other.ymin), min(self.ymax, other.ymax),
                     max(self.zmin, other.zmin), min(self.zmax, other.zmax))

        bits = []
        res = self.copy()
        if sct.xmin > res.xmin:
            bits.append(Region(res.xmin, sct.xmin - 1,
                               res.ymin, res.ymax,
                               res.zmin, res.zmax))
            res.xmin = sct.xmin
        if sct.xmax < res.xmax:
            bits.append(Region(sct.xmax + 1, res.xmax,
                               res.ymin, res.ymax,
                               res.zmin, res.zmax))
            res.xmax = sct.xmax

        if sct.ymin > res.ymin:
            bits.append(Region(res.xmin, res.xmax,
                               res.ymin, sct.ymin - 1,
                               res.zmin, res.zmax))
            res.ymin = sct.ymin
        if sct.ymax < res.ymax:
            bits.append(Region(res.xmin, res.xmax,
                               sct.ymax + 1, res.ymax,
                               res.zmin, res.zmax))
            res.ymax = sct.ymax

        if sct.zmin > res.zmin:
            bits.append(Region(res.xmin, res.xmax,
                               res.ymin, res.ymax,
                               res.zmin, sct.zmin - 1))
            res.zmin = sct.zmin
        if sct.zmax < res.zmax:
            bits.append(Region(res.xmin, res.xmax,
                               res.ymin, res.ymax,
                               sct.zmax + 1, res.zmax))
            res.zmax = sct.zmax
        assert len(bits) <= 6
        assert sct == res
        return sct, bits


SEQUENCE = parse()
REGION = Region(-50, 50, -50, 50, -50, 50)

def solve(region):
    cubes = set()
    for onoff, r in SEQUENCE:
        if region is not None:
            r, _ = REGION.intersection(r)
            if r is None:
                continue
        if onoff:
            pieces = [r]
            for c in cubes:
                newpieces = []
                for p in pieces:
                    n, bits = p.intersection(c)
                    if n is None:
                        newpieces.append(p)
                    else:
                        newpieces.extend(bits)
                pieces = newpieces
            for p in pieces:
                cubes.add(p)
        else:
            newcubes = set()
            for c in cubes:
                n, bits = c.intersection(r)
                if n is None:
                    newcubes.add(c)
                else:
                    for p in bits:
                        newcubes.add(p)
            cubes = newcubes
    print(sum(c.volume for c in cubes))


if __name__ == '__main__':
    solve(REGION)
    solve(None)
