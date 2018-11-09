import pygame, sys
from pygame.locals import *

class Hero:
    x_var=5
    y_var=5
    def __init__(self):
        self.x=0
        self.y=0
        self.Img = pygame.image.load('bloomy.png')
    def move_x(self,dir):
        """
        Method that move the hero in the x axis
        :param dir: p if x position increases, n if x position decreases
        """
        if dir == "p":
            self.x += Hero.x_var
        else:
            self.x -= Hero.x_var

    def move_y(self,dir):
        """
        Method that move the hero in the y axis
        :param dir: p if y position increases, n if y position decreases
        """
        if dir == "p":
            self.y += Hero.y_var
        else:
            self.y -= Hero.y_var
