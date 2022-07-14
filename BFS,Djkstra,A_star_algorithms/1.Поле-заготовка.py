# Поиск в ширину на примере pygame.
# 1.Поле-заготовка

import pygame as pg


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

while True:
    # fill screen
    sc.fill(pg.Color('black'))

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(FPS)
