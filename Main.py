import pygame, sys
from pygame.locals import *
import random


# from src.Game import Game
from src.Hero import Hero
from src.Zombie import Zombie


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('8-Bit Madness', 50)

WIDTH = 1000
HEIGHT = 600
img_width = 60
img_height = 60
FPS = 30  # frames per second setting
vel_x, vel_y = 0., 0. #inicializes the x and y components of the velocity vector of the hero
lasthit_time=2.0 #inicializes the time variable that we are going to use to limit the collisions between the hero and the zombies
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS

displayObj = pygame.display.set_mode((WIDTH, HEIGHT)) #creates the object that display the screen
pygame.display.set_caption('Game')
background_image = pygame.image.load("background.jpeg").convert()


WHITE = (255, 255, 255)

#creates an object of the class Hero
ourHero = Hero()

#here we create a sprite group to make easier to manage our zombies instances
crewZombies = pygame.sprite.Group()


pygame.key.set_repeat(1, 10) #to handle the "holding key" event

pygame.display.flip()

while True:  # the main game loop
    displayObj.blit(background_image, [0, 0])
    if random.randrange(0, 100) < 1:  #here, a probability of 1% is assigned to the appearance of a new zombie
        #if a new zombie instance is created, it is added to the sprite group
        crewZombies.add(Zombie(random.randrange(0, WIDTH-img_width), random.randrange(0, HEIGHT-img_height)))
    #displayObj.fill(WHITE)  # set the background to white
    ourHero.display(displayObj)  # the hero is displayed
    lives_counter = myfont.render('LIVES: '+str(ourHero.lives), False, (0,0,0))
    displayObj.blit(lives_counter, (WIDTH - 180,0))


    crewZombies.draw(displayObj) # the zombies of the group are displayed

    #here we check if it has been any collision between any sprite of the group crewZombies and the hero
    hero_zombies_collision = pygame.sprite.spritecollide(ourHero, crewZombies, False)

    for zombie in hero_zombies_collision:
        #for each zombie that has taken part in the collision, we check if it's been at least 2 seconds from the last collision that was counted
        lasthit_time += time_passed_s
        if lasthit_time >= 2.0:
            ourHero.lives -= 1 #here our hero loses one life per zombie in the collisions list
            lasthit_time=0.0 #set the time from the last collision to hero


    hero_zombies_collision.clear()


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
    #the function update of the sprite group basically calls the update function of each sprite of the group
    #so the zombies update method changes its position, based on the position of the hero the time passed
    crewZombies.update(ourHero.rect, time_passed_s)

    pygame.display.flip() #DO WE NEED BOTH OS THESE?!!!! update the screen with what we've drawn
    pygame.display.update() #updates the state of the game



