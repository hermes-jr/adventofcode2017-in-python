#!/usr/bin/env python
""" run as `python -O level_14.py` to disable debug garbage """

from functools import reduce

import networkx
import numpy as np

startData = "hfdlxzhv"


# Test
# startData = "flqrgnkx"

# Knothash method by poppy_92 (https://www.reddit.com/r/adventofcode/comments/7irzg5/2017_day_10_solutions/dr108gl/)
# Had to "borrow" it because of missing access to my own day 10 solution :)
def knothash(ins, n=256, byte=False):
    skip_size = 0
    index = 0
    nums = list(range(n))
    if byte:
        ins = [ord(k) for k in ins] + [17, 31, 73, 47, 23]
    else:
        ins = [int(k) for k in ins.split(',')]
    n_iter = 1
    if bytes:
        n_iter = 64
    for _ in range(n_iter):
        s = ins[:]
        for length in s:
            seen = set()
            i = (index + length - 1) % n
            for j in range(index, index + length):
                j = j % n
                i = i % n
                if j in seen or i in seen:
                    break
                seen.add(j)
                seen.add(i)
                # print(i, j)
                nums[i], nums[j] = nums[j], nums[i]
                i -= 1
            index = (length + index + skip_size) % n
            skip_size += 1
    if not byte:
        return nums[0] * nums[1]
    dense = []
    for j in range(0, n, 16):
        val = reduce(lambda a, b: a ^ b, nums[j: j + 16])
        hexed = hex(val).replace('0x', '')
        if len(hexed) == 1:
            hexed = '0' + hexed
        dense.append(hexed)
    return ''.join(dense)


def bitval(kh):
    return bin(kh)[2:].zfill(128)


matrix = np.zeros((128, 128))
graph = networkx.Graph()

result1 = 0
for i in range(0, 128):
    hash = knothash("{}-{}".format(startData, i), byte=True)
    bv = bitval(int(hash, 16))
    for oneidx in range(0, len(bv)):
        if bv[oneidx] == "1":
            matrix[i][oneidx] = 1
            result1 += 1

if __debug__: print(matrix)

for i in range(0, 128):
    for j in range(0, 128):
        if matrix[i][j] == 0:
            continue
        graph.add_node('{}-{}'.format(i, j))
        if i < 127 and matrix[i + 1][j] == 1:
            graph.add_edge('{}-{}'.format(i, j), '{}-{}'.format(i + 1, j))
        if j < 127 and matrix[i][j + 1] == 1:
            graph.add_edge('{}-{}'.format(i, j), '{}-{}'.format(i, j + 1))

print("Result1: {}".format(result1))
print("Result2: {}".format(networkx.number_connected_components(graph)))

u"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.-->
|      |   
V      V   

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are present.

How many regions are present given your key string?

"""
