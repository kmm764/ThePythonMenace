import pygame
from setting import *

shotgun_img = pygame.image.load(SHOTGUN_IMG)
backpack_img = pygame.image.load(BACKPACK_IMG)
health_img = pygame.image.load(HP_IMG)



class Item(pygame.sprite.Sprite):

    health_image = pygame.transform.scale(health_img, (TILE_SIZE, TILE_SIZE))
    shotgun_image = pygame.transform.scale(shotgun_img, (TILE_SIZE, TILE_SIZE))
    backpack_image = pygame.transform.scale(backpack_img, (TILE_SIZE, TILE_SIZE))

    def __init__(self, x, y):

        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Health(Item):
    def __init__(self, x, y):
        self.image = Item.health_image
        super().__init__(x, y)


class Shotgun(Item):
    def __init__(self, x, y):
        self.image = Item.shotgun_image
        super().__init__(x, y)


class Backpack(Item):
    def __init__(self, x, y):
        self.image = Item.backpack_image
        super().__init__(x, y)

