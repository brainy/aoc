#!/usr/bin/env python3

import os
import sys

SIZE = 5

class Board:
    class RowCol:
        def __init__(self):
            self.hits = 0
            self.cells = set()
            self.order = []

        def __str__(self) -> str:
            assert len(self.order) == SIZE
            return '{!s:s} {!s:s} {!s:s} {!s:s} {!s:s}'.format(
                self.order[0], self.order[1], self.order[2], self.order[3], self.order[4])

        def add(self, cell, attr: str):
            assert cell not in self.cells
            assert len(self.cells) < SIZE
            assert getattr(cell, attr) is self
            self.cells.add(cell)
            self.order.append(cell)

        def validate(self):
            assert len(self.cells) == SIZE

        @property
        def complete(self) -> bool:
            return self.hits >= len(self.cells)

        def draw(self, cell) -> bool:
            assert cell in self.cells
            cell.hit = True
            self.hits += 1
            return self.complete

    class Cell:
        def __init__(self, x: int, row, col):
            self.value = x
            self.hit = False
            self.row = row
            self.col = col
            row.add(self, 'row')
            col.add(self, 'col')

        def __hash__(self) -> int:
            return self.value

        def __eq__(self, value) -> bool:
            if isinstance(value, self.__class__):
                return self is value or self.value == value.value
            elif isinstance(value, int):
                return self.value == value
            assert False, 'wrong type for eq'

        def __str__(self) -> str:
            if self.hit:
                return '\x1b[1m\x1b[31m{:>2d}\x1b[0m'.format(self.value)
            else:
                return '{:>2d}'.format(self.value)


    def __init__(self, numbers: list[int]):
        assert len(numbers) == SIZE * SIZE
        self.cells = {}
        self.unmarked = set()
        self.rows = [self.RowCol(), self.RowCol(), self.RowCol(), self.RowCol(), self.RowCol()]
        self.cols = [self.RowCol(), self.RowCol(), self.RowCol(), self.RowCol(), self.RowCol()]

        index = -1
        for i in range(SIZE):
            for j in range(SIZE):
                index += 1
                assert index < len(numbers)
                cell = self.Cell(numbers[index], self.rows[i], self.cols[j])
                assert cell not in self.cells
                self.cells[cell.value] = cell
                self.unmarked.add(cell)

        for row in self.rows:
            row.validate()
        for col in self.cols:
            col.validate()

    def __str__(self) -> str:
        assert len(self.rows) == SIZE
        return '{!s:s}\n{!s:s}\n{!s:s}\n{!s:s}\n{!s:s}'.format(
            self.rows[0], self.rows[1], self.rows[2], self.rows[3], self.rows[4])

    def draw(self, x: int) -> bool:
        if x not in self.cells:
            return False
        cell = self.cells[x]
        self.unmarked.remove(cell)
        return cell.row.draw(cell) or cell.col.draw(cell)

    @property
    def summary(self) -> int:
        return sum(cell.value for cell in self.unmarked)


def parse_board(lines, numbers, boards, bmap):
    assert len(lines) >= SIZE
    contents = []
    for n in range(SIZE):
        row = list(int(n) for n in lines.pop(0).strip().split())
        assert len(row) == SIZE
        contents.extend(row)

    if len(lines):
        assert len(lines.pop(0).strip()) == 0

    board = Board(contents)
    for n in numbers:
        if n not in bmap:
            bmap[n] = set()
        bmap[n].add(board)
    board.index = len(boards)
    boards.append(board)

def parse():
    assert len(sys.argv) == 2
    numbers = []
    boards = []
    bmap = {}
    with open(sys.argv[1], 'rt') as f:
        lines = f.readlines()
    numbers = list(int(n) for n in lines.pop(0).strip().split(','))
    assert len(lines.pop(0).strip()) == 0
    while len(lines):
            parse_board(lines, numbers, boards, bmap)
    return numbers, boards, bmap

def printboard(x, board):
    summary = board.summary
    print('{} num={} sum={} score={}'.format(board.index, x, summary, summary * x))
    print('{!s:s}\n'.format(board))

def solve():
    numbers, boards, bmap = parse()
    firstwin = False
    lastwins = None
    lastdraw = None
    for x in numbers:
        wins = set()
        for board in bmap[x]:
            if board.draw(x):
                wins.add(board)
        if len(wins):
            if not firstwin:
                print('First win:')
                for board in wins:
                    printboard(x, board)
                firstwin = True
            for board in wins:
                for n in board.cells.keys():
                    bmap[n].discard(board)
                if board.summary > 0:
                    lastwins = wins
                    lastdraw = x
    assert lastwins is not None
    print('Last win:')
    for board in lastwins:
        printboard(lastdraw, board)

if __name__ == '__main__':
    solve()
