import pygame, sys
import os
from pygame.locals import *

Tile_size = 32
Health_img = pygame.image.load("hp.png")
Shotgun_img = pygame.image.load("shotgun.png")

class Item(pygame.sprite.Sprite):



    def __init__(self, x,y, type): #x and y are the location of the hero


        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.health_image = pygame.transform.scale(Health_img, (Tile_size, Tile_size))
        self.shotgun_image = pygame.transform.scale(Shotgun_img, (Tile_size, Tile_size))
        self.type = type
        if type == "Hp":
            self.image = self.health_image
        elif type == "Shotgun":
            self.image = self.shotgun_image
        else:
            pass
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x * Tile_size
        self.rect.y = y * Tile_size

    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))
