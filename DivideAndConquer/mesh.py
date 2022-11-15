
import pygame
import numpy as np
import math
from   config import *
import config as G
from   divide_conquer_delaunay import delaunay


class Mesh:
    def __init__(self,points):
        np.random.seed(RND_SEED)
        self.points     = points
        self.edges      = None
        self.font_size  = 16
        self.font       = pygame.font.SysFont('Liberation Mono', self.font_size)
        self.cross      = draw_cross()

    def generate(self):
        print(self.points)
        self.edges = delaunay(self.points)
        print(self.edges[0].dest)
        print(self.edges[0].org)
        print(G.screen)
        self.draw(G.screen)

    def draw(self, screen):
        
        screen.fill(BG_COLOR)
        d = self.cross.get_rect().width // 2

        for e in self.edges:
            pygame.draw.line(screen, LINE_COLOR, e.org, e.dest)

        for p in self.points:
            point_rect = pygame.Rect(p[0] - d, p[1] - d, p[0] + d, p[1] + d)
            screen.blit(self.cross, point_rect)
            if DRAW_LABELS:
                label = '({}, {})'.format(p[0], p[1])
                text = self.font.render(label, 0, TEXT_COLOR)
                screen.blit(text, (p[0] + 5, p[1] - self.font_size))
        
        pygame.display.flip()



def draw_cross():
    canvas = pygame.Surface((CROSS_SIZE*2 + 1, CROSS_SIZE*2 + 1))
    canvas.fill(COLOR_KEY)
    canvas.set_colorkey(COLOR_KEY)
    pygame.draw.line(canvas, CROSS_COLOR, [0, CROSS_SIZE], [CROSS_SIZE*2 + 1, CROSS_SIZE])
    pygame.draw.line(canvas, CROSS_COLOR, [CROSS_SIZE, 0], [CROSS_SIZE, CROSS_SIZE*2 + 1])
    return canvas

def gen_random(w, h, n):
    points_x = np.random.randint(0, w, n, dtype=np.int64)
    points_y = np.random.randint(0, h, n, dtype=np.int64)
    # print(type(np.asarray(list(zip(points_x, points_y)), dtype=np.float64)))
    return np.asarray(list(zip(points_x, points_y)), dtype=np.float64)

def gen_grid(w, h, n):
    points_x = np.linspace(50, w-50, n+1, dtype=np.float64)
    points_y = np.linspace(50, h-50, n+1, dtype=np.float64)
    # print(np.asarray(list((i, j) for i in points_x for j in points_y), dtype=np.float64))
    return np.asarray(list((i, j) for i in points_x for j in points_y), dtype=np.float64)

def gen_circle(w, h, n):
    rads = np.linspace(0, 2*math.pi, n+1, dtype=np.float64)
    cx, cy = w // 2, h // 2
    r = min(cx, cy) - 50
    return np.asarray(list((cx + r * math.cos(i), cy + r * math.sin(i)) for i in rads)[:-1], dtype=np.float64)

def gen_circle_i(w, h, n):
    rads = np.linspace(0, 2*math.pi, n+1, dtype=np.float64)
    cx, cy = w // 2, h // 2
    r = min(cx, cy) - 50
    return np.asarray(list((int(cx + r * math.cos(i)), int(cy + r * math.sin(i))) for i in rads)[:-1], dtype=np.float64)