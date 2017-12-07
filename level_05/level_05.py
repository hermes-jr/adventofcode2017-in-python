# !/usr/bin/env python
""" run as `python -O level_05.py` to disable debug garbage """

data = list()

with open('in.txt', 'r') as f:
    for line in f:
        data.append(int(line.strip()))

if __debug__: print(data)
goal = len(data)

# stepCount = 0
# curIdx = 0
# while True:
#     if curIdx > goal - 1:
#         break
#     stepCount += 1
#     nextIdx = curIdx + data[curIdx]
#     data[curIdx] += 1
#     curIdx = nextIdx

stepCount = 0
curIdx = 0
while True:
    if curIdx > goal - 1:
        break
    stepCount += 1
    nextIdx = curIdx + data[curIdx]
    if (data[curIdx] >= 3):
        data[curIdx] -= 1
    else:
        data[curIdx] += 1
    curIdx = nextIdx

print("result: {}".format(stepCount))
