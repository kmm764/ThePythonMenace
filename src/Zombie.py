import pygame, sys
from pygame.locals import *

import random

tile_size=32


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
        self.vel = pygame.math.Vector2(0.0, 0.0) #initialize the velocity vector to 0,0
        self.img_height = 43
        self.img_width = 35


    def display(self, displayObj):
        """
            Method that displays the zombie
            :param displayObj --> Object display where the hero will be display on
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))

    """----------------NEW CODE ----------------------------"""

    def trajectory_intention(self, positionHero):
        vel = pygame.math.Vector2(positionHero.x - self.rect.x, positionHero.y - self.rect.y)
        if vel != (0., 0.):
            # if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            return vel.normalize()
        else:
            return vel

    def collision_wall_y(self, wallx, wally):
        """

        :param wallx: rect.centerx of the wall object
        :param wally: rect.centery of the wall object
        :return:
        """
        dist_center_xmin = self.img_width / 2 + tile_size / 2
        dist_center_ymin = self.img_height / 2 + tile_size / 2
        margin = 5

        if self.rect.centery > wally - dist_center_ymin and self.rect.centery < wally and self.rect.centerx > wallx - dist_center_xmin + margin and self.rect.centerx < wallx + dist_center_xmin - margin:
            return "top"
        elif self.rect.centery < wally + dist_center_ymin and self.rect.centery > wally and self.rect.centerx > wallx - dist_center_xmin + margin and self.rect.centerx < wallx + dist_center_xmin - margin:
            return "bottom"
        else:
            return "none"

    def collision_wall_x(self, wallx, wally):
        """

        :param wallx: rect.centerx of the wall object
        :param wally: rect.centery of the wall object
        :return:
        """
        dist_center_xmin = self.img_width / 2 + tile_size / 2
        dist_center_ymin = self.img_height / 2 + tile_size / 2
        margin = 5
        if self.rect.centerx > wallx - dist_center_xmin and self.rect.centerx < wallx and self.rect.centery <= wally + dist_center_ymin - margin and self.rect.centery >= wally - dist_center_ymin + margin:
            return "left"
        elif self.rect.centerx < wallx + dist_center_xmin and self.rect.centerx > wallx and self.rect.centery <= wally + dist_center_ymin - margin and self.rect.centery >= wally - dist_center_ymin + margin:
            return "right"
        else:
            return "none"

    def setVel(self, vec):
        """
            Method that update the velocity of the hero
            :param vec: new vector velocity
        """
        if vec != (0., 0.):
            # if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vec.normalize()
        else:
            # if the new velocity vector is (0,0)
            self.vel = vec

    def setPos(self, t):
        """
            Method that updates the position of the hero, based on the time passed and the velocity of the hero
            :param t --> time passed in seconds from the last call
        """
        #Here, the new position vector is calculated. The attibute rect is turned into a 2d vector class to make easier the operations


        newpos =  pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*self.speed*t

        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x=clamp(newpos.x,Zombie.pos_min_x,Zombie.pos_max_x)
        newpos.y=clamp(newpos.y, Zombie.pos_min_y, Zombie.pos_max_y)
        self.pos = newpos
        self.rect.x = newpos.x
        self.rect.y = newpos.y

    def update(self, t):
        self.setPos(t)




"""
    def setVel(self, positionHero):

        vel = pygame.math.Vector2(positionHero.x - self.rect.x, positionHero.y - self.rect.y)
        if vel != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vel.normalize()
        else:
            pass

    def update(self, positionHero, t):

        self.setVel(positionHero)

        # calculates the new position vector, to do so, the attibute rect is turned into a 2d vector to make easier the operations
        newpos = pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*(random.randint(self.speed -20, self.speed +20))*t
        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x= clamp(newpos.x,Zombie.pos_min_x,Zombie.pos_max_x)
        newpos.y= clamp(newpos.y, Zombie.pos_min_y, Zombie.pos_max_y)
        self.rect.x = newpos.x
        self.rect.y = newpos.y
        
    """

def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
    """
    return max(min(maxn, n), minn)