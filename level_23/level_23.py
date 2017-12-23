#!/usr/bin/env python
""" run as `python -O level_23.py` to disable debug garbage """

fname = "in.txt"

# Test
# fname = "testin.txt"

regs = {}
program = []

with open(fname, "r") as f:
    for line in f:
        line = line.strip()
        if __debug__: print(line)
        program.append(line)


def getregval(reg):
    if reg not in regs:
        regs[reg] = 0
    return regs[reg]


def setregval(reg, val):
    regs[reg] = val


def nameorval(decode):
    try:
        iv = int(decode)
        return iv
    except ValueError:
        return getregval(decode)


def runprog():
    result1 = 0
    print("Running...")
    ip = 0
    while True:
        # Out of bounds
        if ip >= len(program) or ip < 0:
            print("Program ends: ip is out of bounds")
            break

        # Step
        line = program[ip]
        if __debug__: print("ip: {} line: {} regs: {}".format(ip, line, regs))

        if line.startswith("sub"):
            tgt = line.split()[1]
            arg = nameorval(line.split()[2])
            setregval(tgt, getregval(tgt) - arg)
        elif line.startswith("set"):
            tgt = line.split()[1]
            arg = nameorval(line.split()[2])
            setregval(tgt, arg)
        elif line.startswith("add"):
            tgt = line.split()[1]
            arg = nameorval(line.split()[2])
            setregval(tgt, getregval(tgt) + arg)
        elif line.startswith("mul"):
            result1 += 1
            tgt = line.split()[1]
            arg = nameorval(line.split()[2])
            setregval(tgt, getregval(tgt) * arg)
        elif line.startswith("mod"):
            tgt = line.split()[1]
            arg = nameorval(line.split()[2])
            setregval(tgt, getregval(tgt) % arg)
        elif line.startswith("rcv"):
            arg = nameorval(line.split()[1])
            if (arg != 0):
                break
        elif line.startswith("jnz"):
            cmp = nameorval(line.split()[1])
            offs = nameorval(line.split()[2])
            if cmp != 0:
                if offs != 0:
                    ip += offs - 1
        ip += 1

    if __debug__: print(regs)
    print("Result1: {}".format(result1))


runprog()

u"""
--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems very similar, but some of the instructions are different:

    set X Y sets register X to the value of Y.
    sub X Y decreases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?

"""
