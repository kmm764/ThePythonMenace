import pygame, sys
from pygame.locals import *
import random


import os
from os import path

from src.Game import Game

from src.Hero import Hero
from src.Zombie import Zombie
from src.Bullet import *
from src.Game import Game
from src.Wall import Walls
from src.items import Item




"""----------------------PARAMETERS----------------------------"""
WIDTH = 1024
HEIGHT = 768
img_width = 60
img_height = 60
Tile_size = 32
GridWidth = WIDTH/Tile_size
GridHeight = HEIGHT/Tile_size
last_shot = 0
FPS = 60  # frames per second setting
vel_x, vel_y = 0., 0. #inicializes the x and y components of the velocity vector of the hero
lasthit_time=2.0 #inicializes the time variable that we are going to use to limit the collisions between the hero and the zombies
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
frecuency_Zombie = 3
FRECUENCY_GUN = 1
FRECUENCY_LIVES = 1
map_data = []
shotgun_ammo = 0
play_mode = False
menu_mode = False
game_folder = path.dirname(__file__)


"""----------------------PYGAME INITIALIZING---------------------------"""
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('8-Bit Madness', 50)
Pistol_sound = pygame.mixer.Sound("pistol.wav")
Shotgun_sound = pygame.mixer.Sound("shotgun.wav")
Gun_pickup = pygame.mixer.Sound("gun_pickup.wav")
fpsClock = pygame.time.Clock()  #this object will make sure our program runs at a certain maximum FPS



"""----------------------SCREEN OBJECT----------------------------"""
displayObj = pygame.display.set_mode((WIDTH, HEIGHT)) #creates the object that display the screen
pygame.display.set_caption('Game')
background_image = pygame.image.load("background.jpg").convert()




"""----------------------GAME OBJECT: display start screen ans menu----------------------------"""
game = Game()
# show start screen
menu_mode = game.show_start_screen(displayObj)
# show the menu
play_mode = game.menu(displayObj)



"""----------------------INITIAL INSTANCES AND GROUPS CREATION----------------------------"""
ourHero = Hero()
# display the life bar on the screen
displayObj.blit(ourHero.lives_img, (WIDTH - 200, 0))
#here we create a sprite group to make easier to manage our zombies instances
crewZombies = pygame.sprite.Group()
groupBullets = pygame.sprite.Group()
ourWall = pygame.sprite.Group()
ourItems = pygame.sprite.Group()
#pygame.key.set_repeat(1, 10) #to handle the "holding key" event
weaponType = "Pistol"
pygame.display.flip()


"""----------------------MAP CREATION----------------------------"""

with open(path.join(game_folder, 'map.txt'), 'rt') as f:  #rf is read
    for line in f:
        map_data.append(line)



