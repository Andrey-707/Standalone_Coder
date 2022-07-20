# 1.Game Life Make Grid

import ctypes
import pygame as pg

from random import randint
from copy import deepcopy


user32 = ctypes.windll.user32
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
RES = [WIDTH, HEIGHT]
TILE = 50
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 10

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

while True:
    surface.fill(pg.Color('black'))
    [exit() for event in pg.event.get() if event.type == pg.QUIT]

    # draw grid
    [pg.draw.line(surface, pg.Color('dimgray'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pg.draw.line(surface, pg.Color('dimgray'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]

    # exit game
    [exit() for event in pg.event.get() if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE]

    pg.display.flip()
    clock.tick(FPS)
