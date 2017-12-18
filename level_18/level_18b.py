#!/usr/bin/env python
""" run as `python -O level_08b.py` to disable debug garbage """

import queue
import threading

program = []

with open('in.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if __debug__: print(line)
        program.append(line)

q0 = queue.Queue()
q1 = queue.Queue()


class Duo(object):
    def __init__(self, duoid):
        self.myid = duoid
        self.regs = {"p": duoid}

    def getregval(self, reg):
        if reg not in self.regs:
            self.regs[reg] = 0
        return self.regs[reg]

    def setregval(self, reg, val):
        self.regs[reg] = val

    def nameorval(self, decode):
        try:
            iv = int(decode)
            return iv
        except ValueError:
            return self.getregval(decode)

    def runprog(self):
        print("Running... {}".format(self.myid))
        self.cnt = 0
        self.ip = 0
        while True:
            # Out of bounds
            if self.ip >= len(program) or self.ip < 0:
                print("Program ends: ip is out of bounds")
                break

            # Step
            line = program[self.ip]
            if __debug__: print("ip: {} line: {} regs: {}".format(self.ip, line, self.regs))

            if line.startswith("snd"):
                arg = self.nameorval(line.split()[1])
                tgtq = q1 if self.myid == 0 else q0
                tgtq.put(arg)
                if self.myid == 1:
                    self.cnt += 1
                    print("COUNT: {}".format(self.cnt))
                # self.melody.append(self.getregval(arg))
            elif line.startswith("set"):
                tgt = line.split()[1]
                arg = self.nameorval(line.split()[2])
                self.setregval(tgt, arg)
            elif line.startswith("add"):
                tgt = line.split()[1]
                arg = self.nameorval(line.split()[2])
                self.setregval(tgt, self.getregval(tgt) + arg)
            elif line.startswith("mul"):
                tgt = line.split()[1]
                arg = self.nameorval(line.split()[2])
                self.setregval(tgt, self.getregval(tgt) * arg)
            elif line.startswith("mod"):
                tgt = line.split()[1]
                arg = self.nameorval(line.split()[2])
                self.setregval(tgt, self.getregval(tgt) % arg)
            elif line.startswith("rcv"):
                arg = line.split()[1]
                tgtq = q1 if self.myid == 1 else q0
                val = tgtq.get(True)
                self.setregval(arg, val)
            elif line.startswith("jgz"):
                cmp = self.nameorval(line.split()[1])
                offs = self.nameorval(line.split()[2])
                if cmp > 0:
                    if offs != 0:
                        self.ip += offs - 1

            self.ip += 1

        if __debug__: print(self.regs)
        if __debug__: print("{} Done".format(self.myid))


p0 = Duo(0)
p1 = Duo(1)

threading.Thread(target=p0.runprog).start()
threading.Thread(target=p1.runprog).start()

u"""
--- Part Two ---

As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet this entire time. While you actually got most of the instructions correct, there are a few key differences. This assembly code isn't about sound at all - it's meant to be run twice at the same time.

Each running copy of the program has its own set of registers and follows the code independently - in fact, the programs don't even necessarily run at the same speed. To coordinate, they use the send (snd) and receive (rcv) instructions:

    snd X sends the value of X to the other program. These values wait in a queue until that program is ready to receive them. Each program has its own message queue, so a program can never receive a message it sent.
    rcv X receives the next value and stores it in register X. If no values are in the queue, the program waits for a value to be sent to it. Programs do not continue to the next instruction until they have received a value. Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2, 0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and stores it in a, receives another value (both 2) and stores it in b, and then each receives the program ID of the other program (program 0 receives 1; program 1 receives 0) and stores it in c. Each program now sees a different value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for either of them, and they reach a deadlock. When this happens, both programs terminate.

It should be noted that it would be equally valid for the programs to run at different speeds; for example, program 0 might have sent all three values and then stopped at the first rcv before program 1 executed even its first instruction.

Once both of your programs have terminated (regardless of what caused them to do so), how many times did program 1 send a value?

"""
