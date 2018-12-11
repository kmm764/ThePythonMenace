import pygame, sys
from pygame.locals import *

import math


#  inspired by kidcancode@youtube
class Walls(pygame.sprite.Sprite):
    tile_IMG = pygame.image.load('img/background/tile.png')

    def __init__(self, x,y, Tile_size):

        Walls.tile_IMG = pygame.transform.scale(Walls.tile_IMG, (Tile_size,Tile_size))
        super().__init__()
        self.image = Walls.tile_IMG
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*Tile_size
        self.rect.y = y*Tile_size

    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))

