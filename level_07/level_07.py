# !/usr/bin/env python
""" run as `python -O level_05.py` to disable debug garbage """

import re
from collections import Counter


class Prog(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.grandTotal = weight
        self.parent = None
        self.children = []

    def addchild(self, child):
        child.parent = self
        self.children.append(child)

    def nodeweight(self):
        for x in self.children:
            self.grandTotal += x.nodeweight()
        return self.grandTotal

    def findabomination(self):
        mode = Counter(map(lambda Prog: Prog.grandTotal, self.children)).most_common(2)
        if (len(mode) == 1):
            return
        for x in self.children:
            if (x.grandTotal != mode[0]):
                print("mode: {}, parent (self): {}, child: {}, wt: {}, gt: {}; after diet: {}"
                      .format(mode, self.name, x.name, x.weight, x.grandTotal, x.weight - x.grandTotal + mode[0][0]))
                x.findabomination()

    def __repr__(self):
        return "Prog {{{}, weight: {}, parent: {}, children ({}): {}}}".format(self.name, self.weight, self.parent,
                                                                               len(self.children), self.children)


data = {}
firstPassPattern = re.compile(r"^([a-zA-Z]+) \((\d+)\).*")
secondPassPattern = re.compile(r"^([a-zA-Z]+) \(\d+\) -> (.*)$")

""" Obtain names and weights """
with open('in.txt', 'r') as f:
    for line in f:
        match = firstPassPattern.match(line.strip())
        progName = match.group(1)
        data[progName] = Prog(progName, int(match.group(2)))

if __debug__: print("1: {}".format(data))

""" Obtain links """
with open('in.txt', 'r') as f:
    for line in f:
        match = secondPassPattern.match(line.strip())
        if not match: continue

        parentProg = data[match.group(1)]
        if __debug__: print("adding children to {}".format(parentProg.name))
        for childName in list(match.group(2).split(", ")):
            child = data.get(childName)
            if __debug__: print("\tadding child {}".format(childName))
            parentProg.addchild(child)

root = None

progIter: Prog
for progIter in data.values():
    if progIter.parent is None:
        root = progIter
        break

if __debug__: print(root)

print("Result1: {}".format(root.name))

root.nodeweight()
print("result2: too lazy to calculate depth, just find the lowest grandTotal. Result2 is in \"after diet\" column")
root.findabomination()

u"""
--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large tower.

One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the disc below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this in an orderly fashion; by the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /     
         ugml - ebii
       /      \     
      |         jptl
      |        
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |             
      |         ktlj
       \      /     
         fwft - cntj
              \     
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft. Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up any other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is correct. What is the name of the bottom program?


--- Part Two ---

The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's fixed, they're stuck here.

For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers are supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each match. This means that the following sums must all be the same:

    ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
    padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
    fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?

"""
