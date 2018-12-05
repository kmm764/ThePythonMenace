import pygame, sys
from pygame.locals import *
import math
from random import uniform
import random

class Bullet(pygame.sprite.Sprite):

    

    def __init__(self, positionHero): #x and y are the location of the hero

        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite

        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.speed = 0
        self.Bullet_lifetime = 0

        self.rect.x = positionHero.x
        self.rect.y = positionHero.y
        self.last_shot = 0


        #here we set the velocity towards the position of the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = random.randint(mouse_x-100, mouse_x+100)
        mouse_y = random.randint(mouse_y - 100, mouse_y + 100)
        vel = pygame.math.Vector2(mouse_x - self.rect.x, mouse_y - self.rect.y)
        if vel != (0., 0.):
            #we turn it into a unit vector to get just the direction of the movement
            self.vel = vel.normalize()


        self.spawn_time = pygame.time.get_ticks()


    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))

      
    def update(self, t):


        newpos = pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*self.speed*t

        self.rect.x = newpos.x
        self.rect.y = newpos.y


        #kill it if it leaves the screen
        rate = pygame.time.get_ticks()
        if rate - self.spawn_time > self.Bullet_lifetime:
            self.kill()


class Pistol_bullet(Bullet):

    def __init__(self, positionHero):
        Bullet.__init__(self, positionHero)
        self.speed = 600
        self.Bullet_lifetime = 600


class Shotgun_Bullet(Bullet):

    def __init__(self, positionHero):
        Bullet.__init__(self, positionHero)
        self.speed = 600
        self.Bullet_lifetime = 200
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/2), int(self.size[1]/2)))
