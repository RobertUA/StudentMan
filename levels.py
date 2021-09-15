import random
from settings import *

Level = []


def loadlevel():
    Level.clear()
    # borders
    for i in range(0, 501, 25):
        row = []
        for j in range(0, 501, 25):
            row.append(0)
        Level.append(row)

    for i in range(0, 21):
        Level[i][0] = 1
        Level[i][20] = 1
        if i != 10:
            Level[0][i] = 1
            Level[20][i] = 1

    # rnd1
    if random.randint(0, 1) == 0:
        for j in range(5, 16):
            Level[10][j] = 1
    else:
        for j in range(5, 16):
            Level[j][10] = 1
    # rnd2
    c = random.choice([5, 16])
    if random.randint(0, 1) == 0:
        for j in range(5, 16):
            Level[c][j] = 1
    else:
        for j in range(5, 16):
            Level[j][c] = 1
