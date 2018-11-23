import pygame, sys
from pygame.locals import *


class Hero(pygame.sprite.Sprite):
    speed=100 #set the module of velocity

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    pos_max_x=940
    pos_max_y=540
    pos_min_x=0
    pos_min_y=0
    lives = 3

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('hero.jpeg')
        self.rect = self.image.get_rect()
        self.rect.x = 0.0
        self. rect.y = 0.0
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0

    def display(self, displayObj):
        """
            Method that displays the hero
            :param displayObj --> Object display where the hero will be display on
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))

    def setPos(self, t):
        """
            Method that updates the position of the hero, based on the time passed and the velocity of the hero
            :param t --> time passed in seconds from the last call
        """
        #Here, the new position vector is calculated. The attibute rect is turned into a 2d vector class to make easier the operations
        newpos =  pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*self.speed*t

        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x=clamp(newpos.x,Hero.pos_min_x,Hero.pos_max_x)
        newpos.y=clamp(newpos.y, Hero.pos_min_y, Hero.pos_max_y)
        self.rect.x = newpos.x
        self.rect.y = newpos.y


    def setVel(self, vec):
        """
            Method that update the velocity of the hero
            :param vec: new vector velocity
        """
        if vec != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vec.normalize()
        else:
        #if the new velocity vector is (0,0)
            self.vel=vec


def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
    """
    return max(min(maxn, n), minn)