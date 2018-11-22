import pygame, sys
from pygame.locals import *

import random

class Zombie(pygame.sprite.Sprite):
    speed=50 #set the module of velocity

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    pos_max_x=940
    pos_max_y=540
    pos_min_x=0
    pos_min_y=0

    def __init__(self, x, y):
        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load('coni.png')
        self.rect = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0


    def display(self, displayObj):
        """
            Method that displays the zombie
            :param displayObj --> Object display where the hero will be display on
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))
    def setVel(self, positionHero):
        """
            Method that update the direction of the velocity vector of the zombie towards the hero
            :param vec: new vector velocity
        """
        vel = positionHero - self.rect
        if vel != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vel.normalize()
        else:
            pass

    def update(self, positionHero, t):
        """
            Method that update the position of the Zombie. The method update of the super class does nothing, so here it is overwritten
            :param t --> time passed in seconds from the last call
        """
        self.setVel(positionHero)
        print(positionHero)
        print(t)
        print(self.vel)
        newpos = self.rect+self.vel*self.speed*t #calculates the new position vector
        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x= clamp(newpos.x,Zombie.pos_min_x,Zombie.pos_max_x)
        newpos.y= clamp(newpos.y, Zombie.pos_min_y, Zombie.pos_max_y)
        print(newpos)
        self.rect=newpos

def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
    """
    return max(min(maxn, n), minn)