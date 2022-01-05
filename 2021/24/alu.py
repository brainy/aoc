#!/usr/bin/env python3
"""Generic ALU."""


class ALU:
    __slots__ = ['w', 'x', 'y', 'z', 'data']

    def __init__(self, data):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.data = (int(d) for d in data)

    def __str__(self):
        return('w: {} x: {} y: {} z: {}'.format(self.w, self.x, self.y, self.z))

    def inp(self, reg, val):
        setattr(self, reg, val)

    def add(self, reg, val):
        if not isinstance(val, int):
            val = getattr(self, val)
        regval = getattr(self, reg)
        setattr(self, reg, regval + val)

    def mul(self, reg, val):
        if not isinstance(val, int):
            val = getattr(self, val)
        regval = getattr(self, reg)
        setattr(self, reg, regval * val)

    def div(self, reg, val):
        if not isinstance(val, int):
            val = getattr(self, val)
        assert val != 0
        regval = getattr(self, reg)
        setattr(self, reg, regval // val)

    def mod(self, reg, val):
        if not isinstance(val, int):
            val = getattr(self, val)
        assert val > 0
        regval = getattr(self, reg)
        assert regval >= 0
        setattr(self, reg, regval % val)

    def eql(self, reg, val):
        if not isinstance(val, int):
            val = getattr(self, val)
        regval = getattr(self, reg)
        setattr(self, reg, int(regval == val))

    def run(self, program):
        for insn in program:
            if insn[0] == ALU.inp:
                self.inp(insn[1], next(self.data))
            else:
                insn[0](self, insn[1], insn[2])


def parse(path):
    IMAP = {'inp': ALU.inp,
            'add': ALU.add,
            'mul': ALU.mul,
            'div': ALU.div,
            'mod': ALU.mod,
            'eql': ALU.eql}

    with open(path, 'rt') as f:
        for line in f:
            comment = line.find(';')
            if comment >= 0:
                line = line[:comment]
            line = line.rstrip()
            if not line:
                continue
            insn = line.split()
            N = len(insn)
            insn[0] = IMAP[insn[0]]
            if N == 2:
                assert insn[0] == ALU.inp
            elif N != 3:
                raise SyntaxError(line)
            if insn[1] not in 'wxyz':
                raise SyntaxError(line)
            if N == 3 and insn[2] not in 'wxyz':
                insn[2] = int(insn[2])
            yield insn


if __name__ == '__main__':
    import sys
    assert len(sys.argv) > 1
    alu = ALU([int(sys.argv[i]) for i in range(2, len(sys.argv))])
    alu.run(parse(sys.argv[1]))
    print(str(alu))
