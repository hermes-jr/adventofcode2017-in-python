#!/usr/bin/env python
""" run as `python -O level_10.py` to disable debug garbage """

from itertools import cycle, islice

input = [106, 16, 254, 226, 55, 2, 1, 166, 177, 247, 93, 0, 255, 228, 60, 36]
indata = list(range(0, 256))

# Test data
# input = [1, 2, 3]
# indata = list(range(0, 256))

skip = 0


def rotlist(list, by):
    pool = cycle(list)
    skipedPos = islice(pool, by, None)
    nextState = []
    for i in range(len(indata)):
        nextState.append(next(skipedPos))
    if __debug__: print("Skipped {}: {}".format(by, nextState))
    return nextState


input2 = []
if len(input) > 0:
    for i in input[0:-1]:
        input2 += list(map(ord, str(i)))
        input2.append(44)
    input2 += list(map(ord, str(input[-1])))

input2 += (17, 31, 73, 47, 23)
print(input2)

totalForward = 0
for r in range(0, 64):
    for i in input2:
        if __debug__: print("Original: {}".format(indata))
        indata[0:i] = indata[0:i][::-1]
        if __debug__: print("Reversed {} elements: {}".format(i, indata))
        indata = rotlist(indata, i + skip)
        totalForward += i + skip
        skip += 1
        if __debug__: print("Skip now is: {}".format(skip))

if totalForward > len(indata):
    totalForward = totalForward % len(indata)
if __debug__: print("Total forward from original: {}".format(totalForward))
origProjection = list(indata)
origProjection = rotlist(origProjection, len(indata) - totalForward)
if __debug__: print("Result ({}): {}".format(len(origProjection), origProjection))

dense = []
for x in range(0, 16):
    bte = origProjection[x * 16]
    for y in range(1, 16):
        bte ^= origProjection[x * 16 + y]
    dense.append(bte)

print(dense)
result2 = ""
for i in dense:
    result2 += format(i, '02x')
print("Result2: {}".format(result2))

u"""
--- Part Two ---

The logic you've constructed forms a single round of the Knot Hash algorithm; running the full thing requires many of these rounds. Some input and output processing is also required.

First, from now on, your input should be taken not as a list of numbers, but as a string of bytes instead. Unless otherwise specified, convert characters to bytes using their ASCII codes. This will allow you to handle arbitrary ASCII strings, and it also ensures that your input lengths are never larger than 255. For example, if you are given 1,2,3, you should convert it to the ASCII codes for each character: 49,44,50,44,51.

Once you have determined the sequence of lengths to use, add the following lengths to the end of the sequence: 17, 31, 73, 47, 23. For example, if you are given 1,2,3, your final sequence of lengths should be 49,44,50,44,51,17,31,73,47,23 (the ASCII codes from the input string combined with the standard length suffix values).

Second, instead of merely running one round like you did above, run a total of 64 rounds, using the same length sequence in each round. The current position and skip size should be preserved between rounds. For example, if the previous example was your first round, you would start your second round with the same length sequence (3, 4, 1, 5, 17, 31, 73, 47, 23, now assuming they came from ASCII codes and include the suffix), but start with the previous round's current position (4) and skip size (4).

Once the rounds are complete, you will be left with the numbers from 0 to 255 in some order, called the sparse hash. Your next task is to reduce these to a list of only 16 numbers called the dense hash. To do this, use numeric bitwise XOR to combine each consecutive block of 16 numbers in the sparse hash (there are 16 such blocks in a list of 256 numbers). So, the first element in the dense hash is the first sixteen elements of the sparse hash XOR'd together, the second element in the dense hash is the second sixteen elements of the sparse hash XOR'd together, etc.

For example, if the first sixteen elements of your sparse hash are as shown below, and the XOR operator is ^, you would calculate the first output number like this:

65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22 = 64

Perform this operation on each of the sixteen blocks of sixteen numbers in your sparse hash to determine the sixteen numbers in your dense hash.

Finally, the standard way to represent a Knot Hash is as a single hexadecimal string; the final output is the dense hash in hexadecimal notation. Because each number in your dense hash will be between 0 and 255 (inclusive), always represent each number as two hexadecimal digits (including a leading zero as necessary). So, if your first three numbers are 64, 7, 255, they correspond to the hexadecimal numbers 40, 07, ff, and so the first six characters of the hash would be 4007ff. Because every Knot Hash is sixteen such numbers, the hexadecimal representation is always 32 hexadecimal digits (0-f) long.

Here are some example hashes:

    The empty string becomes a2582a3a0e66e6e86e3812dcb672a272.
    AoC 2017 becomes 33efeb34ea91902bb2f59c9920caa6cd.
    1,2,3 becomes 3efbe78a8d82f29979031a4aa0b16a9d.
    1,2,4 becomes 63960835bcdc130f0b66d7ff4f6a5a8e.

Treating your puzzle input as a string of ASCII characters, what is the Knot Hash of your puzzle input? Ignore any leading or trailing whitespace you might encounter.

"""
