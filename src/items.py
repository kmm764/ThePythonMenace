import pygame, sys
import os
from pygame.locals import *

Tile_size = 32
health_img = pygame.image.load("hp.png")
shotgun_img = pygame.image.load("shotgun.png")
horrocrux_img = pygame.image.load("hp.png")


class Item(pygame.sprite.Sprite):

    health_image = pygame.transform.scale(health_img, (Tile_size, Tile_size))
    shotgun_image = pygame.transform.scale(shotgun_img, (Tile_size, Tile_size))
    horrocrux_image = pygame.transform.scale(horrocrux_img, (Tile_size, Tile_size))

    def __init__(self, x,y, type):

        super().__init__()

        self.type = type
        if type == "Hp":
            self.image = Item.health_image
        elif type == "Shotgun":
            self.image = Item.shotgun_image
        else:
            self.image = Item.horrocrux_image

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))
