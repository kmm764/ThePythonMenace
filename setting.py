import pygame, sys
from pygame.locals import *
'''--------Main--------'''

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#game options
WIDTH = 1024
HEIGHT = 768
FPS = 60  # frames per second setting
img_width = 60
img_height = 60
TILE_SIZE = 32

'''Hero'''
Player_sound = ["p0.wav", "p1.wav", "p2.wav", "p3.wav", "p4.wav", "p5.wav", "p6.wav"]


'''Zombies'''

FREQUENCY_ZOMBIE = 10
PROBABILITY_SUPERZOMBIE = 70
Zombie_sound = ["z0.wav", "z1.wav", "z2.wav", "z3.wav", "z4.wav", "z5.wav", "z6.wav", "z7.wav"]



'''guns'''
PISTOL_SOUND = "snd/pistol.wav"
SHOTGUN_SOUND = "snd/shotgun.wav"
GUN_PICKUP_SOUND = "snd/gun_pickup.wav"





'''items'''
FREQUENCY_GUN = 3
FREQUENCY_LIVES = 5
MAX_BACKPACKS = 5

'''effects'''


TIME_DISPLAY_SPLASH = 3000
TIME_DISPLAY_RED = 250