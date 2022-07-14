# Поиск в ширину на примере pygame.
# 5.Добавление кнопок управления и картинки фона

import pygame as pg

from random import random
from collections import deque


def get_rect(x, y):
    """
    Функция отрисовки прямоугольника.
    """
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def get_next_nodes(x, y):
    """
    Функция проверки соседней клетки.
    """
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

# main canvas
cols, rows = 25, 15
TILE = 60

# main resolution
RES = [cols * TILE, rows * TILE]

pg.init()
pg.display.set_caption("breadth first search algorithm")
sc = pg.display.set_mode(RES)
clock = pg.time.Clock()

# grid
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]

# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (0, 0)
queue = deque([start])
visited = {start: None}
cur_node = start

# text font
font = pg.font.Font('text\\font.ttf', 45)

# game pause
PAUSED = False
text_paused = font.render('PAUSED', True, ('darkblue'))

# game background
game_bg = pg.image.load('images\\bg.jpg').convert()

while True:
    # control
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            elif event.key == pg.K_p:
                PAUSED = not PAUSED
    
    pg.display.flip()
    clock.tick(7)
    
    if not PAUSED:
        # fill screen
        sc.fill(pg.Color('black'))

        # draw grid
        [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
          for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

        # draw BFS work
        [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
        [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]

        # BFS logic
        if queue:
            cur_node = queue.popleft()
            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        # draw path
        path_head, path_segment = cur_node, cur_node
        while path_segment:
            pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
            path_segment = visited[path_segment]
        pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
        pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)

    if PAUSED:
        sc.blit(game_bg, (0, 0))
        sc.blit(text_paused, (600, 400))
