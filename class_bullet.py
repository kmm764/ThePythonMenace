#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:50:46 2018

@author: oceancio
"""

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): #x and y are the location of the hero
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(255, 255, 0) #yellow
        self.rect = self.image.get_rect() #create bullet as a rectangle
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    
    def update(self):
        self.rect.y += self.speedy #just upwards
        #kill it if it leaves the screen
        if self.rect.bottom < 0:
            self.kill()

#for main game (event in pygame)
if event.key == pygame.K_SPACE:
    ourHero.shoot()

#shoot function
def shoot(self):
    bullet = Bullet(self.rect.centerx, self.rect.top)
    all_sprites.add(bullet) #add bullet to all sprites
    bullets.add(bullet)