import pygame, sys
from pygame.locals import *


class Hero:
    speed=100 #set the module of velocity

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    pos_max_x=940
    pos_max_y=540
    pos_min_x=0
    pos_min_y=0

    def __init__(self):
        self.Img = pygame.image.load('bloomy.png')
        self.pos = pygame.math.Vector2(0.0,0.0) #inicialize the vector position to 0,0
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0

    def display(self, displayObj):
        """
            Method that displays the hero
            :param displayObj --> Object display where the hero will be display on
        """
        displayObj.blit(self.Img, (self.pos.x, self.pos.y))

    def setPos(self, t):
        """
            Method that updates the position of the hero, based on the time passed and the velocity of the hero
            :param t --> time passed in seconds from the last call
        """
        newpos = self.pos+self.vel*self.speed*t #calculates the new position vector
        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x=clamp(newpos.x,Hero.pos_min_x,Hero.pos_max_x)
        newpos.y=clamp(newpos.y, Hero.pos_min_y, Hero.pos_max_y)
        self.pos=newpos

    def setVel(self, vec):
        """
            Method that update the velocity of the hero
            :param vec: new vector velocity
        """
        if vec != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector
            self.vel = vec.normalize()
        else:
        #if the new velocity vector is (0,0)
            self.vel=vec


def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
    """
    return max(min(maxn, n), minn)