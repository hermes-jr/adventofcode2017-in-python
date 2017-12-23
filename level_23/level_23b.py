#!/usr/bin/env python
""" run as `python -O level_23b.py` to disable debug garbage """

b = 108400  # 100000 + 84 * 100
c = 125400  # 100000 + 84 * 100 + 17000
step = 17  # line 31

result2 = 0
for rng in range(b, c + 1, step):
    for i in range(2, rng):
        if rng % i == 0:
            result2 += 1
            break

print("Result2: {}".format(result2))

u"""
--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes. Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?
"""
