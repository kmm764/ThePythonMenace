import pygame, sys
from pygame.locals import *
from src.Person import Person

import math

WIDTH = 1024
HEIGHT = 768
INI_HERO_X = 416
INI_HERO_Y = 224
tile_size = 32
img_width = 49
img_height = 43
RED = (255, 0, 0)
pygame.font.init()
fontlives = pygame.font.SysFont('8-Bit Madness', 15)

class Hero(Person):

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    speed = 150  # set the module of velocity


    lives_ini = 5

    hero_IMG = pygame.image.load("Hero.png")
    hero_IMG = pygame.image.load("Hero.png")
    life_bar_full = pygame.image.load("life_bar_full.png")
    life_bar_3 = pygame.image.load("life_bar_3.png")
    life_bar_half = pygame.image.load("life_bar_half.png")
    life_bar_1 = pygame.image.load("life_bar_1.png")
    life_bar_empty = pygame.image.load("life_bar_empty.png")
    bullets_6 = pygame.image.load("bullets_6.png")
    bullets_5 = pygame.image.load("bullets_5.png")
    bullets_4 = pygame.image.load("bullets_4.png")
    bullets_3 = pygame.image.load("bullets_3.png")
    bullets_2 = pygame.image.load("bullets_2.png")
    bullets_1 = pygame.image.load("bullets_1.png")
    backpack_icon = pygame.image.load("backpack_icon.png")
    score_icon = pygame.image.load("score_icon.png")

    def __init__(self):
        super().__init__()
        self.image = Hero.hero_IMG
        self.rect = self.image.get_rect()
        self.rect.x = INI_HERO_X
        self.rect.y = INI_HERO_Y
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0
        self.rot = 0
        self.rot_speed = 0
        self.angle = 0
        self.pos = self.rect
        self.orientation = pygame.math.Vector2(1.0, 0.0) #inicialize the orientation vector to 0,0
        self.score = 0
        self.lives = Hero.lives_ini
        self.lives_img = Hero.life_bar_full
        self.ammo_img = Hero.bullets_6
        self.backpack_icon = Hero.backpack_icon
        self.score_icon = Hero.score_icon
        self.img_width = 49
        self.img_height = 43
        self.pos_max_x = WIDTH - self.img_width
        self.pos_max_y = HEIGHT - self.img_height
        self.backpack_collected = 0


    def get_rot_mouse(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        # we change the orientation of the vector
        if self.orientation.rotate(self.angle)!= (0.0,0.0):
            self.orientation = self.orientation.rotate(-self.angle)

    def setPos2(self, x, y):

        self.rect.x = x
        self.rect.y = y

    def under_attack_display(self, screen):
        attack_effect = fontlives.render("-200",False,RED)
        screen.blit(attack_effect,(self.rect.centerx, self.rect.centery - self.img_height-5))


    def update_livebar(self, num_lives):
        """
            Method that update the life bar image when the hero gain or lose lives
            :param num_lives : number of lifes left
        """
        if num_lives == 5:
            self.lives_img = Hero.life_bar_full
        if num_lives == 4:
            self.lives_img = Hero.life_bar_3
        if num_lives == 3:
            self.lives_img = Hero.life_bar_half
        if num_lives == 2:
            self.lives_img = Hero.life_bar_1
        if num_lives == 1:
            self.lives_img = Hero.life_bar_empty
        else:
            pass


    def update_ammo(self, num_bullets):
        if num_bullets == 6:
            self.ammo_img = Hero.bullets_6
        if num_bullets == 5:
            self.ammo_img = Hero.bullets_5
        if num_bullets == 4:
            self.ammo_img = Hero.bullets_4
        if num_bullets == 3:
            self.ammo_img = Hero.bullets_3
        if num_bullets == 2:
            self.ammo_img = Hero.bullets_2
        if num_bullets == 1:
            self.ammo_img = Hero.bullets_1
        else:
            pass
        

    def update(self,t):
        self.get_rot_mouse()
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(Hero.hero_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.setPos(t)

    def ifCheckpoint(self,cp_xmin, cp_xmax,cp_ymin, cp_ymax):
        if self.rect.centerx > cp_xmin and self.rect.centerx < cp_xmax  and self.rect.centery > cp_ymin and self.rect.centery < cp_ymax:
            return True

