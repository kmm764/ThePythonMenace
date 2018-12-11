import pygame


tile_size = 32

shotgun_img = pygame.image.load("img/items/shotgun.png")
backpack_img = pygame.image.load("img/items/backpack.png")
health_img = pygame.image.load("img/items/hp.png")



class Item(pygame.sprite.Sprite):

    health_image = pygame.transform.scale(health_img, (tile_size, tile_size))
    shotgun_image = pygame.transform.scale(shotgun_img, (tile_size, tile_size))
    backpack_image = pygame.transform.scale(backpack_img, (tile_size, tile_size))

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

