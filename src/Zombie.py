import pygame

from src.Person import Person
from setting import *

import random



class Zombie(Person):
    speed=100 #set the module of velocity
    radius_min = 100
    zombie_IMG = pygame.image.load(ZOMBIE_IMG)

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
        self.lives = 1



    """----------------NEW CODE ----------------------------"""

    def trajectory_intention(self, positionHero):
        """
            Method that calculates the direction of the movement that the zombie is intended to have to chase the hero
        :param positionHero: vector position of the hero
        :return: a unit vector with the intention of the movement of the zombie
        """
        vel = pygame.math.Vector2(positionHero.x - self.rect.x, positionHero.y - self.rect.y)
        if vel != (0., 0.):
            # if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            return vel.normalize()
        else:
            return vel

    def hero_near(self, positionHero):
        """
            Method that check if the hero is closer than 100 pixels from the position where the zombie is
        :param positionHero: vector position of the hero
        :return: True if the hero is nearer than 100 pixels. False if not.
        """
        if abs(positionHero.x - self.rect.x) < Zombie.radius_min or abs(positionHero.y - self.rect.y) < Zombie.radius_min:
            return True
        else:
            return False

    def set_angle(self, positionHero):
        """
         Method that calls the rotate method of the super class, to set the value of the rotation angle of the zombie,
         to make him face the hero when he is chasing him
        :param positionHero: vector position of the hero
        :return:
        """
        self.rotate(positionHero.x, positionHero.y)

    def updates_life(self):
        """
        Method that substracts a life to the total lives of the zombie. And kill him from the groups if his lives left are zero.
        :return: True if the zombie has been killed
        """
        self.lives -= 1
        if self.lives == 0:
            self.kill()
            return True

    def update(self, positionHero, t):
        """
            Method that update the position and the orientation of the zombie
        :param positionHero: vector position of the hero
        :param t: time passed from the last update
        """
        self.set_angle(positionHero)
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(Zombie.zombie_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.set_pos(t)


class SuperZombie(Zombie):
    speed = 50
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

    def updates_life(self):
        """
            Method that overwrites the method of the parent class. It substracts a life to the total lives
             of the superzombie and update the life bar image. It kills him from the groups if his lives left are zero.
        :return: True if the zombie is killed
        """
        self.lives -= 1
        self.lives_img = SuperZombie.life_bar_img[self.lives - 1]
        if self.lives == 0:
            self.kill()
            return True


    def life_bar_display(self, screen):
        """
            Method that displays the life bar of the superzombie
        :param screen: Display object where the life bar will be display on
        :return:
        """
        screen.blit(self.lives_img, self.rect)


    def update(self, positionHero, t):
        """
            Method that update the position and the orientation of the zombie
        :param positionHero: vector position of the hero
        :param t: time passed from the last update
        """
        self.set_angle(positionHero)
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(SuperZombie.zombie_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.set_pos(t)
