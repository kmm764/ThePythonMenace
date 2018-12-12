import pygame, sys
from pygame.locals import *
import math
import random
from setting import *

class Bullet(pygame.sprite.Sprite):


    def __init__(self, positionHero): #x and y are the location of the hero

        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load(BULLET_IMG)
        self.rect = self.image.get_rect()
        self.rect.x = positionHero.centerx
        self.rect.y = positionHero.centery
        self.last_shot = 0
        #here we set the velocity towards the position of the mouse
        self.spawn_time = pygame.time.get_ticks()


    def display(self, displayObj):
        """
        Method that displays the Bullet
        :param displayObj: Display object where the bullet object will be display on
        :return:
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))

      
    def update(self, t):
        """
        Method updates the bullet class
        :param t: time related to fpsclock.tick
        :return:
        """

        newpos = pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*self.speed*t
        self.rect.x = newpos.x
        self.rect.y = newpos.y
        #kill it if it leaves the screen
        rate = pygame.time.get_ticks()
        if rate - self.spawn_time > self.bullet_lifetime:
            self.kill()


class PistolBullet(Bullet):
    """
    inherit the Bullet class, and change the bullet speed, lifetime
    """
    def __init__(self, positionHero):
        Bullet.__init__(self, positionHero)
        self.speed = 600
        self.bullet_lifetime = 600
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        vel = pygame.math.Vector2(self.mouse_x - self.rect.x, self.mouse_y - self.rect.y)
        if vel != (0., 0.):
            # we turn it into a unit vector to get just the direction of the movement
            self.vel = vel.normalize()

class ShotgunBullet(Bullet):
    """
    inherit the Bullet class, and change the image size, bullet speed, lifetime, and add random bullet shooting direction
    """
    def __init__(self, positionHero):
        Bullet.__init__(self, positionHero)
        self.speed = 600
        self.bullet_lifetime = 350
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/2), int(self.size[1]/2)))
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        # make the location for vel random between 100 and -100 from the mouse location for both x and y
        self.mouse_x = random.randint(self.mouse_x - 100, self.mouse_x + 100)
        self.mouse_y = random.randint(self.mouse_y - 100, self.mouse_y + 100)
        vel = pygame.math.Vector2(self.mouse_x - self.rect.x, self.mouse_y - self.rect.y)
        if vel != (0., 0.):
            # we turn it into a unit vector to get just the direction of the movement
            self.vel = vel.normalize()
