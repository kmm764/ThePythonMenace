import pygame

tile_size = 32
splash_img = pygame.image.load('splat.png')
TIME_DISPLAY_SPLASH = 3000
TIME_DISPLAY_RED = 250


class Effects(pygame.sprite.Sprite):
    splash_image = pygame.transform.scale(splash_img, (tile_size, tile_size))
    hit_screen = pygame.image.load("red_screen.png")

    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        if (pygame.time.get_ticks() - self.creation_time) > self.life_time:
            self.kill()


class Splash(Effects):
    def __init__(self, x, y):
        self.image = Effects.splash_image
        super().__init__(x, y)
        self.life_time = TIME_DISPLAY_SPLASH


class Red_screen(Effects):
    def __init__(self):
        self.image = Effects.hit_screen
        super().__init__(0, 0)
        self.life_time = TIME_DISPLAY_RED
