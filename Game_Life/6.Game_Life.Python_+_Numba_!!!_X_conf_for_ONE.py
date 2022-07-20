# 6.Game Life Python + Numba !!! X config for 'ONE'

import ctypes
import pygame as pg
import numpy as np

from random import randint
from copy import deepcopy
from numba import njit


user32 = ctypes.windll.user32
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
RES = [WIDTH, HEIGHT]
TILE = 5
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 20

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

# numpay array
next_field = np.array([[0 for i in range(W)] for j in range(H)])
current_field = np.array([[0 for i in range(W)] for j in range(H)])
for i in range(H):
    current_field[i][i + (W - H) // 2] = 1
    current_field[H - i - 1][i + (W - H) // 2] = 1


@njit(fastmath=True)
def check_cell(current_field, next_field):
    """
    Функция проверки соседних клеток.
    """
    res = []
    for x in range(W):
        for y in range(H):
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if current_field[j % H][i % W] == 1:
                        count +=1

            if current_field[y][x] == 1:
                count -= 1
                if count == 2 or count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0
            else:
                if count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0
    return next_field, res


while True:
    surface.fill(pg.Color('black'))
    [exit() for event in pg.event.get() if event.type == pg.QUIT]

    # draw life
    next_field, res = check_cell(current_field, next_field)
    [pg.draw.rect(surface, pg.Color('green'), (x * TILE + 1, y * TILE + 1, \
        TILE - 1, TILE - 1)) for x, y in res]

    current_field = deepcopy(next_field)

    pg.display.flip()
    clock.tick(FPS)

    # exit game
    [exit() for event in pg.event.get() if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE]
