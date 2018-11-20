import pygame, sys
from pygame.locals import *


# from src.Game import Game
from src.Hero import Hero


FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS

displayObj = pygame.display.set_mode((1000, 600)) #creates the object that display the screen
pygame.display.set_caption('Game')

WHITE = (255, 255, 255)

#creates an object of the class Hero
ourHero = Hero()
pygame.key.set_repeat(1, 10) #to handle the "holding key" event

vel_x, vel_y = 0., 0. #inicializes the x and y components of the velocity vector of the hero

while True:  # the main game loop
    displayObj.fill(WHITE)  # set the background to white
    ourHero.display(displayObj) #the hero is displayed

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # ends pygame
            sys.exit()  # ends the program
        if event.type == KEYUP:
            # handles if a key is released
            if event.key in (K_LEFT, K_a) or ourHero.pos.x <= 0:
                vel_x = 0.
            if event.key in (K_RIGHT, K_d) or ourHero.pos.x >=940:
                vel_x = 0.
            if event.key in (K_UP, K_w) or ourHero.pos.y <= 0:
                vel_y = 0.
            if event.key in (K_DOWN, K_s):
                vel_y = 0.
        if event.type == KEYDOWN:
        #handles if a key is pressed, and moves the hero
            if event.key in (K_LEFT, K_a) and ourHero.pos.x >= 0:
                vel_x = -1.
            if event.key in (K_RIGHT, K_d) and ourHero.pos.x <= 940:
                vel_x = 1.
            if event.key in (K_UP, K_w) and ourHero.pos.y >= 0:
                vel_y = -1.
            if event.key in (K_DOWN, K_s) and ourHero.pos.y <= 540:
                vel_y = 1.
        # once the keys have been read, the method setVel is called to modify the velocity of the hero
        ourHero.setVel(pygame.math.Vector2(vel_x, vel_y))

    # sets the frames per second to our clock object and store the time passed from the last call in time_passed_ms
    time_passed_ms = fpsClock.tick(FPS)

    # converts the time to seconds
    time_passed_s = time_passed_ms / 1000.0
    #call the hero method to update its position, based on the time passed and its velocity
    ourHero.setPos(time_passed_s)

    pygame.display.update() #updates the state of the game



