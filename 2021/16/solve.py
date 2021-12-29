#!/usr/bin/env python3

import os
import sys

HEXBIN = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

def parse():
    assert len(sys.argv) == 2
    if sys.argv[1] == '-':
        f = sys.stdin
    else:
        f = open(sys.argv[1], 'rt')

    line = f.readline().strip()
    for c in line:
        assert c in HEXBIN
        for b in HEXBIN[c]:
            yield b


def solve():
    stream = parse()
    bitcount = 0
    def getbit():
        nonlocal stream, bitcount
        c = next(stream)
        bitcount += 1
        return int(c)

    def skip(count):
        for _ in range(count):
            getbit()

    def number(start, count):
        for _ in range(count):
            start = (start << 1) + getbit()
        return start

    versions = []
    def unpack(total_length=None, packet_count=None):
        nonlocal bitcount, versions
        stream_start = bitcount
        packets = []

        if total_length is None:
            assert packet_count is not None
            iterate = lambda: len(packets) < packet_count
        elif packet_count is None:
            assert total_length is not None
            iterate = lambda: bitcount - stream_start < total_length
        else:
            assert False, 'bad total lenght/packet_count combo'

        while iterate():
            version = number(0, 3)
            versions.append(version)
            typeid = number(0, 3)
            if typeid == 4:     # literal
                more = True
                literal = 0
                while more:
                    more = getbit()
                    literal = number(literal, 4)
                packets.append(literal)
                continue

            # operators
            lenid = getbit()
            if lenid == 0:
                subpackets = unpack(total_length=number(0, 15))
            else:
                subpackets = unpack(packet_count=number(0, 11))

            if typeid == 0:     # sum
                assert len(subpackets) > 0
                packets.append(sum(subpackets))
            elif typeid == 1:   # product
                assert len(subpackets) > 0
                n = 1
                for m in subpackets:
                    n *= m
                packets.append(n)
            elif typeid == 2:   # min
                packets.append(min(subpackets))
            elif typeid == 3:   # max
                packets.append(max(subpackets))
            elif typeid == 5:   # gt
                assert len(subpackets) == 2
                packets.append(1 if subpackets[0] > subpackets[1] else 0)
            elif typeid == 6:   # lt
                assert len(subpackets) == 2
                packets.append(1 if subpackets[0] < subpackets[1] else 0)
            elif typeid == 7:   # eq
                assert len(subpackets) == 2
                packets.append(1 if subpackets[0] == subpackets[1] else 0)
            else:
                assert False

        if total_length is not None:
            # print('L', total_length, bitcount, stream_start, bitcount - stream_start)
            assert total_length == bitcount - stream_start
        # if packet_count is not None:
            # print('S', packet_count, packet_count)
        return packets

    pkt = unpack(packet_count=1)
    while bitcount % 4:
        assert getbit() == 0
    assert len(pkt) == 1
    print(sum(versions))
    print(pkt[0])


if __name__ == '__main__':
    solve()
