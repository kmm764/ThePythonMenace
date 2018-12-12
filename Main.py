import pygame, sys
from pygame.locals import *
import random
from setting import *

import os
from os import path


from src.Hero import Hero
from src.Zombie import *
from src.Bullet import *
from src.Game import Game
from src.Walls import Walls
from src.Item import *
from src.Effects import *


"""----------------------PARAMETERS----------------------------"""


#dist_center_xmin = img_width / 2 + Tile_size / 2
#dist_center_ymin = img_height / 2 + Tile_size / 2
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGTH = HEIGHT / TILE_SIZE

LAST_HIT_TIME = 0.5
last_hit_t = LAST_HIT_TIME  #initializes the time variable that we are going to use to limit the collisions between the hero and the zombies
last_attack_time = 0.
frequency_Zombie = FREQUENCY_ZOMBIE



vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero movement intention
zombie_vel = pygame.math.Vector2(0., 0.)
backpack_killed = 0
last_shot = 0
shotgun_ammo = 0
level = 1
weaponType = "Pistol"
first_time = True
second_time = False
final_screen = False
game_complete = False
maps = []
map_data = []
map2_data = []
map3_data = []
play_mode = False
menu_mode = False
new_zombie_delete = False
pause_happened = False
game_folder = path.dirname(__file__)

"""----------------------PYGAME INITIALIZING---------------------------"""
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('8-Bit Madness', 35)

pistol_sound = pygame.mixer.Sound(PISTOL_SOUND)
Shotgun_sound = pygame.mixer.Sound(SHOTGUN_SOUND)
Gun_pickup = pygame.mixer.Sound(GUN_PICKUP_SOUND)


for sounds in range(len(Player_sound)):
    Player_sound[sounds] = pygame.mixer.Sound("snd/Player_Sound/" + Player_sound[sounds])
    Player_sound[sounds].set_volume(2.0)

for z in range(len(Zombie_sound)):
    Zombie_sound[z] = pygame.mixer.Sound("snd/Zombie_Sound/" + Zombie_sound[z])
    Zombie_sound[z].set_volume(2.0)

fpsClock = pygame.time.Clock()

"""----------------------SCREEN OBJECT----------------------------"""

displayObj = pygame.display.set_mode((WIDTH, HEIGHT))  # creates the object that display the screen
pygame.display.set_caption('Game')


"""----------------------GAME OBJECT: display start screen, intro, menu----------------------------"""

game = Game()
game.show_start_screen(displayObj)
game.show_intro(displayObj)
play_mode = game.menu(displayObj)

#initial music
level_1_sound = pygame.mixer.music.load("snd/Level_Sound/Level1.mp3")
pygame.mixer.music.play(2)

#to display the instruccions
game.instructions(displayObj)

"""----------------------INITIAL INSTANCES AND GROUPS CREATION----------------------------"""
our_hero = Hero()

# here we create a sprite group to make easier to manage our zombies instances
crew_zombies = pygame.sprite.Group()
group_bullets = pygame.sprite.Group()
our_wall = pygame.sprite.Group()
our_items = pygame.sprite.Group()
our_effects = pygame.sprite.Group()
# pygame.key.set_repeat(1, 10) #to handle the "holding key" event


"""-----------------------------MAP CREATION----------------------------"""

