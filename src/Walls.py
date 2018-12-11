import pygame, sys
from pygame.locals import *
from setting import *

import math


#  inspired by kidcancode@youtube, the way to use wall function alongside with the .txt file

class Walls(pygame.sprite.Sprite):
    tile_IMG = pygame.image.load(TILE_IMG)

    def __init__(self, x, y, TILE_SIZE):

        Walls.tile_IMG = pygame.transform.scale(Walls.tile_IMG, (TILE_SIZE, TILE_SIZE))
        super().__init__()
        self.image = Walls.tile_IMG
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def display(self, displayObj):
        """
        Method that displays the wall
        :param displayObj: Display object where the wall object will be display on
        :return:
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))

