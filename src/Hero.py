import pygame, sys
from pygame.locals import *
from src.Wall import *
import math

WIDTH = 1024
HEIGHT = 768
img_width = 60
img_height = 60
INI_HERO_X = 416
INI_HERO_Y = 224

class Hero(pygame.sprite.Sprite):

    # set the max and min position in each axis to prevent the hero from go outside the boundaries of the screen
    speed = 100  # set the module of velocity
    pos_max_x=WIDTH-img_width
    pos_max_y=HEIGHT-img_height
    pos_min_x=0
    pos_min_y=0
    lives_ini = 4
    hero_IMG = pygame.image.load("Hero.png")
    hero_IMG = pygame.image.load("Hero.png")
    life_bar_full = pygame.image.load("life_bar_full.png")
    life_bar_3 = pygame.image.load("life_bar_3.png")
    life_bar_half = pygame.image.load("life_bar_half.png")
    life_bar_1 = pygame.image.load("life_bar_1.png")
    life_bar_empty = pygame.image.load("life_bar_empty.png")


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
    #def collide_with_walls(self,dir):
       # if dir = "x"
    
    def update_livebar(self, num_lives):
        if num_lives == 4:
            self.lives_img = Hero.life_bar_full
        if num_lives == 3:
            self.lives_img = Hero.life_bar_3
        if num_lives == 2:
            self.lives_img = Hero.life_bar_half
        if num_lives == 1:
            self.lives_img = Hero.life_bar_1
        if num_lives == 0:
            self.lives_img = Hero.life_bar_empty
        else:
            pass

    def update(self,t):
        self.get_rot_mouse()
        self.rot = (self.rot + self.rot_speed * t) % 360
        self.image = pygame.transform.rotate(Hero.hero_IMG, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.setPos(t)


def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
    """
    return max(min(maxn, n), minn)
