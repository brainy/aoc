#!/usr/bin/env python3

import os
import sys

def parse():
    assert len(sys.argv) == 2
    numbers = []
    maxwidth = 0
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            width = len(line)
            if width > maxwidth:
                maxwidth = width
            number = 0
            for d in line:
                number *= 2
                if d == '0':
                    pass
                elif d == '1':
                    number += 1
                else:
                    assert False, 'not a binary ' + line
            numbers.append(number)
    return maxwidth, numbers

MAXWIDTH, NUMBERS = parse()

def one():
    gamma = 0
    epsilon = 0
    maxwidth, numbers = MAXWIDTH, NUMBERS
    assert maxwidth > 1
    mask = 2 ** (maxwidth - 1)
    while mask > 0:
        ones = 0
        zeroes = 0
        for n in numbers:
            if n & mask:
                ones += 1
            else:
                zeroes += 1
        if ones > zeroes:
            gamma += mask
        else:
            epsilon += mask
        mask //= 2
    print(gamma * epsilon)

def two():
    maxwidth, numbers = MAXWIDTH, NUMBERS
    assert maxwidth > 1
    oxyset = set(numbers)
    co2set = set(numbers)
    mask = 2 ** (maxwidth - 1)
    oxy = None
    co2 = None
    while mask > 0:
        if oxy is None:
            ones = 0
            zeroes = 0
            for n in oxyset:
                if (n & mask) != 0:
                    ones += 1
                else:
                    zeroes += 1
            for n in oxyset.copy():
                thisbit = (n & mask) != 0
                if ones > zeroes:
                    if not thisbit:
                        oxyset.discard(n)
                elif zeroes > ones:
                    if thisbit:
                        oxyset.discard(n)
                else:
                    if not thisbit:
                        oxyset.discard(n)
                if len(oxyset) == 1:
                    oxy = oxyset.pop()

        if co2 is None:
            ones = 0
            zeroes = 0
            for n in co2set:
                if (n & mask) != 0:
                    ones += 1
                else:
                    zeroes += 1
            for n in co2set.copy():
                thisbit = (n & mask) != 0
                if ones < zeroes:
                    if not thisbit:
                        co2set.discard(n)
                elif zeroes < ones:
                    if thisbit:
                        co2set.discard(n)
                else:
                    if thisbit:
                        co2set.discard(n)
                if len(co2set) == 1:
                    co2 = co2set.pop()
        mask //= 2
    print(oxy * co2)

if __name__ == '__main__':
    one()
    two()
