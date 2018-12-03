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
YELLOW = (255, 255, 0)

#pygame.font.init()
#myfont = pygame.font.SysFont('8-Bit Madness', 50)

class Game:
    max_options=3
    
    def __init__(self):
        self.font = pygame.font.SysFont('8-Bit Madness', 50)
        self.font_selected = pygame.font.SysFont('8-Bit Madness', 70)
        self.option = 1
    
    def show_start_screen(self, screen):
        screen.fill(BLACK)
        #self.text_surface = myfont.render('Our Pygame', False, WHITE)
        self.draw_text("Our Pygame", 48, WHITE, WIDTH/2, HEIGHT/4, screen, False)
        self.draw_text("Shoot the zombies and escape", 22, WHITE, WIDTH/2, HEIGHT/2, screen, False)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT/3*4, screen, False)
        pygame.display.flip()
        return self.wait_for_key_start()
    
    def show_over_screen(self, screen):
        screen.fill(BLACK)
        self.draw_text("GAME OVER", 22, RED, WIDTH/4, HEIGHT/2, screen, True)
        pygame.display.flip()
        return self.wait_for_key_start()
    
    def menu(self, screen):

        self.wait_for_key_menu(screen)
        if self.option == 1:
            return True
        elif self.option == 2:
            return self.tutorial(screen)
        else:
            return self.ranking(screen)
    
    def tutorial(self, screen):
        screen.fill(BLACK)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        return
                        
            
        pass
    
    def ranking(self,screen):
        screen.fill(BLACK)
        self.menu(screen)
        pass
            
    
    def options_draw(self, screen):
        screen.fill(BLACK)
        self.draw_text("MENU", 100, RED, WIDTH/8, HEIGHT/5, screen,True)
        if self.option==1:
            self.draw_text("PLAY", 40, YELLOW, WIDTH/3*2, HEIGHT/3, screen,True)
            self.draw_text("TUTORIAL", 40, WHITE, WIDTH/3*2, HEIGHT/3 +100, screen,False)
            self.draw_text("RANKING", 40, WHITE, WIDTH/3*2, HEIGHT/3 +200, screen,False)
        elif self.option==2:
            self.draw_text("PLAY", 40, WHITE, WIDTH/3*2, HEIGHT/3, screen,False)
            self.draw_text("TUTORIAL", 40, YELLOW, WIDTH/3*2, HEIGHT/3 +100, screen,True)
            self.draw_text("RANKING", 40, WHITE, WIDTH/3*2, HEIGHT/3 +200, screen,False)
        else:
            self.draw_text("PLAY", 40, WHITE, WIDTH/3*2, HEIGHT/3, screen,False)
            self.draw_text("TUTORIAL", 40, WHITE, WIDTH/3*2, HEIGHT/3 +100, screen,False)
            self.draw_text("RANKING", 40, YELLOW, WIDTH/3*2, HEIGHT/3 +200, screen,True)
        pygame.display.flip()
    
    def wait_for_key_menu(self, screen):
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
                if event.type == pygame.KEYDOWN:
                    if event.key == K_DOWN:
                        if self.option==3:
                            self.option=1
                        else:
                            self.option += 1
                    if event.key == K_UP:
                        if self.option ==1:
                            self.option=Game.max_options
                        else:
                            self.option-=1
                    if event.key == K_RETURN:
                        if self.option == 2:
                            self.tutorial(screen)
                        elif self.option == 1:
                            return True
                    self.options_draw(screen)
                    
    
    def wait_for_key_start(self):
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
    
    def draw_text(self, text, size, color, x, y, screen, selected):
        if selected == True:
            text_surface = self.font_selected.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)
            
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, (x,y))