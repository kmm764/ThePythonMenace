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
from src.Walls import Walls
from src.items import Item
from src.Effects import *

"""----------------------PARAMETERS----------------------------"""
WIDTH = 1024
HEIGHT = 768
img_width = 60
img_height = 60
Tile_size = 32
dist_center_xmin = img_width / 2 + Tile_size / 2
dist_center_ymin = img_height / 2 + Tile_size / 2
GridWidth = WIDTH / Tile_size
GridHeight = HEIGHT / Tile_size

FPS = 60  # frames per second setting

lasthit_time = 2.0  # inicializes the time variable that we are going to use to limit the collisions between the hero and the zombies
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
frecuency_Zombie = 2
FRECUENCY_GUN = 100
FRECUENCY_LIVES = 5
MAX_HORROCRUX = 5
CHECKPOINT_X_MIN = 960
CHECKPOINT_Y_MAX = 256
CHECKPOINT_Y_MIN = 224
FINAL_XMAX = 480
FINAL_XMIN = 416
FINAL_YMAX = 352
FINAL_YMIN = 288
vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero
horrocrux_killed = 0
last_shot = 0
shotgun_ammo = 0
first_time = True
second_time = False
game_complete = False
maps = []
map_data = []
map2_data = []
map3_data = []
margin = 5 # we add a margin to make the movements more natural, as our hero image has transparents borders
play_mode = False
menu_mode = False
game_folder = path.dirname(__file__)

"""----------------------PYGAME INITIALIZING---------------------------"""
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('8-Bit Madness', 35)
Pistol_sound = pygame.mixer.Sound("pistol.wav")
Shotgun_sound = pygame.mixer.Sound("shotgun.wav")
Gun_pickup = pygame.mixer.Sound("gun_pickup.wav")
Player_sound = ["p0.wav", "p1.wav", "p2.wav", "p3.wav", "p4.wav", "p5.wav", "p6.wav"]
Zombie_sound = ["z0.wav", "z1.wav", "z2.wav", "z3.wav", "z4.wav", "z5.wav", "z6.wav", "z7.wav"]


for sounds in range(len(Player_sound)):
    Player_sound[sounds] = pygame.mixer.Sound(Player_sound[sounds])
    Player_sound[sounds].set_volume(2.0)

for z in range(len(Zombie_sound)):
    Zombie_sound[z] = pygame.mixer.Sound(Zombie_sound[z])
    Zombie_sound[z].set_volume(2.0)

fpsClock = pygame.time.Clock()  # this object will make sure our program runs at a certain maximum FPS

"""----------------------SCREEN OBJECT----------------------------"""

displayObj = pygame.display.set_mode((WIDTH, HEIGHT))  # creates the object that display the screen
pygame.display.set_caption('Game')


"""----------------------GAME OBJECT: display start screen ans menu----------------------------"""

game = Game()
# show start screen
menu_mode = game.show_start_screen(displayObj)
# show the menu
play_mode = game.menu(displayObj)

#initial music
level_1_sound= pygame.mixer.music.load("Level1.mp3")
pygame.mixer.music.play(2)

""" to display the instruccions
if play_mode == True:
    img_instructions = pygame.image.load("instructions_screen.png")
    displayObj.blit(img_instructions, (0, 0))
    pygame.display.flip()
    pygame.time.delay(10000)
"""

"""----------------------INITIAL INSTANCES AND GROUPS CREATION----------------------------"""
ourHero = Hero()
# display the life bar on the screen
displayObj.blit(ourHero.lives_img, (WIDTH - 200, 0))
# here we create a sprite group to make easier to manage our zombies instances
crewZombies = pygame.sprite.Group()
groupBullets = pygame.sprite.Group()
ourWall = pygame.sprite.Group()
ourItems = pygame.sprite.Group()
ourEffect = pygame.sprite.Group()
# pygame.key.set_repeat(1, 10) #to handle the "holding key" event
weaponType = "Pistol"
level = 1
pygame.display.flip()

"""-----------------------------MAP CREATION----------------------------"""

