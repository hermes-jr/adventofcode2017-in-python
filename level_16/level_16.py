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
"""