with open(path.join(game_folder, 'map/FirstMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map_data.append(line)

with open(path.join(game_folder, 'map/SecondMap.txt'), 'rt') as f:  # rf is read
    for line in f:
        map2_data.append(line)

with open(path.join(game_folder, 'map/ThirdMap.txt'), 'rt') as f:  # rf is read
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

    our_wall.empty()
    for row, tiles in enumerate(maps):  # enumerate to get both index and value as row and column
        for col, tile in enumerate(tiles):
            if tile == "1":
                our_wall.add(Walls(col, row, TILE_SIZE))

    if level == 1:
        background_image = pygame.image.load("img/background/level1_1024.jpg").convert()
    elif level == 2:
        background_image = pygame.image.load("img/background/level2.jpg").convert()
    elif final_screen == False:
        background_image = pygame.image.load("img/background/level3_begin.jpg").convert()
    else:
        background_image = pygame.image.load("img/background/level3_final.jpg").convert()

    displayObj.blit(background_image, [0, 0])

    """------------------------------------INSTANCES CREATION------------------------------------"""

    #·········································BACKPACKS·······································
    if first_time == True:
        for i in range(MAX_BACKPACKS):
            our_items.add(Backpack(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT / 4 * 3)))
        first_time = False
    else:
        for i in range(backpack_killed):
            #it keeps creating backpacks if they've been destroyed because of the collisions with the wall
            our_items.add(Backpack(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT / 4 * 3)))
        backpack_killed = 0

    # ···········································ZOMBIES·····································
    if random.randrange(0, 100) < frequency_Zombie:  # here, a probability of "frecuency zombie" is assigned to the appearance of a new zombie
        # if a new zombie instance is created, it has a probability of being a superzombie
        if random.randrange(0, 100) < PROBABILITY_SUPERZOMBIE:
            zombie_new = SuperZombie(random.randrange(0, WIDTH - img_width), random.randrange(0, HEIGHT - img_height))
        else:
            zombie_new = Zombie(random.randrange(0, WIDTH - img_width), random.randrange(0, HEIGHT - img_height))

        newzombie_walls_collision = pygame.sprite.spritecollide(zombie_new, our_wall, False)
        # if the zombie is created over a wall, we delete it. Otherwise is added to the zombies group
        for wall in our_wall:
            if(zombie_new.collision_wall_x(wall.rect.centerx, wall.rect.centery) != "none" or zombie_new.collision_wall_y(wall.rect.centery, wall.rect.centery) != "none") or zombie_new.hero_near(our_hero.rect):
                new_zombie_delete = True
        if len(newzombie_walls_collision)==0 and new_zombie_delete == False:
            crew_zombies.add(zombie_new)

        else:
            new_zombie_delete = False

    # ·····························GUNS································
    if random.randrange(0, 1000) < FREQUENCY_GUN:
        our_items.add(Shotgun(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT - TILE_SIZE)))

    # ·····························LIVES································
    if random.randrange(0, 1000) < FREQUENCY_LIVES:
        our_items.add(Health(random.randrange(0, WIDTH - TILE_SIZE), random.randrange(0, HEIGHT - TILE_SIZE)))

    """--------------------------------OBJECTS DISPLAY---------------------------------"""

    # ·····························AMMU································
    if shotgun_ammo > 0:  # only display the text on screen when the player is using shotgun
        displayObj.blit(our_hero.ammo_img, (WIDTH - 110, 30))
        
    # ............................LIFEBAR...............................
    displayObj.blit(our_hero.lives_img, (WIDTH - 200, 0))

    # ·····························SCORE································
    score_counter = myfont.render(str(our_hero.score), False, (255, 255, 255))
    displayObj.blit(score_counter, (WIDTH - 170, 30))
    displayObj.blit(our_hero.score_icon, (WIDTH - 200, 30))
    
    # ..........................BACKPACKS......................................
    backpack_collected = myfont.render(str(our_hero.backpack_collected), False, (255, 255, 255))
    displayObj.blit(backpack_collected, (WIDTH - 170, 60))
    displayObj.blit(our_hero.backpack_icon, (WIDTH - 200, 60))

    # ·····························SPRITE GROUPS································
    group_bullets.draw(displayObj)
    our_effects.draw(displayObj)
    our_items.draw(displayObj)
    crew_zombies.draw(displayObj)
    our_hero.display(displayObj)
    # ·····························SUPERZOMBIE LIFE BAR································
    for zombie in crew_zombies:
        if type(zombie) == SuperZombie:
            zombie.life_bar_display(displayObj)
    # ·····························HERO DAMAGE································
    if (pygame.time.get_ticks() - last_attack_time) < MAX_TIME_DISPLAY:
        our_hero.under_attack_display(displayObj)

    pygame.display.flip()


    """---------------------------------COLLISIONS : PART 1---------------------------------"""

    hero_zombies_collision = pygame.sprite.spritecollide(our_hero, crew_zombies, False)
    hero_wall_collision = pygame.sprite.spritecollide(our_hero, our_wall, False)
    hero_item_collision = pygame.sprite.spritecollide(our_hero, our_items, False)

    # ···························COLLISIONS: ZOMBIE - HERO································
    for zombie in hero_zombies_collision:
        # for each zombie that has taken part in the collision, we check if it's been at least 0.5 seconds from the last collision that was counted
        last_hit_t += time_passed_s
        if last_hit_t >= LAST_HIT_TIME:
            rand_sound = random.randint(0, len(Player_sound) - 1)
            pygame.mixer.Sound.play(Player_sound[rand_sound])
            our_hero.lives -= 1  # here our hero loses one life per zombie in the collisions list
            last_attack_time = our_hero.get_time_hit()
            our_effects.add(Red_screen())
            our_hero.update_livebar(our_hero.lives)
            last_hit_t = 0.0  # set the time from the last collision to hero
            if our_hero.lives == 0:  # If Hero dies show Game Over screen
                if game.show_over_screen(displayObj, our_hero.score) == True:
                    #here we initializes all the variables, as the user has chosen to play again
                    our_hero = Hero()
                    crew_zombies.empty()
                    group_bullets.empty()
                    our_items.empty()
                    our_wall.empty()
                    level = 1
                    vel_x, vel_y = 0., 0.
                    backpack_killed = 0
                    last_shot = 0
                    shotgun_ammo = 0
                    first_time = True
                    second_time = False
                    frequency_Zombie = FREQUENCY_ZOMBIE

    # ·····························COLLISIONS: ITEMS - HERO································
    for hit in hero_item_collision:
        if type(hit) == Health and our_hero.lives < 5:
            hit.kill()
            our_hero.lives += 1
            our_hero.update_livebar(our_hero.lives)
        elif type(hit) == Shotgun:
            if shotgun_ammo < 6:
                hit.kill()
                pygame.mixer.Sound.play(Gun_pickup)
                weaponType = "Shotgun"
                shotgun_ammo = 6
            our_hero.update_ammo(shotgun_ammo)
            displayObj.blit(our_hero.ammo_img, (WIDTH - 110, 30))
        elif type(hit) == Backpack:
            our_hero.backpack_collected += 1
            hit.kill()

    # ·····························COLLISIONS: ITEMS - WALL································
    #we kill the items that have been created over a wall, and we count the backpacks that have been killed to create then randomly again afterwards
    for wall in our_wall:
        item_wall_collision = pygame.sprite.spritecollide(wall, our_items, False)
        for item in item_wall_collision:
            if type(item) == Backpack:
                backpack_killed += 1
            item.kill()

    # ·····························COLLISIONS: ZOMBIE - BULLETS································
    if len(group_bullets.sprites()) > 0:
        for bul in group_bullets:
            bullet_zombies_collision = pygame.sprite.spritecollide(bul, crew_zombies, False)
            bullet_wall_collision = pygame.sprite.spritecollide(bul, our_wall, False)
            # if there is a collision the bullets is also deleted from the group
            if len(bullet_wall_collision) > 0:
                bul.kill()
            if len(bullet_zombies_collision) > 0:
                bul.kill()
                for z in bullet_zombies_collision:
                    our_effects.add(Splash(bul.rect.x, bul.rect.y))
                    if z.updates_life() is True:
                        our_hero.score += 1

    """-------------------------------ZOMBIES EFFECTS----------------------------"""

    #sound of the roar of zombies randomized
    if len(crew_zombies.sprites()) > 0:
        if random.randrange(0, 1000) < 3:
            pygame.mixer.Sound.play(Zombie_sound[random.randint(0, len(Zombie_sound) - 1)])

    """------------------------------EVENTS HANDLING--------------------------------"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # ends pygame
            os._exit(0)
            sys.exit()  # ends the program
        # ····························· HERO MOVEMENT································
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

        # ····························· PAUSE SCREEN································
            if event.key == K_p:
                time_pause_start = pygame.time.get_ticks()
                pygame.mixer.music.pause()
                game.pause_screen(displayObj)
                pause_happened=True
                total_time_paused = pygame.time.get_ticks() - time_pause_start #we store the time of the pause
                pygame.mixer.music.unpause()
        # ····························· SHOOTING································
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                now = pygame.time.get_ticks()
                if weaponType == "Pistol":
                    Bullet_Rate = 350
                    if now - last_shot > Bullet_Rate:
                        last_shot = now
                        group_bullets.add(Pistol_bullet(our_hero.rect))
                        pygame.mixer.Sound.play(pistol_sound)

                elif weaponType == "Shotgun":
                    Bullet_Rate = 1200
                    if now - last_shot > Bullet_Rate:
                        last_shot = now
                        if shotgun_ammo > 0:
                            shotgun_ammo -= 1
                            for x in range(10):
                                group_bullets.add(Shotgun_Bullet(our_hero.rect))
                                pygame.mixer.Sound.play(Shotgun_sound)
                            our_hero.update_ammo(shotgun_ammo)
                        else:
                            weaponType = "Pistol"

    """---------------------------------COLLISIONS : PART 2---------------------------------"""
    # ···································COLLISIONS: HERO - WALLS································
    #we check the type of the collision and we evaluate if the intention of the movement is allowed or not
    for wall in our_wall:
        colx = our_hero.collision_wall_x(wall.rect.centerx, wall.rect.centery)
        coly = our_hero.collision_wall_y(wall.rect.centerx, wall.rect.centery)
        if colx == "left" and vel_x > 0:
            vel_x = 0.
        elif colx == "right" and vel_x < 0:
            vel_x = 0.
        if coly == "top" and vel_y > 0:
            vel_y = 0.
        elif coly == "bottom" and vel_y < 0:
            vel_y = 0.
    # ···································COLLISIONS: ZOMBIES - WALLS································
    for zombie in crew_zombies:
        zombie_vel = zombie.trajectory_intention(our_hero.rect)
        for wall in our_wall:
            colx_zombie = zombie.collision_wall_x(wall.rect.centerx, wall.rect.centery)
            if colx_zombie == "left" and zombie_vel.x > 0:
                zombie_vel.x = 0.
            elif colx_zombie == "right" and zombie_vel.x < 0:
                zombie_vel.x = 0.
        for wall in our_wall:
            coly_zombie = zombie.collision_wall_y(wall.rect.centerx, wall.rect.centery)
            if coly_zombie == "top" and zombie_vel.y > 0:
                zombie_vel.y = 0.
            elif coly_zombie == "bottom" and zombie_vel.y < 0:
                zombie_vel.y = 0.
        zombie.set_vel(zombie_vel) #we set the new velocity of the zombie


    """-------------------------------------UPDATES-------------------------------------"""

    our_hero.set_vel(pygame.math.Vector2(vel_x, vel_y)) # we set the new velocity of the hero

    # sets the frames per second to our clock object and store the time passed from the last call in time_passed_ms
    time_passed_ms = fpsClock.tick(FPS)
    if pause_happened:
        time_passed_s = (time_passed_ms - total_time_paused)/1000 #if paused was pressed, we substract the time of the pause to the time passed
        pause_happened = False
    else:
        time_passed_s = time_passed_ms / 1000.0

    # the function update of the sprite group basically calls the update function of each sprite of the group
    crew_zombies.update(our_hero.rect, time_passed_s)
    group_bullets.update(time_passed_s)
    our_hero.update(time_passed_s)
    our_effects.update()

    """-----------------CHECK CONDITIONS TO GO TO THE NEXT LEVEL OR COMPLETE THE GAME-------------------------------"""

    if our_hero.backpack_collected >= MAX_BACKPACKS:
        if our_hero.if_checkpoint(CHECKPOINT_X_MIN, WIDTH, CHECKPOINT_Y_MIN, CHECKPOINT_Y_MAX):
            if level == 1:
                #here we set the settings to level 2
                level = 2
                first_time = True
                our_hero.backpack_collected=0
                our_hero.set_pos2(48, 48)
                frequency_Zombie *=4
                crew_zombies.empty()
                our_items.empty()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("snd/Level_Sound/Level2.mp3")
                pygame.mixer.music.play(2)

            elif level == 2:
                # here we set the settings to the first screen of level 3
                level = 3
                frequency_Zombie /=4
                our_hero.set_pos2(48, 48)
                crew_zombies.empty()
                our_items.empty()
                our_hero.backpack_collected = 0
                first_time = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("snd/Level_Sound/Level3.mp3")
                pygame.mixer.music.play(2)
            elif final_screen == True:
                # here we set the settings to the last screen of level 3
                game_complete = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("snd/Level_Sound/GameComplete.mp3")
                pygame.mixer.music.play(2)

        elif level == 3 and our_hero.if_checkpoint(FINAL_XMIN, FINAL_XMAX, FINAL_YMIN, FINAL_YMAX):
            final_screen = True

    if game_complete == True:
        if game.game_complete_screen(displayObj, our_hero.score) == True:
            our_hero = Hero()
            crew_zombies.empty()
            group_bullets.empty()
            our_items.empty()
            our_wall.empty()
            level = 1
            vel_x, vel_y = 0., 0.  # inicializes the x and y components of the velocity vector of the hero
            backpack_killed = 0
            last_shot = 0
            shotgun_ammo = 0
            first_time = True
            second_time = False
            final_screen = False
            game_complete = False
            frequency_Zombie = FREQUENCY_ZOMBIE




