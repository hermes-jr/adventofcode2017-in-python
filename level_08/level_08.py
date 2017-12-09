#!/usr/bin/env python
""" run as `python -O level_08.py` to disable debug garbage """

regs = {}
program = []
largestSeen = None
import re

with open('in.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if __debug__: print(line)
        program.append(line)


def getregval(reg):
    if reg not in regs:
        regs[reg] = 0
    return regs[reg]


def setregval(reg, val):
    global largestSeen
    regs[reg] = val
    if largestSeen == None or largestSeen < val:
        largestSeen = val


def chkcond(reg, operator, val):
    if operator == "==":
        return getregval(reg) == val
    elif operator == "<":
        return getregval(reg) < val
    elif operator == ">":
        return getregval(reg) > val
    elif operator == "<=":
        return getregval(reg) <= val
    elif operator == ">=":
        return getregval(reg) >= val
    elif operator == "!=":
        return getregval(reg) != val
    raise Exception("Unknown operator {}".format(operator))


cmdRe = re.compile(
    r"^([a-z]+) ([a-z]+) (-?[0-9]+) if ([a-z]+) ([=<>!]+) (-?[0-9]+)$")


def runprog():
    print("Running...")
    for line in program:
        matcher = cmdRe.match(line)
        tgtregname = matcher.group(1)
        op = matcher.group(2)
        opoperand = int(matcher.group(3))
        condregname = matcher.group(4)
        cond = matcher.group(5)
        condoperand = int(matcher.group(6))

        if __debug__: print(tgtregname, op, opoperand, condregname, cond, condoperand)
        if (chkcond(condregname, cond, condoperand)):
            if (op == "inc"):
                setregval(tgtregname, getregval(tgtregname) + opoperand)
            elif (op == "dec"):
                setregval(tgtregname, getregval(tgtregname) - opoperand)
            else:
                raise Exception("Unknown operation {}".format(op))

    if __debug__: print(regs)
    print("Result1: {}".format(max(tuple(regs.values()))))
    print("Result2: {}".format(largestSeen))


runprog()

u"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much memory to allocate to these operations. For example, in the above instructions, the highest value ever held was 10 (in register c after the third instruction was evaluated).

"""
