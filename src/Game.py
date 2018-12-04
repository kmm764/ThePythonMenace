import pygame, sys, os
from pygame.locals import *




WIDTH = 1024
HEIGHT = 768
img_width = 60
img_height = 60
FPS = 30  # frames per second setting
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
menu_left_margin = 180

#pygame.font.init()
#myfont = pygame.font.SysFont('8-Bit Madness', 50)

class Game:
    max_options = 3
    top_ranking = 3
    
    def __init__(self):
        self.font = pygame.font.SysFont('8-Bit Madness', 50)
        self.font_selected = pygame.font.SysFont('8-Bit Madness', 70)
        self.option = 1
    
    def show_start_screen(self, screen):
        """
            Method that displays the start screen of the game
                :param screen --> Object display where the start screen will be display on
        """
        screen.fill(BLACK)
        #self.text_surface = myfont.render('Our Pygame', False, WHITE)
        img_ini = pygame.image.load("start_screen_game.jpg")
        screen.blit(img_ini, (0, 0))
        #self.draw_text("Our Pygame", 48, WHITE, WIDTH/3, HEIGHT/5, screen, False)
        #self.draw_text("Shoot the zombies and escape", 22, WHITE, WIDTH/5, HEIGHT/5+100, screen, False)
        #self.draw_text("Press a key to play", 22, WHITE, WIDTH/3, HEIGHT/5 + 200, screen, False)
        pygame.display.flip()
        return self.wait_for_key_start()
    
    def show_over_screen(self, screen, score):
        """
                Method that displays the geame over screen of the game and update the ranking
                :param  screen  --> Object display where the start screen will be display on
                        score --> score of the current game to be store
        """
        print("Final score:")
        print(score)
        screen.fill(BLACK)
        self.draw_text("GAME OVER", RED, WIDTH/4, HEIGHT/2, screen, True)
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
        self.draw_text("TUTORIAL", RED, WIDTH / 8, HEIGHT / 5, screen, True)
        img1 = pygame.image.load("arrows2.png")
        img2 = pygame.image.load("arrows.jpg")
        screen.blit(img1, (60, HEIGHT/3))
        screen.blit(img2, (60 + 70, HEIGHT / 3))
        self.draw_text("Arrows - Move the hero", WHITE, WIDTH / 4, HEIGHT / 3, screen, False)
        self.draw_text("Mouse pointer - Rotate the hero", WHITE, WIDTH / 4, HEIGHT / 3 + 100, screen, False)
        self.draw_text("Right mouse click - Shoot", WHITE, WIDTH / 4, HEIGHT / 3 + 200, screen, False)
        self.draw_text("Press <- to go back to the menu", YELLOW, WIDTH / 5, HEIGHT / 3 + 300, screen, False)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # ends pygame
                    os.exit(0)
                    sys.exit()  # ends the program
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        return
                        

    
    def ranking(self,screen):
        screen.fill(BLACK)
        self.draw_text("Ranking", RED, WIDTH / 8, HEIGHT / 5, screen, True)
        self.ranking_draw(screen)
        self.draw_text("Press <- to go back to the menu", YELLOW, WIDTH / 5, HEIGHT / 3 + 300, screen, False)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        return

    def ranking_draw(self,screen):
        try:
            print("Abiertos lectura 1")
            file_scores_r = open("Ranking/scores.txt", 'r')
            file_names_r = open("Ranking/names.txt", 'r')
        except FileNotFoundError:
            self.draw_text("No scores yet", WHITE, WIDTH / 5 * 2, HEIGHT / 3 + 100, screen, True)
            return

        scores = []
        names = []
        k=0
        txt=""

        for lines in file_scores_r.readlines():  # WE STORE THE POINTS
            scores += [lines]

        for lines in file_names_r.readlines():  # WE STORE THE NAMES
            names += [lines]

        # CLEAN THE LISTS
        for i in range(0, len(names)):
            names[i] = names[i][:len(names[i]) - 1]
        print(names)

        for i in range(0, len(scores)):
            scores[i] = int(scores[i][:len(scores[i]) - 1])
        print(scores)
        # close the files
        file_scores_r.close()
        file_names_r.close()
        if len(scores)<=3:
            k=len(scores)
        else:
            k=Game.top_ranking
        for i in range(0,k):
            txt=names[i]+" - "+str(scores[i])
            print(txt)
            print(k)
            self.draw_text(txt, WHITE, WIDTH / 4, HEIGHT / 3 + 100*i, screen, True)
        pygame.display.flip()
        #self.draw_text("Mouse pointer - Rotate the hero", 40, WHITE, WIDTH / 4, HEIGHT / 3 + 100, screen, False)
        #self.draw_text("Right mouse click - Shoot", 40, WHITE, WIDTH / 4, HEIGHT / 3 + 200, screen, False)
    
    def options_draw(self, screen):
        img_menu = pygame.image.load("menu_screen_game.jpg")
        screen.blit(img_menu, (0, 0))
        #self.draw_text("MENU", 100, RED, WIDTH/8, HEIGHT/5, screen,True)
        if self.option==1:
            self.draw_text("PLAY", YELLOW, menu_left_margin, HEIGHT/5*2, screen,True)
            self.draw_text("TUTORIAL", WHITE, menu_left_margin, HEIGHT/5*2 +100, screen,False)
            self.draw_text("RANKING", WHITE, menu_left_margin, HEIGHT/5*2 +200, screen,False)
        elif self.option==2:
            self.draw_text("PLAY", WHITE, menu_left_margin, HEIGHT/5*2, screen,False)
            self.draw_text("TUTORIAL", YELLOW, menu_left_margin, HEIGHT/5*2 +100, screen,True)
            self.draw_text("RANKING", WHITE, menu_left_margin, HEIGHT/5*2 +200, screen,False)
        else:
            self.draw_text("PLAY", WHITE, menu_left_margin, HEIGHT/5*2, screen,False)
            self.draw_text("TUTORIAL", WHITE, menu_left_margin, HEIGHT/5*2 +100, screen,False)
            self.draw_text("RANKING", YELLOW, menu_left_margin, HEIGHT/5*2 +200, screen,True)
        pygame.display.flip()


    def wait_for_key_menu(self, screen):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

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
                        if self.option == 1:
                            return True
                        elif self.option == 2:
                            self.tutorial(screen)
                        else:
                            self.ranking(screen)
                    self.options_draw(screen)
                    
    
    def wait_for_key_start(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return False
                if event.type == pygame.KEYUP:
                    #pygame.event.clear()
                    return True
    
    def draw_text(self, text, color, x, y, screen, selected):
        if selected == True:
            text_surface = self.font_selected.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)
            
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, (x,y))