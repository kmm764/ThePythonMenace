import pygame, sys
from pygame.locals import *




class Bullet(pygame.sprite.Sprite):
    speed=200
    

    def __init__(self, positionHero): #x and y are the location of the hero
        
        super().__init__()
        #image and rect are the attributes used by the methods of the superclass sprite
        self.image = pygame.image.load('bulletRight.png')
        self.rect = self.image.get_rect()
        self.rect = positionHero
        #here we set the velocity towards the position of the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        vel = pygame.math.Vector2(mouse_x - self.rect.x, mouse_y - self.rect.y)
        if vel != (0., 0.):
            #we turn it into a unit vector to get just the direction of the movement
            self.vel = vel.normalize()


    
    def display(self, displayObj):

        displayObj.blit(self.image, (self.rect.x, self.rect.y))

      
    def update(self, t):


        newpos = pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*Bullet.speed*t

        self.rect.x = newpos.x
        self.rect.y = newpos.y


        #kill it if it leaves the screen
        if self.rect.x > 1000 or self.rect.x < 0:
            self.kill()
        if self.rect.y > 600 or self.rect.y < 0:
            self.kill()
