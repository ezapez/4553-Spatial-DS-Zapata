from quadTree import *
import pygame as pg
from random import randint
import random as rd
import numpy as np

import os

# Get the size
# of the terminal
size = os.get_terminal_size()

# set the size of terminal
x, y = size
x *= 5
y *= 15
size = (x, y)
width, height = size

pg.init()
screen = pg.display.set_mode(size)
pg.display.set_caption('P07')
radius = 3
SIZE = 3


def genPoints(bbox, x=500):

    points = []
    for p in range(x):
        x = randint(radius, bbox.w - radius)
        y = randint(radius, bbox.h - radius)
        points.append(Point(x, y))
    return points


def highlightPoints(foundPoints):
    for p in foundPoints:
        # colors found dot in box as green
        pg.draw.circle(screen, (86, 140, 53), [p.x, p.y], radius + 2)


if __name__ == '__main__':

    # makes bbox
    bbox = Rect(size[0] // 2, size[0] // 2, size[0], size[0])
    qt = QuadTree(bbox)

    points = genPoints(bbox, 500)

    for p in points:
        qt.insert(p)

    foundPoints = []
    # create var to make it easier to read
    # size the box
    box_X = 0
    box_Y = 0
    box_w = 50
    box_h = 50
    # make box
    box = Rect(box_X, box_Y, box_w, box_h)

    # query_box = Rect(0,0,100,100)

    # finds points in box
    # qt.query(query_box,foundPoints)

    running = True
    # switch to kill game after box hits the bottom
    switch = pg.Rect(351.00, 325.00, 401.00, 375.00)

    change_x = 1
    change_y = 0
    lock_w = 100
    lock_h = 100
    new_y = 100

    # Game loop
    # keep game running till running is true
    while running:
        # white background
        screen.fill((255, 255, 255))

        # Check for event if user has pushed
        # any event in queue
        for event in pg.event.get():
            # if event is of type quit then set
            # running bool to false
            if event.type == pg.QUIT:
                running = False

        # change += 1
        # print(change)

        #moving box
        box_X += 4
        box = Rect(box_X, box_Y, box_w, box_h)
        #prints found points within box
        # also print width and height 
        print(foundPoints,(box_w,box_h))
        # clear list each time new points are found
        foundPoints.clear()
        

        displayBox = pg.Rect(box_X - 25, box_Y - 25, box_w, box_h)

        # change_x += 2
        # print(change_x)

        #query_box = Rect(change_x, change_y, lock_w, lock_h)

        #print(query_box)
        qt.query(box, foundPoints)

        if box.east_edge > width:
            box_X = 0
            box_Y += 50
            box = Rect(box_X, box_Y, box_w, box_h)
            # foundPoints.clear()
            # print(foundPoints)


        
        qt.draw(screen, radius)
        highlightPoints(foundPoints)
        pg.draw.rect(screen, (123, 200, 77), displayBox, SIZE)

        pg.display.update()
        pg.time.delay(60)  
