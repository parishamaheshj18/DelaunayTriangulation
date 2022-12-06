

import pygame
from pygame.locals import *
from config import *
import config as G
import time
import numpy as np
from mesh import Mesh
from mesh import gen_random
from mesh import gen_grid
from mesh import gen_circle
from mesh import gen_circle_i
from divide_conquer_delaunay import delaunay
import geopandas as gpd


def main():
    pygame.init()
    pygame.display.set_caption('Delaunay')
    G.screen_w = SCREEN_W
    G.screen_h = SCREEN_H
    G.screen_mode = SCREEN_MODE
    G.screen = pygame.display.set_mode([G.screen_w, G.screen_h], G.screen_mode)
    G.screen.fill(BG_COLOR)
    G.background = G.screen.copy()

    temp_data = gpd.read_file("data.csv")
    coord = np.column_stack((np.asarray(
        temp_data.lon, dtype=np.float32), np.asarray(temp_data.lat, dtype=np.float32)))
    lon_max = np.amax(coord, axis=0)[0]
    lat_max = np.amax(coord, axis=0)[1]
    lon_min = np.amin(coord, axis=0)[0]
    lat_min = np.amin(coord, axis=0)[1]
    coordinate_normal = []
    for crd in coord:
        x = SCREEN_H * (crd[0] - lon_min)/(lon_max - lon_min)
        y = SCREEN_W - SCREEN_W * (crd[1] - lat_min)/(lat_max - lat_min)
        coordinate_normal.append([x, y])

    points = []
    for i in range(len(coord)):
        x = coordinate_normal[i][0]
        y = coordinate_normal[i][1]
        points.append(pygame.Vector2(x, y))

    G.mesh = Mesh(points)
    G.mesh.generate()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.__dict__['key'] == 32:         # space
                    G.mesh.generate()
        time.sleep(0.1)


def main_no_visual():
    points = gen_random(10, 10, 10)
    print(points)
    edges = delaunay(points)
    print("Number of edges (random): " + str(len(edges)))

    points = gen_grid(100_000_000, 100_000_000, 35)
    edges = delaunay(points)
    print("Number of edges (grid): " + str(len(edges)))

    points = gen_circle(100_000_000, 100_000_000, 1000)
    edges = delaunay(points)
    print("Number of edges (circle): " + str(len(edges)))

    points = gen_circle_i(100_000_000, 100_000_000, 1000)
    edges = delaunay(points)
    print("Number of edges (circle_i): " + str(len(edges)))


if __name__ == '__main__':
    main()
    # main_no_visual()
