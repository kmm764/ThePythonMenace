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
    zombie_IMG = pygame.image.load('img/zombies/zombie.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = Zombie.zombie_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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

    def setAngle(self, positionHero):
        self.rotate(positionHero.x, positionHero.y)


    def update(self, positionHero, t):
        self.setAngle(positionHero)
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(Zombie.zombie_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.setPos(t)


class SuperZombie(Zombie):
    zombie_IMG = pygame.image.load('img/zombies/bigZombie.png')
    life_bar_img = ["life_bar_empty_zombie.png", "life_bar_half_zombie.png", "life_bar_full_zombie.png"]
    for b in range(len(life_bar_img)):
        life_bar_img[b] = pygame.image.load("img/effects/life_bar/superzombie/"+life_bar_img[b])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = SuperZombie.zombie_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lives = 3
        self.lives_img = SuperZombie.life_bar_img[self.lives - 1]
        self.img_height = 48
        self.img_width = 40
        self.pos_max_x = WIDTH - self.img_width
        self.pos_max_y = HEIGHT - self.img_height

    def updates_life(self, screen):
        self.lives -= 1
        self.lives_img = SuperZombie.life_bar_img[self.lives - 1]
        screen.blit(self.lives_img, self.rect.midtop)
        if self.lives == 0:
            self.kill()

    def life_bar_display(self, screen):
        screen.blit(self.lives_img, self.rect.midtop)


    def update(self, positionHero, t):
        self.setAngle(positionHero)
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(SuperZombie.zombie_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.setPos(t)
