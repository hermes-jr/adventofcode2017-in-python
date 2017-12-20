#!/usr/bin/env python
""" run as `python -O level_19.py` to disable debug garbage """

import re

filename = "in.txt"
map = [x[:] for x in [[" "] * 201] * 201]


# Test
# filename = "testin.txt"
# map = [x[:] for x in [[" "] * 16] * 16]


def getdirection(oldX, oldY):
    global map, pX, pY
    for option in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        if __debug__: print("Analyzing turn option: {}".format(option))
        if pX + option[0] == oldX and pY + option[1] == oldY:
            # Don't go back
            if __debug__: print("Would send back: {}".format(option))
            continue
        if map[pY + option[1]][pX + option[0]] != " ":
            if __debug__: print("Gonna turn: {}".format(option))
            return option
    return None  # Dead end


result2 = 0

with open(filename, 'r') as f:
    ln = 0
    for line in f:
        cn = 0
        for chr in line.rstrip():
            if __debug__: print("ln: {} cn: {} chr: {}".format(ln, cn, chr))
            map[ln][cn] = chr
            cn += 1
        ln += 1

if __debug__: print(map)

pX = map[0].index("|")
pY = 0
dX, dY = (0, 1)
lettersSeen = []

if __debug__: print("In: {}:{}".format(pX, pY))
ltrRe = re.compile("[a-zA-Z]")

while True:
    pX += dX
    pY += dY
    result2 += 1
    curTile = map[pY][pX]

    if __debug__: print("Analyzing {}:{} ({})".format(pX, pY, curTile))

    if ltrRe.match(curTile):
        lettersSeen.append(curTile)
        print("Letter found: {}".format(curTile))
        continue
    elif curTile == " ":
        print("This is the end")
        break
    elif curTile == "+":
        print("Have to turn")
        nd = getdirection(pX - dX, pY - dY)
        if nd == None:
            print("Dead end")
            break
        dX, dY = nd

print("Result1: {}".format("".join(lettersSeen)))
print("Result2: {}".format(result2))
u"""
"""
