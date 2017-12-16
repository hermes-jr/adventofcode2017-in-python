#!/usr/bin/env python
""" run as `python -O level_16.py` to disable debug garbage """

import re

spinp = re.compile("^s([0-9]+)$")
exchp = re.compile("^x([0-9]+)/([0-9]+)$")
partp = re.compile("^p([a-p])/([a-p])$")

with open('in.txt', 'r') as f:
    for line in f:
        ops = list(line.split(","))

if __debug__: print(ops)

progs = list(map(chr, range(97, 113)))

# Test
# progs = list(map(chr, range(97, 102)))
# ops = ["s1", "x3/4", "pe/b"]

seenbefore = {}

for i in range(0, 1_000_000_000):
    snp = tuple(progs)
    if seenbefore.keys() and snp in seenbefore.keys():
        if __debug__: print("getting cached: {} {}".format(snp, seenbefore[snp]))
        progs = seenbefore.get(snp)
        continue
    instate = progs
    for cmd in ops:
        sm = spinp.match(cmd)
        xm = exchp.match(cmd)
        pm = partp.match(cmd)

        if sm:
            nmitems = int(sm.group(1))
            if __debug__: print("swap: {}".format(nmitems))
            progs = progs[-nmitems:] + progs[0:len(progs) - nmitems]
        elif xm:
            idx1 = int(xm.group(1))
            idx2 = int(xm.group(2))
            if __debug__: print("exchange: {} - {}".format(idx1, idx2))
            progs[idx2], progs[idx1] = progs[idx1], progs[idx2]
        elif pm:
            name1 = pm.group(1)
            name2 = pm.group(2)
            if __debug__: print("partners: {} - {}".format(name1, name2))
            idx1, idx2 = progs.index(name1), progs.index(name2)
            progs[idx2], progs[idx1] = progs[idx1], progs[idx2]
        if __debug__: print(progs)
    if i == 0:
        print("Result1: {}".format("".join(progs)))
    seenbefore[tuple(instate)] = progs

print("Result2: {}".format("".join(progs)))

u"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
    Exchange, written xA/B, makes the programs at positions A and B swap places.
    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

"""
