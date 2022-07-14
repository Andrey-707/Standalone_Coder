# Поиск в ширину на примере pygame.
# 2.Создание карты препятствий

import pygame as pg

from random import random
from collections import deque


def get_rect(x, y):
    """
    Функция отрисовки прямоугольника.
    """
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

# main canvas
cols, rows = 25, 15
TILE = 60

# main resolution
RES = [cols * TILE, rows * TILE]

pg.init()
pg.display.set_caption("breadth first search algorithm")
sc = pg.display.set_mode(RES)
clock = pg.time.Clock()
FPS = 7

# grid
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]

while True:
    # fill screen
    sc.fill(pg.Color('black'))

    # draw grid
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(FPS)
