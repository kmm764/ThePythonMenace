import pygame, sys
from pygame.locals import *
from src.Person import Person

import random

tile_size=32
WIDTH = 1024
HEIGHT = 768


class Zombie(Person):
    speed=50 #set the module of velocity
    radius_min = 100
    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen



    def __init__(self, x, y):
        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load('zombie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = pygame.math.Vector2(0.0, 0.0) #initialize the velocity vector to 0,0
        self.img_height = 43
        self.img_width = 35
        self.pos_max_x = WIDTH - self.img_width
        self.pos_max_y = HEIGHT - self.img_height


    """----------------NEW CODE ----------------------------"""

    def trajectory_intention(self, positionHero):
        vel = pygame.math.Vector2(positionHero.x - self.rect.x, positionHero.y - self.rect.y)
        if vel != (0., 0.):
            # if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            return vel.normalize()
        else:
            return vel

    def hero_near(self, positionHero):
        if abs(positionHero.x - self.rect.x) < Zombie.radius_min or abs(positionHero.y - self.rect.y) < Zombie.radius_min:
            return True
        else:
            return False

    def splash_display(self):
        splash_img = pygame.image.load('splat.png')
        splash_img_scale = pygame.transform.scale(splash_img, (tile_size, tile_size))

    def update(self, t):
        self.setPos(t)
