import pygame, sys
from pygame.locals import *

from pynput.keyboard import Key, Listener
# from src.Game import Game
from src.Hero import Hero


FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS

displayObj = pygame.display.set_mode((1000, 600)) #creates the object
pygame.display.set_caption('Game')

WHITE = (255, 255, 255)

#creates an object of the class Hero
ourHero = Hero()
pygame.key.set_repeat(1, 10) #to handle the "holding key" event
key_up, key_down, key_left, key_right = False, False, False, False


while True:  # the main game loop
    displayObj.fill(WHITE)  # set the background to white
    ourHero.display(displayObj) #the hero is displayed
    #displayObj.blit(ourHero.Img, (ourHero.x, ourHero.y))  #add the img to the display object on the x,y coordinates

    if key_left == True and ourHero.x >= 0:
        ourHero.move_x("n")
    if key_right == True and ourHero.x <= 940:
        ourHero.move_x("p")
    if key_up == True and ourHero.y >= 0:
        ourHero.move_y("n")
    if key_down == True and ourHero.y <= 540:
        ourHero.move_y("p")

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # ends pygame
            sys.exit()  # ends the program
        if event.type == KEYDOWN:
        #handles if a key is pressed, and moves the hero
            if event.key in (K_LEFT, K_a) and ourHero.x >= 0:
                key_left = True
                #ourHero.move_x("n")
            if event.key in (K_RIGHT, K_d) and ourHero.x <= 940:
                key_right = True
                #ourHero.move_x("p")
            if event.key in (K_UP, K_w) and ourHero.y >= 0:
                key_up = True
                #ourHero.move_y("n")
            if event.key in (K_DOWN, K_s) and ourHero.y <= 540:
                key_down = True
                #ourHero.move_y("p")
        if event.type == KEYUP:
            # handles if a key is released
            if event.key in (K_LEFT, K_a):
                key_left = False
            if event.key in (K_RIGHT, K_d):
                key_right = False
            if event.key in (K_UP, K_w):
                key_up = False
            if event.key in (K_DOWN, K_s):
                key_down = False


    pygame.display.update() #updates the state of the game
    fpsClock.tick(FPS) #sets the frames per second to our clock object

