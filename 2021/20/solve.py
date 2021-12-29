#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    image = set()
    with open(sys.argv[1], 'rt') as f:
        algo = f.readline().strip()
        assert len(algo) == 512
        line = f.readline().strip()
        assert len(line) == 0
        y = -1
        for line in f:
            y += 1
            line = line.strip()
            if not len(line):
                break
            for x in range(len(line)):
                if line[x] == '#':
                    image.add((x, y))
                else:
                    assert line[x] == '.'
    algo = [1 if c == '#' else 0 for c in algo]
    return algo, frozenset(image)

ALGO, IMAGE = parse()

def limits(image):
    xmin = ymin = 999_999_999_999
    xmax = ymax = -xmin
    for x, y in image:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    return xmin, xmax, ymin, ymax

def enhance(image, step):
    xmin, xmax, ymin, ymax = limits(image)

    def value(x, y):
        if (x, y) in image:
            return 1
        if x < xmin or x > xmax or y < ymin or y > ymax:
            return ALGO[0] if step % 2 != 0 else 0
        return 0

    def getindex(x, y):
        index = 0
        index = (index << 1) + value(x - 1, y - 1)
        index = (index << 1) + value(x,     y - 1)
        index = (index << 1) + value(x + 1, y - 1)
        index = (index << 1) + value(x - 1, y)
        index = (index << 1) + value(x,     y)
        index = (index << 1) + value(x + 1, y)
        index = (index << 1) + value(x - 1, y + 1)
        index = (index << 1) + value(x,     y + 1)
        index = (index << 1) + value(x + 1, y + 1)
        assert index < 512
        return index

    result = set()
    for y in range(ymin - 1, ymax + 2):
        for x in range(xmin - 1, xmax + 2):
            index = getindex(x, y)
            if ALGO[index]:
                result.add((x, y))
    return result

def pprint(image):
    xmin, xmax, ymin, ymax = limits(image)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            sys.stdout.write(' #' if (x, y) in image else ' .')
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    pass

def one():
    result = IMAGE
    # pprint(result)
    for step in range(2):
        result = enhance(result, step)
        # pprint(result)
    print(len(result))

def two():
    result = IMAGE
    # pprint(result)
    for step in range(50):
        result = enhance(result, step)
        # pprint(result)
    print(len(result))

if __name__ == '__main__':
    one()
    two()
