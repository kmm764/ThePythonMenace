import pygame, sys
from pygame.locals import *

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

class Hero(pygame.sprite.Sprite):

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    speed = 150  # set the module of velocity
    pos_max_x=WIDTH-img_width
    pos_max_y=HEIGHT-img_height
    pos_min_x=0
    pos_min_y=0
    lives_ini = 5
    horrocrux_collected = 0
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
    hit_screen = pygame.image.load("red_screen.png")
    backpack_icon = pygame.image.load("backpack_icon.png")
    score_icon = pygame.image.load("score_icon.png")
    img_width = 49
    img_height = 43

    




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

        



        
    def get_rot_mouse(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        # we change the orientation of the vector
        if self.orientation.rotate(self.angle)!= (0.0,0.0):
            self.orientation = self.orientation.rotate(-self.angle)



        #self.rot_speed = 0
        #keys = pygame.key.get_pressed()
        #if keys[pygame .K_j]:
            #self.rot_speed = -250
        #if keys[pygame.K_k]:
            #self.rot_speed = 250


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
        self.pos = newpos
        self.rect.x = newpos.x
        self.rect.y = newpos.y

    def setPos2(self, x, y):

        self.rect.x = x
        self.rect.y = y

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
    """
    def collision_wall(self,wallx, wally):

        dist_center_xmin = self.img_width / 2 + tile_size / 2
        dist_center_ymin = self.img_height / 2 + tile_size / 2
        margin = 5
        if self.rect.centerx > wallx - dist_center_xmin and self.rect.centerx < wallx and self.rect.centery <= wally + dist_center_ymin - margin and self.rect.centery >= wally - dist_center_ymin + margin: # and vel_x > 0:
            print("left", end="")
            print(self.vel.x)
            return "left"
        elif self.rect.centerx < wallx + dist_center_xmin and self.rect.centerx > wallx and self.rect.centery <= wally + dist_center_ymin - margin and self.rect.centery >= wally - dist_center_ymin + margin:# and vel_x < 0:
            print("right", end="")
            print(self.vel.x)
            return "right"
        elif self.rect.centery > wally - dist_center_ymin and self.rect.centery < wally and self.rect.centerx > wallx - dist_center_xmin + margin and self.rect.centerx < wallx + dist_center_xmin -margin: # and vel_y > 0:
            print("top", end="")
            print(self.vel.y)
            return "top"
        elif self.rect.centery < wally + dist_center_ymin and self.rect.centery > wally and self.rect.centerx > wallx - dist_center_xmin + margin and self.rect.centerx < wallx + dist_center_xmin - margin: # and vel_y < 0:
            print("bottom",end="")
            print(self.vel.y)
            return "bottom"
        else:
            return "none"
    """
    def under_attack_display(self, screen):
        attack_effect = fontlives.render("-250",False,RED)
        screen.blit(attack_effect,(self.rect.centerx, self.rect.centery - self.img_height-5))

    def red_screen_display(self, screen):
        screen.blit(self.hit_screen, (0, 0))

    def under_attack(self):
        return pygame.time.get_ticks()

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


def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
        Source:https://stackoverflow.com/questions/5996881/how-to-limit-a-number-to-be-within-a-specified-range-python
    """
    return max(min(maxn, n), minn)
