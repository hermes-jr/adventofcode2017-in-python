#!/usr/bin/env python
""" run as `python -O level_11.py` to disable debug garbage """

import gc

import hexutil

with open('in.txt', 'r') as f:
    for line in f:
        progPath = line.strip().split(",")
        if __debug__: print(progPath)

xcoord = 0
ycoord = 0
maxPathLen = 0
origin = hexutil.Hex(0, 0)
nstep = 0
totalPathLen = len(progPath)

for direction in progPath:
    nstep += 1
    if direction == "n":
        xcoord += 2
    elif direction == "s":
        xcoord -= 2
    elif direction == "nw":
        xcoord += 1
        ycoord += 1
    elif direction == "ne":
        xcoord += 1
        ycoord -= 1
    elif direction == "sw":
        xcoord -= 1
        ycoord += 1
    elif direction == "se":
        xcoord -= 1
        ycoord -= 1
    lostProgram = hexutil.Hex(xcoord, ycoord)
    pf = lostProgram.find_path(origin, lambda z: True)
    pathLen = len(pf) - 1
    if __debug__: print("x: {} y: {} pl: {} step {}/{}".format(xcoord, ycoord, pathLen, nstep, totalPathLen))
    if nstep % 100 == 0:
        gc.collect()
        print("Path analysis: {} / {}".format(nstep, totalPathLen))
    if pathLen > maxPathLen:
        maxPathLen = pathLen

print("Result1: {}".format(pathLen))

print("Result2: {}".format(maxPathLen))

u"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

"""
