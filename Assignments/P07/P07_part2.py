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

  
    
    xy_pos = []
    wh_pos =[]
  
    start = (0, 0)
    size = (0, 0)
  # bool value for drawing 
    drawing = False
  # while loop to quit game
    running = True
    foundPoints = []
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
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                start = event.pos
                size = 0, 0
                drawing = True
                
            elif event.type == pg.MOUSEBUTTONUP:
                end = event.pos
                size = end[0] - start[0], end[1] - start[1]
                xy_pos.append(end)
                wh_pos.append(size)
              
                drawing = False

          
              
            if drawing == True:
              xy_pos.clear()
              wh_pos.clear()
              foundPoints.clear()
              
                
  
        
        for x,y in xy_pos:
          print("x,y:", x , y)
         
          for w,h in wh_pos:
              new_w = w /2
              new_h = h/2
              box = Rect(x,y,w,h)
              displayBox = pg.Rect(x - new_w ,y -new_h,w,h)
              pg.draw.rect(screen,(255,0,0),displayBox,SIZE)
              qt.query(box, foundPoints)
             
            
                   
                
              
      
      
        
       
        qt.draw(screen, radius)
        highlightPoints(foundPoints)
        pg.display.update()
        pg.display.flip()
        pg.time.delay(60)  
