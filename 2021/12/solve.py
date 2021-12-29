#!/usr/bin/env python3

import os
import sys
from collections import defaultdict

class Node:
    def __init__(self, name):
        self.name = name
        self.small = (name == name.lower())
        self.out = set()

    def __repr__(self):
        return '{} -> {}'.format(self.name, repr(self.out))

def parse():
    assert len(sys.argv) == 2
    nodes = {}
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            try:
                name, out = line.strip().split('-')
            except:
                continue
            node = nodes.setdefault(name, Node(name))
            node.out.add(out)
            edon = nodes.setdefault(out, Node(out))
            edon.out.add(name)
    return nodes

NODES = parse()

def findmore(paths, path, node, visited, maxvisit):
    if node.small and node.name in visited and visited[node.name] > maxvisit:
        return

    path.append(node.name)
    if node.name == 'end':
        # print(','.join(path))
        paths.append(path)
        return

    if node.small:
        visited[node.name] += 1
        if visited[node.name] > maxvisit:
            maxvisit = 0

    for name in node.out:
        findmore(paths, path.copy(), NODES[name], visited.copy(), maxvisit)

def findpath(maxvisit):
    assert maxvisit in (1, 2)
    paths = []
    node = NODES['start']
    visited = defaultdict(lambda: 0, {node.name: 2})
    for name in node.out:
        findmore(paths, [node.name], NODES[name], visited.copy(), maxvisit - 1)
    print(len(paths))


def one():
    findpath(1)

def two():
    findpath(2)

if __name__ == '__main__':
    one()
    two()
