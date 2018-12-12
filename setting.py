
'''--------Main--------'''

#God mode, to never die:
GOD_MODE =  False

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

#game platform coordinates
MAX_TIME_DISPLAY = 1000
CHECKPOINT_X_MIN = 960
CHECKPOINT_Y_MAX = 256
CHECKPOINT_Y_MIN = 224
FINAL_XMAX = 480
FINAL_XMIN = 416
FINAL_YMAX = 352
FINAL_YMIN = 288

'''Hero'''
Player_sound = ["p0.wav", "p1.wav", "p2.wav", "p3.wav", "p4.wav", "p5.wav", "p6.wav"]
HERO_IMG = "img/Hero/Hero.png"
LIFE_BAR_IMG = ["life_bar_empty.png", "life_bar_1.png", "life_bar_half.png", "life_bar_3.png", "life_bar_full.png"]

#initial settings
INI_HERO_X = 416
INI_HERO_Y = 224
LIVES_INI = 5




'''Zombies'''
ZOMBIE_IMG = 'img/zombies/zombie.png'
FREQUENCY_ZOMBIE = 10
FREQUENCY_ZOMBIE_L2 = 30
FREQUENCY_ZOMBIE_L3 = 16
PROBABILITY_SUPERZOMBIE = 60
Zombie_sound = ["z0.wav", "z1.wav", "z2.wav", "z3.wav", "z4.wav", "z5.wav", "z6.wav", "z7.wav"]



'''guns'''
PISTOL_SOUND = "snd/pistol.wav"
SHOTGUN_SOUND = "snd/shotgun.wav"
GUN_PICKUP_SOUND = "snd/gun_pickup.wav"
BULLETS_IMG = ["bullets_1.png", "bullets_2.png", "bullets_3.png", "bullets_4.png", "bullets_5.png", "bullets_6.png"]
BULLET_IMG = 'img/bullet.png'

'''items'''
FREQUENCY_GUN = 3
FREQUENCY_LIVES = 5
MAX_BACKPACKS = 5
BACKPACK_ICON_IMG = "img/effects/backpack_icon.png"
SCORE_ICON_IMG = "img/effects/score_icon.png"
TILE_IMG = 'img/background/tile.png'
SHOTGUN_IMG = "img/items/shotgun.png"
BACKPACK_IMG = "img/items/backpack.png"
HP_IMG = "img/items/hp.png"

'''effects'''
SPLAT_IMG = 'img/effects/splat.png'
HIT_SCREEN = "img/effects/red_screen.png"
TIME_DISPLAY_SPLASH = 3000
TIME_DISPLAY_RED = 250