while play_mode:  # the main game loop
    if len(ourWall) == 0:
        for row, tiles in enumerate(map_data):  # enumerate to get both index and value as row and column
            for col, tile in enumerate(tiles):
                if tile == "1":
                    ourWall.add(Walls(col, row, Tile_size))


    displayObj.blit(background_image, [0, 0])

    if random.randrange(0, 100) < frecuency_Zombie :  #here, a probability of 5% is assigned to the appearance of a new zombie
        #if a new zombie instance is created, it is added to the sprite group
        crewZombies.add(Zombie(random.randrange(0, WIDTH-img_width), random.randrange(0, HEIGHT-img_height)))

    if random.randrange(0, 1000) < FRECUENCY_GUN:
        ourItems.add(Item(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), "Shotgun"))
    if random.randrange(0, 1000) < FRECUENCY_LIVES:
        ourItems.add(Item(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), "Hp"))



    """----------------------OBJECTS DISPLAY----------------------------"""
    ourHero.display(displayObj)
    Shotgun_ammo_count = myfont.render('Shotgun Ammo: '+str(shotgun_ammo), False, (0,0,0))
    displayObj.blit(ourHero.lives_img, (WIDTH - 200,0))
    displayObj.blit(Shotgun_ammo_count, (WIDTH - 350, 30))
    # we display score
    score_counter = myfont.render('SCORE: ' + str(ourHero.score), False, (255, 255, 255))
    displayObj.blit(score_counter, (WIDTH - 180, HEIGHT-200))
    crewZombies.draw(displayObj) # the zombies of the group are displayed
    groupBullets.draw(displayObj)
    #ourWall.draw(displayObj)
    ourItems.draw(displayObj)

    """----------------------COLLISIONS CHECKING----------------------------"""
    hero_zombies_collision = pygame.sprite.spritecollide(ourHero, crewZombies, False)
    hero_wall_collision = pygame.sprite.spritecollide(ourHero, ourWall, False)
    hero_item_collision = pygame.sprite.spritecollide(ourHero, ourItems, False)

    for zombie in hero_zombies_collision:
        #for each zombie that has taken part in the collision, we check if it's been at least 2 seconds from the last collision that was counted
        lasthit_time += time_passed_s
        if lasthit_time >= 2.0:
            ourHero.lives -= 1 #here our hero loses one life per zombie in the collisions list
            ourHero.update_livebar(ourHero.lives)
            lasthit_time=0.0 #set the time from the last collision to hero
            if ourHero.lives == 0: # If Hero dies show Game Over screen
                if game.show_over_screen(displayObj,ourHero.score) == True:
                    ourHero = Hero()
                    displayObj.blit(ourHero.lives_img, (WIDTH - 200, 0))
                    crewZombies = pygame.sprite.Group()
                    groupBullets = pygame.sprite.Group()
                    ourWall = pygame.sprite.Group()
                    pygame.display.flip()

    for hit in hero_item_collision:
        if hit.type == "Hp" and ourHero.lives < 4:
            hit.kill()
            ourHero.lives += 1
            ourHero.update_livebar(ourHero.lives)
        elif hit.type == "Shotgun":
            hit.kill()
            pygame.mixer.Sound.play(Gun_pickup)
            weaponType = "Shotgun"
            shotgun_ammo = 6


    # here we check the collision between the bullets and the zombies, if they collision, the zombies deleted from the groups
    if len(groupBullets.sprites())>0:
        for bul in groupBullets:
            bullet_zombies_collision = pygame.sprite.spritecollide(bul, crewZombies, True)
            bullet_wall_collision = pygame.sprite.spritecollide(bul, ourWall, False)
            # if there is a collision the bullets is also deleted from the group
            if len(bullet_wall_collision) > 0:
                bul.kill()
            if len(bullet_zombies_collision) > 0:
                bul.kill()
                ourHero.score += 1

    hero_zombies_collision.clear()

    """----------------------EVENTS HANDLING----------------------------"""
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
                now=pygame.time.get_ticks()

                if weaponType == "Pistol":
                    Bullet_Rate = 350
                    if now - last_shot > Bullet_Rate:
                            last_shot = now
                            groupBullets.add(Pistol_bullet(ourHero.rect))
                            pygame.mixer.Sound.play(Pistol_sound)
                elif weaponType == "Shotgun":
                    Bullet_Rate = 1200
                    if now - last_shot > Bullet_Rate:
                        last_shot = now
                        if shotgun_ammo > 0:
                            shotgun_ammo -= 1
                            for x in range(10):
                                groupBullets.add(Shotgun_Bullet(ourHero.rect))
                                pygame.mixer.Sound.play(Shotgun_sound)
                        else:
                            weaponType = "Pistol"

    #colision of the hero with the wall, and change in the velocity
    for wall in ourWall:

        if (ourHero.rect.x >= wall.rect.x-Tile_size) and (ourHero.rect.x <= wall.rect.x) and vel_y == 1. and (ourHero.rect.y + img_width) >= wall.rect.y and (ourHero.rect.y <= wall.rect.y+ Tile_size):

            ourHero.rect.y = (wall.rect.y - img_width)
            vel_y = 0.

        if (ourHero.rect.x >= wall.rect.x - Tile_size) and (ourHero.rect.x <= wall.rect.x) and vel_y == -1. and (ourHero.rect.y <= wall.rect.y + Tile_size) and (ourHero.rect.y >= wall.rect.y):
            ourHero.rect.y = (wall.rect.y + Tile_size)
            vel_y = 0.
        if (ourHero.rect.y+20 >= wall.rect.y - Tile_size) and (ourHero.rect.y <= wall.rect.y) and (ourHero.rect.x + img_width >= wall.rect.x) and (ourHero.rect.x <= wall.rect.x+Tile_size) and vel_x == 1. :
            ourHero.rect.x = (wall.rect.x - img_width)
            vel_x = 0.
        if (ourHero.rect.y+20 >= wall.rect.y - Tile_size) and (ourHero.rect.y <= wall.rect.y) and (ourHero.rect.x >= wall.rect.x) and (ourHero.rect.x <= wall.rect.x+Tile_size) and vel_x == -1. :

            ourHero.rect.x = (wall.rect.x + Tile_size)
            vel_x = 0.



    """----------------------OBJECTS UPDATE----------------------------"""
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


    pygame.display.flip() #DO WE NEED BOTH OS THESE?!!!! update the screen with what we've drawn
    pygame.display.update() #updates the state of the game



