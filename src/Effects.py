import pygame, sys
from pygame.locals import *

import random
Tile_size = 32

class effect(pygame.sprite.Sprite):
    def __init__(self, Zombiepos):
        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load('splat.png')
        self.rect = self.image.get_rect()
        self.rect.x = Zombiepos.x
        self.rect.y = Zombiepos.y
        self.spawn_time = pygame.time.get_ticks()
        self.splat_lifetime = 3500

    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):


        self.rate = pygame.time.get_ticks()
        if self.rate - self.spawn_time > self.splat_lifetime:
            self.kill()


class zombie_splat(effect):
    def __init__(self, Zombiepos):

        effect.__init__(self,Zombiepos)
        self.zombie_splat_img = pygame.image.load('splat.png')
        self.zombie_splat_img = pygame.transform.scale(self.zombie_splat_img, (Tile_size, Tile_size))
        self.image = self.zombie_splat_img

