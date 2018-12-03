import pygame, sys, os
from pygame.locals import *




WIDTH = 1000
HEIGHT = 600
img_width = 60
img_height = 60
FPS = 30  # frames per second setting
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#pygame.font.init()
#myfont = pygame.font.SysFont('8-Bit Madness', 50)

class Game:
    
    def __init__(self, myfont):
        self.font = myfont
    
    def show_start_screen(self, screen):
        screen.fill(BLACK)
        #self.text_surface = myfont.render('Our Pygame', False, WHITE)
        self.draw_text("Our Pygame", 48, WHITE, WIDTH/2, HEIGHT/4, screen)
        self.draw_text("Shoot the zombies and escape", 22, WHITE, WIDTH/2, HEIGHT/2, screen)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT/3*4, screen)
        pygame.display.flip()
        return self.wait_for_key()
    
    def show_over_screen(self, screen):
        self.screen = screen
        self.screen.fill(BLACK)
        pygame.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        global play_mode
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit() # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return False
                if event.type == pygame.KEYUP:
                    waiting = False
                    return True
    
    def draw_text(self, text, size, color, x, y, screen):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, (x,y))