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

    hero_IMG = pygame.image.load("img/Hero/Hero.png")
    #life_bar_full = pygame.image.load("life_bar_full.png")
    #life_bar_3 = pygame.image.load("life_bar_3.png")
    #life_bar_half = pygame.image.load("life_bar_half.png")
    #life_bar_1 = pygame.image.load("life_bar_1.png")
    #life_bar_empty = pygame.image.load("life_bar_empty.png")

    life_bar_img = ["life_bar_empty.png","life_bar_1.png","life_bar_half.png","life_bar_3.png","life_bar_full.png"]

    bullets_img = ["bullets_1.png", "bullets_2.png","bullets_3.png","bullets_4.png","bullets_5.png","bullets_6.png"]

    for z in range(len(bullets_img)):
        bullets_img[z] = pygame.image.load("img/effects/shotgun_ammo/"+bullets_img[z])
    for b in range(len(life_bar_img)):
        life_bar_img[b] = pygame.image.load("img/effects/life_bar/player/"+life_bar_img[b])

    backpack_icon = pygame.image.load("img/effects/backpack_icon.png")
    score_icon = pygame.image.load("img/effects/score_icon.png")

    def __init__(self):
        super().__init__()
        self.image = Hero.hero_IMG
        self.rect = self.image.get_rect()
        self.rect.x = INI_HERO_X
        self.rect.y = INI_HERO_Y
        self.vel = pygame.math.Vector2(0.0, 0.0) #inicialize the velocity vector to 0,0
        self.pos = self.rect
        self.score = 0
        self.lives = Hero.lives_ini
        self.lives_img = Hero.life_bar_img[len(Hero.life_bar_img)-1]

        self.ammo_img = self.bullets_img[len(Hero.bullets_img)-1]

        self.backpack_icon = Hero.backpack_icon
        self.score_icon = Hero.score_icon
        self.img_width = 49
        self.img_height = 43
        self.pos_max_x = WIDTH - self.img_width
        self.pos_max_y = HEIGHT - self.img_height
        self.backpack_collected = 0

    def get_rot_mouse(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rotate(mouse_x, mouse_y)

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
        self.lives_img = Hero.life_bar_img[num_lives-1]

    def update_ammo(self, num_bullets):

        self.ammo_img = Hero.bullets_img[(num_bullets-1)]


    def update(self,t):
        self.get_rot_mouse()
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(Hero.hero_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.setPos(t)

    def ifCheckpoint(self,cp_xmin, cp_xmax,cp_ymin, cp_ymax):
        if self.rect.centerx > cp_xmin and self.rect.centerx < cp_xmax  and self.rect.centery > cp_ymin and self.rect.centery < cp_ymax:
            return True

