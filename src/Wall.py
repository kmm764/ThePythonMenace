import pygame, sys
from pygame.locals import *

import math

class Walls(pygame.sprite.Sprite):
    tile_IMG = pygame.image.load('tile.png')

    def __init__(self, x,y, Tile_size):  # x and y are the location of the hero

        Walls.tile_IMG = pygame.transform.scale(Walls.tile_IMG, (Tile_size,Tile_size))
        super().__init__()
        # image and rect are the attributes used by the methods of the superclass sprite
        self.image = Walls.tile_IMG
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*Tile_size
        self.rect.y = y*Tile_size

    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))