with open(path.join(game_folder, 'FirstMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map_data.append(line)

with open(path.join(game_folder, 'SecondMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map2_data.append(line)

with open(path.join(game_folder, 'ThirdMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map3_data.append(line)

"""----------------------------------------------------------------------------"""
"""--------------------------------GAME LOOP-----------------------------------"""
"""----------------------------------------------------------------------------"""

while play_mode:  # the main game loop

    """------------------------MAP CREATION IN FUNCTION OF THE LEVEL---------------------------"""

    if level == 1:
        maps = map_data
    elif level == 2:
        maps = map2_data
    else:
        maps = map3_data

    ourWall.empty()
    for row, tiles in enumerate(maps):  # enumerate to get both index and value as row and column
        for col, tile in enumerate(tiles):
            if tile == "1":
                ourWall.add(Walls(col, row, Tile_size))


    if level == 1:
        background_image = pygame.image.load("level1_1024.jpg").convert()
    elif level == 2:
        background_image = pygame.image.load("level2.jpg").convert()
    else:
        background_image = pygame.image.load("level3_begin.jpg").convert()
    displayObj.blit(background_image, [0, 0])

    """------------------------INSTANCES CREATION---------------------------"""
    #·····························HORROCRUXES································
    if first_time == True:
        for i in range(MAX_HORROCRUX):
            ourItems.add(Item(random.randrange(0, WIDTH - Tile_size), random.randrange(0, HEIGHT/4 * 3), "Horrocrux"))
        first_time = False
    else:
        for i in range(horrocrux_killed):
            ourItems.add(Item(random.randrange(0, WIDTH - Tile_size), random.randrange(0, HEIGHT / 4 * 3), "Horrocrux"))
        horrocrux_killed=0

    # ·····························ZOMBIES································
    if random.randrange(0, 100) < frecuency_Zombie:  # here, a probability of "frecuency zombie" is assigned to the appearance of a new zombie
        # if a new zombie instance is created, it is added to the sprite group
        crewZombies.add(Zombie(random.randrange(0, WIDTH - img_width), random.randrange(0, HEIGHT - img_height)))

    # ·····························GUNS································
    if random.randrange(0, 1000) < FRECUENCY_GUN:
        ourItems.add(Item(random.randrange(0, WIDTH - Tile_size), random.randrange(0, HEIGHT-Tile_size), "Shotgun"))

    # ·····························LIVES································
    if random.randrange(0, 1000) < FRECUENCY_LIVES:
        ourItems.add(Item(random.randrange(0, WIDTH - Tile_size), random.randrange(0, HEIGHT - Tile_size), "Hp"))






    """----------------------OBJECTS DISPLAY----------------------------"""

    # ·····························AMMU································
    if shotgun_ammo > 0:  # only display the text on screen when the player is using shotgun
        displayObj.blit(ourHero.ammo_img, (WIDTH - 110, 30))
        
    # ............................LIFEBAR...............................
    displayObj.blit(ourHero.lives_img, (WIDTH - 200, 0))

    # ·····························SCORE································
    score_counter = myfont.render(str(ourHero.score), False, (255, 255, 255))
    displayObj.blit(score_counter, (WIDTH - 170, 30))
    displayObj.blit(ourHero.score_icon, (WIDTH - 200, 30))
    
    # ..........................HORROCRUX......................................
    horrocrux_collected = myfont.render(str(ourHero.horrocrux_collected), False, (255, 255, 255))
    displayObj.blit(horrocrux_collected, (WIDTH - 170, 60))
    displayObj.blit(ourHero.backpack_icon, (WIDTH - 200, 60))

    # ·····························SPRITE GROUPS································
    groupBullets.draw(displayObj)
    ourEffect.draw(displayObj)
    ourItems.draw(displayObj)

    crewZombies.draw(displayObj)
    ourHero.display(displayObj)

    """---------------------------------COLLISIONS : PART 1---------------------------------"""

    hero_zombies_collision = pygame.sprite.spritecollide(ourHero, crewZombies, False)
    hero_wall_collision = pygame.sprite.spritecollide(ourHero, ourWall, False)
    hero_item_collision = pygame.sprite.spritecollide(ourHero, ourItems, False)

    # ·····························ZOMBIE - HERO································
    for zombie in hero_zombies_collision:
        # for each zombie that has taken part in the collision, we check if it's been at least 2 seconds from the last collision that was counted
        lasthit_time += time_passed_s
        if lasthit_time >= 2.0:
            rand_sound = random.randint(0, len(Player_sound) - 1)
            pygame.mixer.Sound.play(Player_sound[rand_sound])
            ourHero.lives -= 1  # here our hero loses one life per zombie in the collisions list
            ourHero.update_livebar(ourHero.lives)
            lasthit_time = 0.0  # set the time from the last collision to hero
            if ourHero.lives == 0:  # If Hero dies show Game Over screen
                if game.show_over_screen(displayObj, ourHero.score) == True:
                    ourHero = Hero()
                    crewZombies.empty()
                    groupBullets.empty()
                    ourItems.empty()
                    ourWall.empty()
                    level = 1
                    vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero
                    horrocrux_killed = 0
                    last_shot = 0
                    shotgun_ammo = 0
                    first_time = True
                    second_time = False

    # ·····························ITEMS - HERO································
    for hit in hero_item_collision:
        if hit.type == "Hp" and ourHero.lives < 5:
            hit.kill()
            ourHero.lives += 1
            ourHero.update_livebar(ourHero.lives)
        elif hit.type == "Shotgun":
            if shotgun_ammo < 6:
                hit.kill()
                pygame.mixer.Sound.play(Gun_pickup)
                weaponType = "Shotgun"
                shotgun_ammo = 6
            ourHero.update_ammo(shotgun_ammo)
            displayObj.blit(ourHero.ammo_img, (WIDTH - 110, 30))
        elif hit.type == "Horrocrux":
            ourHero.horrocrux_collected+=1
            hit.kill()

    # ·····························ITEMS - WALL································
    for wall in ourWall:
        item_wall_collision = pygame.sprite.spritecollide(wall,ourItems,False)
        for item in item_wall_collision:
            if item.type == "Horrocrux":
                horrocrux_killed+=1
            item.kill()

    # ·····························ZOMBIE - BULLETS································
    if len(groupBullets.sprites()) > 0:
        for bul in groupBullets:
            bullet_zombies_collision = pygame.sprite.spritecollide(bul, crewZombies, True)
            bullet_wall_collision = pygame.sprite.spritecollide(bul, ourWall, False)
            # if there is a collision the bullets is also deleted from the group
            if len(bullet_wall_collision) > 0:
                bul.kill()
            if len(bullet_zombies_collision) > 0:
                bul.kill()
                ourEffect.add(zombie_splat(bul.rect))
                ourHero.score += 1

    hero_zombies_collision.clear()

    #sound of the roar of zombies randomize
    if len(crewZombies.sprites()) > 0:
        if random.randrange(0, 1000) < 3:
            pygame.mixer.Sound.play(Zombie_sound[random.randint(0, len(Zombie_sound) - 1)])

    """----------------------EVENTS HANDLING----------------------------"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # ends pygame
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
            # handles if a key is pressed, and moves the hero
            if event.key in (K_LEFT, K_a):
                vel_x = -1.
            if event.key in (K_RIGHT, K_d):
                vel_x = 1.
            if event.key in (K_UP, K_w):
                vel_y = -1.
            if event.key in (K_DOWN, K_s):
                vel_y = 1.
            if event.key == K_n:
                level = 2
            if event.key == K_l:
                level = 3
            if event.key == K_o:
                game_complete = True


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                now = pygame.time.get_ticks()

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
                            ourHero.update_ammo(shotgun_ammo)
                            for x in range(10):
                                groupBullets.add(Shotgun_Bullet(ourHero.rect))
                                print("shotgun")
                                print(shotgun_ammo)
                                pygame.mixer.Sound.play(Shotgun_sound)
                        else:
                            weaponType = "Pistol"

        # once the keys have been read, the method setVel is called to modify the velocity of the hero

    """---------------------------------COLLISIONS : PART 2---------------------------------"""
    # ···································HERO - WALLS································
    for wall in ourWall:
        if ourHero.rect.centerx > wall.rect.centerx - dist_center_xmin and ourHero.rect.centerx < wall.rect.centerx and ourHero.rect.centery <= wall.rect.centery + dist_center_ymin - margin and ourHero.rect.centery >= wall.rect.centery - dist_center_ymin + margin and vel_x > 0:
            vel_x = 0.
            break
        elif ourHero.rect.centerx < wall.rect.centerx + dist_center_xmin and ourHero.rect.centerx > wall.rect.centerx and ourHero.rect.centery <= wall.rect.centery + dist_center_ymin - margin and ourHero.rect.centery >= wall.rect.centery - dist_center_ymin + margin and vel_x < 0:
            vel_x = 0.
            break
        elif ourHero.rect.centery > wall.rect.centery - dist_center_ymin and ourHero.rect.centery < wall.rect.centery and ourHero.rect.centerx > wall.rect.centerx - dist_center_xmin + margin and ourHero.rect.centerx < wall.rect.centerx + dist_center_xmin -margin and vel_y > 0:
            vel_y = 0.
            break
        elif ourHero.rect.centery < wall.rect.centery + dist_center_ymin and ourHero.rect.centery > wall.rect.centery and ourHero.rect.centerx > wall.rect.centerx - dist_center_xmin + margin and ourHero.rect.centerx < wall.rect.centerx + dist_center_xmin - margin and vel_y < 0:
            vel_y = 0.
            break

    """---------------------------------UPDATES---------------------------------"""

    # sets the frames per second to our clock object and store the time passed from the last call in time_passed_ms
    ourHero.setVel(pygame.math.Vector2(vel_x, vel_y))
    time_passed_ms = fpsClock.tick(FPS)

    # converts the time to seconds
    time_passed_s = time_passed_ms / 1000.0
    # call the hero method to update its position, based on the time passed and its velocity

    # the function update of the sprite group basically calls the update function of each sprite of the group
    # so the zombies update method changes its position, based on the position of the hero the time passed
    crewZombies.update(ourHero.rect, time_passed_s)
    groupBullets.update(time_passed_s)
    ourHero.update(time_passed_s)




    if ourHero.horrocrux_collected == MAX_HORROCRUX:
        if ourHero.ifCheckpoint(CHECKPOINT_X_MIN,WIDTH,CHECKPOINT_Y_MIN,CHECKPOINT_Y_MAX):
            if level == 1:
                level = 2
                first_time = True
                #reinitializes the position of the hero and delete the zombies
                ourHero.horrocrux_collected=0
                ourHero.setPos2(48,48)
                crewZombies.empty()
                ourItems.empty()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Level2.mp3")
                pygame.mixer.music.play(0)

            elif level == 2:
                level = 3
                ourHero.setPos2(48, 48)
                crewZombies.empty()
                ourItems.empty()
                ourHero.horrocrux_collected = 0
                first_time = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Level3.mp3")
                pygame.mixer.music.play(0)
        elif level == 3 and ourHero.ifCheckpoint(FINAL_XMIN,FINAL_XMAX,FINAL_YMIN,FINAL_YMAX):
            game_complete = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("GameComplete.mp3")
            pygame.mixer.music.play(0)

    if game_complete == True:
        if game.game_complete_screen(displayObj, ourHero.score) == True:
            ourHero = Hero()
            crewZombies.empty()
            groupBullets.empty()
            ourItems.empty()
            ourWall.empty()
            level = 1
            vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero
            horrocrux_killed = 0
            last_shot = 0
            shotgun_ammo = 0
            first_time = True
            second_time = False
            game_complete = False



    pygame.display.flip()  # DO WE NEED BOTH OS THESE?!!!! update the screen with what we've drawn
    pygame.display.update()  # updates the state of the game



