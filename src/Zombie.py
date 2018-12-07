import pygame, sys
from pygame.locals import *

import random

class Zombie(pygame.sprite.Sprite):
    speed=50 #set the module of velocity

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    pos_max_x=1024
    pos_max_y=768
    pos_min_x=0
    pos_min_y=0


    def __init__(self, x, y):
        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load('zombie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0


    def display(self, displayObj):
        """
            Method that displays the zombie
            :param displayObj --> Object display where the hero will be display on
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))
    def setVel(self, positionHero, vx):
        """
            Method that update the direction of the velocity vector of the zombie towards the hero
            :param vec: new vector velocity
        """
        vx_tohero = positionHero.x - self.rect.x
        vy_tohero = positionHero.y - self.rect.y
        if vx == 0:
            vel_x = 0
            vel_y = vy_tohero
            print(vy_tohero)
            if vy_tohero < 30 or vy_tohero > 30:
                vel_y = -1
        else:
            vel_x = vx_tohero
            vel_y = vy_tohero
        vel = pygame.math.Vector2(vel_x, vel_y)
        if vel != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vel.normalize()
        else:
            pass

    def update(self, t):
        """
            Method that update the position of the Zombie. The method update of the super class does nothing, so here it is overwritten
            :param t --> time passed in seconds from the last call
        """

        # calculates the new position vector, to do so, the attibute rect is turned into a 2d vector to make easier the operations
        newpos = pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*(random.randint(self.speed -20, self.speed +20))*t
        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x= clamp(newpos.x,Zombie.pos_min_x,Zombie.pos_max_x)
        newpos.y= clamp(newpos.y, Zombie.pos_min_y, Zombie.pos_max_y)
        self.rect.x = newpos.x
        self.rect.y = newpos.y

def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
    """
    return max(min(maxn, n), minn)