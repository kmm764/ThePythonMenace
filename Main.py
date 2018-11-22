import pygame, sys
from pygame.locals import *
import random


# from src.Game import Game
from src.Hero import Hero
from src.Zombie import Zombie

WIDTH = 1000
HEIGHT = 600
img_width = 60
img_height = 60
FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS

displayObj = pygame.display.set_mode((WIDTH, HEIGHT)) #creates the object that display the screen
pygame.display.set_caption('Game')

WHITE = (255, 255, 255)

#creates an object of the class Hero
ourHero = Hero()
crewZombies = pygame.sprite.Group()

crewZombies.add(Zombie(random.randrange(0,WIDTH-img_width), random.randrange(0,HEIGHT-img_height)))



pygame.key.set_repeat(1, 10) #to handle the "holding key" event

pygame.display.flip()
vel_x, vel_y = 0., 0. #inicializes the x and y components of the velocity vector of the hero

while True:  # the main game loop

    if random.randrange(0, 100) < 1:  #here, a probability of 1% is assigned to the appearance of a new zombie
        crewZombies.add(Zombie(random.randrange(0, WIDTH-img_width), random.randrange(0, HEIGHT-img_height)))
    displayObj.fill(WHITE)  # set the background to white
    ourHero.display(displayObj)  # the hero is displayed
    crewZombies.draw(displayObj)
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # ends pygame
            sys.exit()  # ends the program
        if event.type == KEYUP:
            # handles if a key is released
            if event.key in (K_LEFT, K_a):
                vel_x = 0.
            if event.key in (K_RIGHT, K_d):
                vel_x = 0.
            if event.key in (K_UP, K_w):
                vel_y = 0.
            if event.key in (K_DOWN, K_s):
                vel_y = 0.
        if event.type == KEYDOWN:
        #handles if a key is pressed, and moves the hero
            if event.key in (K_LEFT, K_a):
                vel_x = -1.
            if event.key in (K_RIGHT, K_d):
                vel_x = 1.
            if event.key in (K_UP, K_w):
                vel_y = -1.
            if event.key in (K_DOWN, K_s):
                vel_y = 1.
        # once the keys have been read, the method setVel is called to modify the velocity of the hero
        ourHero.setVel(pygame.math.Vector2(vel_x, vel_y))

    # sets the frames per second to our clock object and store the time passed from the last call in time_passed_ms
    time_passed_ms = fpsClock.tick(FPS)

    # converts the time to seconds
    time_passed_s = time_passed_ms / 1000.0
    #call the hero method to update its position, based on the time passed and its velocity
    ourHero.setPos(time_passed_s)
    crewZombies.update(ourHero.rect, time_passed_s)

    pygame.display.flip() #DO WE NEED BOTH OS THESE?!!!! update the screen with what we've drawn
    pygame.display.update() #updates the state of the game



