# 5.Game Life Python + Numba !!!

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
FPS = -1

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

# numpay array
next_field = np.array([[0 for i in range(W)] for j in range(H)])

# other config for 'ONE' 
# current_field = np.array([[randint(0, 1) for i in range(W)] for j in range(H)])
current_field = np.array([[1 if not i % 33 else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not (4 * i + j) % 4 else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)])


@njit(fastmath=True)
def check_cell(current_field, next_field):
    """
    Функция проверки соседних клеток.
    """
    res = []
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if current_field[j][i] == 1:
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
    [pg.draw.rect(surface, pg.Color('darkorange'), (x * TILE + 1, y * TILE + 1, \
        TILE - 1, TILE - 1)) for x, y in res]

    current_field = deepcopy(next_field)

    pg.display.flip()
    clock.tick(FPS)

    # exit game
    [exit() for event in pg.event.get() if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE]
