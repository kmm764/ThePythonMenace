import pygame, sys
from pygame.locals import *

Bulletspeed = 100


class Bullet(pygame.sprite.Sprite):
    

    def __init__(self, x, y): #x and y are the location of the hero
        
        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load('bulletRight.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = pygame.math.Vector2(0.0, 0.0)
        self.speed = Bulletspeed
    
    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))
    

      
    def update(self, t):
        
        #setVel(positionHero)
        #newpos = pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*self.speed
        self.rect.x += self.speed*t #just forward
        #kill it if it leaves the screen
        if self.rect.x > 1000 or self.rect.x < 0:
            self.kill()
        if self.rect.y > 600 or self.rect.y < 0:
            self.kill()
