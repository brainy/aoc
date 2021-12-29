#!/usr/bin/env python3

import os
import sys

def parse(cmds):
    assert len(sys.argv) == 2
    steps = []
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            cmd, arg = line.split()
            steps.append((cmds[cmd], int(arg)))
    return steps

class State:
    def __init__(self):
        self.position = 0
        self.depth = 0
        self.aim = 0

def simple_forward(state, x):
    assert x >= 0
    state.position += x

def simple_down(state, x):
    assert x >= 0
    state.depth += x

def simple_up(state, x):
    assert x >= 0
    assert state.depth >= x
    state.depth -= x

def better_forward(state, x):
    assert x >= 0
    state.position += x
    state.depth += state.aim * x

def better_down(state, x):
    assert x >= 0
    state.aim += x

def better_up(state, x):
    assert x >= 0
    state.aim -= x

def one():
    steps = parse({'forward': simple_forward,
                   'down': simple_down,
                   'up': simple_up})
    state = State()
    for step in steps:
        step[0](state, step[1])
    print(state.position * state.depth)

def two():
    steps = parse({'forward': better_forward,
                   'down': better_down,
                   'up': better_up})
    state = State()
    for step in steps:
        step[0](state, step[1])
    print(state.position * state.depth)


if __name__ == '__main__':
    one()
    two()
