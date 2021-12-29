#!/usr/bin/env python3

import os
import sys

__detval = 0
def reset():
    global __detval
    __detval = 0

def deterministic():
    global __detval
    roll = __detval + 1
    __detval = (__detval + 1) % 100
    return roll


def move(pos, shift):
    npos = (pos - 1 + shift) % 10 + 1
    return npos

def play(p1, p2, die, maxscore):
    reset()
    s1 = s2 = cast = 0

    while s1 < maxscore and s2 < maxscore:
        p1 = move(p1, die() + die() + die())
        s1 += p1
        cast += 3
        if s1 < maxscore:
            p2 = move(p2, die() + die() + die())
            s2 += p2
            cast += 3

    print(p1, s1, p2, s2, cast, 'result:', min(s1, s2) * cast)

def one():
    play(4, 8, deterministic, 1000)  # Example
    play(6, 7, deterministic, 1000)  # Input

splits = {}
for c1 in range(1, 4):
    for c2 in range(1, 4):
        for c3 in range(1, 4):
            n = c1 + c2 + c3
            if n not in splits:
                splits[n] = 1
            else:
                splits[n] += 1

class Player:
    def __init__(self, wins, winindex, position, score):
        self.wins = wins
        self.winindex = winindex
        self.position = position
        self.score = score

    def roll(self, amount, count, maxscore):
        npos = move(self.position, amount)
        if self.score + npos >= maxscore:
            self.wins[self.winindex] += count
            return None
        return Player(self.wins, self.winindex, npos, self.score + npos)


def dirac(p1, p2, maxscore):
    def step(pa, pb, start):
        for amount, count in splits.items():
            np = pa.roll(amount, start * count, maxscore)
            if np is not None:
                step(pb, np, start * count)

    wins = [0, 0]
    step(Player(wins, 0, p1, 0), Player(wins, 1, p2, 0), 1)
    if wins[0] > wins[1]:
        print('Player 1: {}'.format(wins[0]))
    else:
        print('Player 2: {}'.format(wins[1]))

def two():
    dirac(4, 8, 21)             # Example
    dirac(6, 7, 21)             # Input

if __name__ == '__main__':
    one()
    two()
