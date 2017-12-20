#!/usr/bin/env python
""" run as `python -O level_19.py` to disable debug garbage """

import re

filename = "in.txt"

ptcs = []
vels = []
accs = []


# Test
# filename = "testin.txt"
# filename = "testin2.txt"


def dist3(three):
    return abs(three[0]) + abs(three[1]) + abs(three[2])


def vectorlength(three):
    return (three[0] ** 2 + three[1] ** 2 + three[2] ** 2) ** (1 / 2.0)


# p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
linematch = re.compile(
    "^p=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, v=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, a=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>$")

with open(filename, 'r') as f:
    for line in f:
        matcher = linematch.match(line.strip())
        ptcs.append((int(matcher.group(1)), int(matcher.group(2)), int(matcher.group(3))))
        vels.append((int(matcher.group(4)), int(matcher.group(5)), int(matcher.group(6))))
        accs.append((int(matcher.group(7)), int(matcher.group(8)), int(matcher.group(9))))
    accs = (accs)

if __debug__: print(accs)

mid = 0
minvl = None
for idx, val in enumerate(accs):
    cvl = vectorlength(val)
    if minvl == None or cvl <= minvl:
        mid = idx
        minvl = cvl
        if __debug__: print("Found new low acc: {} {}".format(mid, minvl))

print("Result1: {}".format(mid))

step = 0
while step < 100_000_000:
    step += 1
    cstate = {}
    for idx, val in enumerate(ptcs):
        vels[idx] = [a + b for a, b in zip(vels[idx], accs[idx])]
        ptcs[idx] = [a + b for a, b in zip(ptcs[idx], vels[idx])]
        curTupl = tuple(ptcs[idx])
        if curTupl in cstate:
            cstate[curTupl] = cstate[curTupl] + ([idx])  # One more element at the same coordinate at this point in time
        else:
            cstate[curTupl] = ([idx])  # The only element at this coordinate for now
    for k, v in cstate.items():
        if len(v) > 1:
            print("Collision found on step {}: {}".format(step, v))
            for idtoremove in reversed(sorted(v)):
                del ptcs[idtoremove]
                del vels[idtoremove]
                del accs[idtoremove]
            print("Items left {}".format(len(ptcs)))

print("Result2: {}".format(len(ptcs)))

u"""
--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parenthesis), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?


--- Part Two ---

To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------    
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)         
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?
"""
