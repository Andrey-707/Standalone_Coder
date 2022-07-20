# Game Life Main file

import ctypes
import pygame as pg
import numpy as np

from time import time
from random import randrange
from copy import deepcopy
from numba import njit


user32 = ctypes.windll.user32
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
RES = [WIDTH, HEIGHT]
TILE = 5
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 15
game = True
start_time = time()
end_time = 53

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

# numpay array
next_field = np.array([[0 for i in range(W)] for j in range(H)])
current_field = np.array([[0 for i in range(W)] for j in range(H)])

# background
img = pg.image.load('image\\space1.png')
# img = pg.image.load('image\\space2.png')
img = pg.transform.scale(img, RES)

# sound track
pg.mixer.init()
sound_track = 'sound\\Bon_Jovi_-_Its_My_Life.mp3'#pg.mixer.Sound()


def set_glider_SE(current_field, x, y):
    """
    Функция отрисовки глайдера с юга на восток.
    """
    pos = [(x, y), (x + 1, y + 1), (x - 1, y + 2), (x, y + 2), (x + 1, y + 2)]
    for i, j in pos:
        current_field[j][i] = 1
    return current_field


def set_glider_NW(current_field, x, y):
    """
    Функция отрисовки глайдера с севера на запад.
    """
    pos = [(x, y), (x - 2, y - 1), (x - 2, y), (x - 2, y + 1), (x - 1, y - 1)]
    for i, j in pos:
        current_field[j][i] = 1
    return current_field


for _ in range(500):
    i0, j0 = randrange(TILE, W // 2 + W // 4, TILE), randrange(TILE, H // 2)
    current_field = set_glider_SE(current_field, i0, j0)
    i1, j1 = randrange(W // 2 - W // 4, W - TILE), randrange(H // 2, H - TILE)
    current_field = set_glider_NW(current_field, i1, j1)


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


def play_sound(sound):
    """
    Функция запуска звукового файла.
    """
    pg.mixer.music.load(sound)
    pg.mixer.music.play()


play_sound(sound_track)

while game:
    # check timer
    current_time = int(time() - start_time)
    if current_time == end_time:
        game = False
    
    # draw background
    surface.blit(img, (0, 0))

    # draw life
    next_field, res = check_cell(current_field, next_field)
    [pg.draw.rect(surface, pg.Color('white'), (x * TILE + 1, y * TILE + 1, \
        TILE - 1, TILE - 1)) for x, y in res]

    current_field = deepcopy(next_field)

    pg.display.flip()
    clock.tick(FPS)

    # exit game
    [exit() for event in pg.event.get() if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE]
