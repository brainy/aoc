#!/usr/bin/env python3

import sys
from io import StringIO


def inp(stream, lineno, reg):
    stream.write('\n    /* line {}: inp {} */\n'.format(lineno, reg))
    stream.write('    assert(index < inlen && "[inp {}]");\n'.format(reg))
    stream.write('    {} = input[index++];\n'.format(reg))

def add(stream, lineno, reg, val):
    stream.write('\n    /* line {}: add {} {} */\n'.format(lineno, reg, val))
    if isinstance(val, int):
        if val == 0:
            stream.write('    /* noop */;\n')
            return
    stream.write('    {} += {};\n'.format(reg, val))

def mul(stream, lineno, reg, val):
    stream.write('\n    /* line {}: mul {} {} */\n'.format(lineno, reg, val))
    if isinstance(val, int):
        if val == 0:
            stream.write('    {} = 0;\n'.format(reg))
            return
        if val == 1:
            stream.write('    /* noop */;\n')
            return
    stream.write('    {} *= {};\n'.format(reg, val))

def div(stream, lineno, reg, val):
    stream.write('\n    /* line {}: div {} {} */\n'.format(lineno, reg, val))
    if not isinstance(val, int):
        stream.write('    assert({} != 0 && "[div {} {}]");\n'.format(val, reg, val))
    else:
        assert val != 0, '{}: division by zero'.format(lineno)
    if isinstance(val, int):
        if val == 1:
            stream.write('    /* noop */;\n')
            return
    stream.write('    {} /= {};\n'.format(reg, val))

def mod(stream, lineno, reg, val):
    stream.write('\n    /* line {}: mod {} {} */\n'.format(lineno, reg, val))
    stream.write('    assert({} >= 0 && "[mod {} {}]");\n'.format(reg, reg, val))
    if not isinstance(val, int):
        stream.write('    assert({} > 0 && "[mod {} {}]");\n'.format(val, reg, val))
    else:
        assert val > 0, '{}: modulo by non-positive'.format(lineno)
    if isinstance(val, int):
        if val == 1:
            stream.write('    {} = 0;\n'.format(reg))
            return
    stream.write('    {} %= {};\n'.format(reg, val))

def eql(stream, lineno, reg, val):
    stream.write('\n    /* line {}: eql {} {} */\n'.format(lineno, reg, val))
    if not isinstance(val, int):
        if reg == val:
            stream.write('    {} = 1;\n'.format(reg))
            return
    stream.write('    {} = ({} == {} ? 1 : 0);\n'.format(reg, reg, val))


OPEN = '''\
static long long
execute{:02d}(const long long* const restrict input, const size_t inlen, const long long z0)
{{
    size_t index = 0;

    long long w = 0;
    long long x = 0;
    long long y = 0;
    long long z = z0;
'''

CLOSE = '''\

    return z;
}

'''

def parse():
    assert len(sys.argv) == 2

    insnmap = {'inp': inp,
               'add': add,
               'mul': mul,
               'div': div,
               'mod': mod,
               'eql': eql}

    counter = 0;
    lineno = 0;
    program = StringIO()
    with open(sys.argv[1], 'rt') as f:
        for line in f:
            lineno += 1
            comment = line.find(';')
            if comment >= 0:
                line = line[:comment]
            line = line.rstrip()
            if not line:
                continue

            insn = line.split()
            N = len(insn)
            if N not in (2, 3):
                raise SyntaxError('{}: {}'.format(lineno, line))
            if insn[0] not in insnmap:
                raise SyntaxError('{}: {}'.format(lineno, line))
            if insn[1] not in 'wxyz':
                raise SyntaxError('{}: {}'.format(lineno, line))

            insn[0] = insnmap[insn[0]]
            if N == 2:
                if insn[0] is not inp:
                    raise SyntaxError('{}: {}'.format(lineno, line))
                if counter > 0:
                    program.write(CLOSE)
                program.write(OPEN.format(counter))
                counter += 1
            if N == 3 and insn[2] not in 'wxyz':
                try:
                    insn[2] = int(insn[2])
                except:
                    raise SyntaxError('{}: {}'.format(lineno, line))
            insn[0](program, lineno, *insn[1:])
    if counter > 0:
        program.write(CLOSE)
    return program.getvalue()

if __name__ == '__main__':
    print(parse())
