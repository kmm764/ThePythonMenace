import pygame, sys
from pygame.locals import *
import random
import os


# from src.Game import Game
from src.Hero import Hero
from src.Zombie import Zombie
from src.Bullet import Bullet
from src.Game import Game
from src.Wall import Walls


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('8-Bit Madness', 50)


WIDTH = 1024
HEIGHT = 768
img_width = 60
img_height = 60
Tile_size = 32
GridWidth = WIDTH/Tile_size
GridHeight = HEIGHT/Tile_size


FPS = 60  # frames per second setting
vel_x, vel_y = 0., 0. #inicializes the x and y components of the velocity vector of the hero
lasthit_time=2.0 #inicializes the time variable that we are going to use to limit the collisions between the hero and the zombies
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS

displayObj = pygame.display.set_mode((WIDTH, HEIGHT)) #creates the object that display the screen
pygame.display.set_caption('Game')
background_image = pygame.image.load("background.jpg").convert()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

play_mode = False
menu_mode = False

# create an object of the class Game
game = Game()
# show start screen
menu_mode = game.show_start_screen(displayObj)

# show the menu
play_mode = game.menu(displayObj)

#creates an object of the class Hero
ourHero = Hero()
# display the life bar on the screen
displayObj.blit(ourHero.lives_img, (WIDTH - 200, 0))

#here we create a sprite group to make easier to manage our zombies instances
crewZombies = pygame.sprite.Group()
groupBullets = pygame.sprite.Group()
ourWall = pygame.sprite.Group()

#pygame.key.set_repeat(1, 10) #to handle the "holding key" event

pygame.display.flip()

while play_mode:  # the main game loop

    displayObj.blit(background_image, [0, 0])

    if random.randrange(0, 100) < 3:  #here, a probability of 5% is assigned to the appearance of a new zombie
        #if a new zombie instance is created, it is added to the sprite group
        crewZombies.add(Zombie(random.randrange(0, WIDTH-img_width), random.randrange(0, HEIGHT-img_height)))
    #displayObj.fill(WHITE)  # set the background to white
    ourHero.display(displayObj)  # the hero is displayed

    #we display lives
    #lives_counter = myfont.render('LIVES: '+str(ourHero.lives), False, (0,0,0))
    displayObj.blit(ourHero.lives_img, (WIDTH - 200,0))

    # we display score
    score_counter = myfont.render('SCORE: ' + str(ourHero.score), False, (255, 255, 255))
    displayObj.blit(score_counter, (WIDTH - 180, HEIGHT-200))


    crewZombies.draw(displayObj) # the zombies of the group are displayed
    groupBullets.draw(displayObj)
    ourWall.draw(displayObj)

    for x in range(2,10):
        ourWall.add(Walls(x,1,Tile_size))


    #here we check if it has been any collision between any sprite of the group crewZombies and the hero
    hero_zombies_collision = pygame.sprite.spritecollide(ourHero, crewZombies, False)
    hero_wall_collision = pygame.sprite.spritecollide(ourHero, ourWall, False)

    for zombie in hero_zombies_collision:
        #for each zombie that has taken part in the collision, we check if it's been at least 2 seconds from the last collision that was counted
        lasthit_time += time_passed_s
        if lasthit_time >= 2.0:
            ourHero.lives -= 1 #here our hero loses one life per zombie in the collisions list
            ourHero.update_livebar(ourHero.lives)
            lasthit_time=0.0 #set the time from the last collision to hero
            if ourHero.lives == 0: # If Hero dies show Game Over screen
                game.show_over_screen(displayObj,ourHero.score)
                #ourHero.lives = 4 # hero's life back to 4
                ourHero.lives = ourHero.lives_ini



                
    # here we check the collision between the bullets and the zombies, if they collision, the zombies deleted from the groups
    if len(groupBullets.sprites())>0:
        for bul in groupBullets:
            bullet_zombies_collision = pygame.sprite.spritecollide(bul, crewZombies, True)
            bullet_wall_collision = pygame.sprite.spritecollide(bul, ourWall, True)
            # if there is a collision the bullets is also deleted from the group
            if len(bullet_wall_collision) > 0:
                bul.kill()
            if len(bullet_zombies_collision) > 0:
                bul.kill()
                ourHero.score += 1



    hero_zombies_collision.clear()


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # ends pygame
            os._exit(0)
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                groupBullets.add(Bullet(ourHero.rect))

        if hero_wall_collision:  # right

            if vel_x <0:
                ourHero.rect.left= hero_wall_collision[0].rect.right + 10
                #vel_x = 1
            elif vel_x > 0:
                ourHero.rect.right= hero_wall_collision[0].rect.left - 10
                #vel_x = -1

            if vel_y < 0:
                ourHero.rect.top = hero_wall_collision[0].rect.bottom + 10

                #vel_y = 1
            elif vel_y >0:
                ourHero.rect.bottom = hero_wall_collision[0].rect.top - 10
                #vel_y = -1





        # once the keys have been read, the method setVel is called to modify the velocity of the hero
        ourHero.setVel(pygame.math.Vector2(vel_x, vel_y))

    # sets the frames per second to our clock object and store the time passed from the last call in time_passed_ms
    time_passed_ms = fpsClock.tick(FPS)

    # converts the time to seconds
    time_passed_s = time_passed_ms / 1000.0
    #call the hero method to update its position, based on the time passed and its velocity

    #the function update of the sprite group basically calls the update function of each sprite of the group
    #so the zombies update method changes its position, based on the position of the hero the time passed
    crewZombies.update(ourHero.rect, time_passed_s)
    groupBullets.update(time_passed_s)
    ourHero.update(time_passed_s)

    for x in range(0 , WIDTH, Tile_size):
        pygame.draw.line(background_image, RED, (x,0),(x,HEIGHT))
    for y in range(0, HEIGHT, Tile_size):
        pygame.draw.line(background_image, RED, (0, y), (WIDTH, y))

    pygame.display.flip() #DO WE NEED BOTH OS THESE?!!!! update the screen with what we've drawn
    pygame.display.update() #updates the state of the game



