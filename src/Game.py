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
INTRO_X_INI=50
INTRO_Y_INI=50
TIME_TYPING = 100

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
        img_ini = pygame.image.load("start_screen_game.jpg")
        screen.blit(img_ini, (0, 0))
        pygame.display.flip()
        while True:
            if self.wait_for_anykey():
                return


    def show_intro(self, screen):
        """
            Method that displays the intro of the game
                :param screen --> Object display where the start screen will be display on
        """
        nextline=50
        screen.fill(BLACK)
        txt=""
        intro = ["Moodle Programming announcements:"," Thursday, 20 December 2018, 13:59PM:","","Alert to all the students. Demonstration","cancelled. Waves of zombies are invading"," the Earth. If somebody is reading this,","please, save us all.","Letting us die would be even worse than","repeating code.","Best regards.","Isaac and Thorsten"]
        pygame.mixer.music.load("keyboard.wav")
        pygame.mixer.music.play(4)
        lines=0
        currentline = INTRO_Y_INI
        pygame.event.clear()
        for line in intro:
            for letter in line:
                if letter == ".":
                    pygame.mixer.music.stop()
                    for k in range(3):
                        txt += "_"
                        self.draw_text(txt, WHITE, INTRO_X_INI, currentline, screen, False)
                        pygame.display.flip()
                        print(txt)
                        pygame.time.delay(TIME_TYPING)
                        txt = txt[:-1]
                        screen.fill(BLACK)
                        for j in range(0, lines):
                            self.draw_text(intro[j], WHITE, INTRO_X_INI, INTRO_Y_INI + nextline * j, screen, False)
                        self.draw_text(txt, WHITE, INTRO_X_INI, currentline, screen, False)
                        pygame.display.flip()
                        print(txt)
                        pygame.time.delay(TIME_TYPING)
                    txt += "."
                    self.draw_text(txt, WHITE, INTRO_X_INI, currentline, screen, False)
                    pygame.display.flip()
                    pygame.time.delay(TIME_TYPING)
                    pygame.mixer.music.play(4)
                else:
                    txt += letter
                    for j in range(0,lines):
                        self.draw_text(intro[j], WHITE, INTRO_X_INI, INTRO_Y_INI+nextline*j, screen, False)
                    self.draw_text(txt, WHITE, INTRO_X_INI,currentline, screen, False)
                    pygame.display.flip()
                    pygame.time.delay(TIME_TYPING)
                if self.wait_for_anykey()==True:
                    pygame.mixer.music.stop()
                    return
            lines+=1
            currentline=INTRO_Y_INI+nextline*lines
            txt=""
        pygame.mixer.music.stop()
        return

    def wait_for_anykey(self):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return False
                if event.type == pygame.KEYUP:
                    pygame.event.clear()
                    return True


    def menu(self, screen):
        self.options_draw(screen)
        self.wait_for_key_menu(screen)
        if self.option == 1:
            return True
        elif self.option == 2:
            return self.tutorial(screen)
        else:
            return self.ranking(screen)

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
    def options_draw(self, screen):
        img_menu = pygame.image.load("menu_screen_game.jpg")
        screen.blit(img_menu, (0, 0))
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

    def instructions(self, screen):
        img_instructions = pygame.image.load("lifebar_score.jpg")
        screen.blit(img_instructions, (0, 0))
        pygame.display.flip()
        pygame.event.clear()
        #the total time we show the screen is 10s, but every second we check if the user wants to skip it
        self.watchdog()
        img_instructions = pygame.image.load("hero_platform.jpg")
        screen.blit(img_instructions, (0, 0))
        pygame.display.flip()
        self.watchdog()
        img_instructions = pygame.image.load("shotgun.jpg")
        screen.blit(img_instructions, (0, 0))
        pygame.display.flip()
        self.watchdog()

    def watchdog(self):
        now = pygame.time.get_ticks()
        pygame.event.clear()
        while True:
            # if it detect any key or the time run 10 seconds it returns
            if self.wait_for_anykey()==True:
                return
            elif (pygame.time.get_ticks() - now > 10000):
                return





    def game_complete_screen(self, screen, score):
        """
            Method that displays the start screen of the game
                :param screen --> Object display where the start screen will be display on
        """
        screen.fill(BLACK)
        img_ini = pygame.image.load("game_complete_screen.png")
        screen.blit(img_ini, (0, 0))
        pygame.display.flip()
        if self.wait_for_key_over()== "save":
            name = self.input_name_screen(screen)
            ranking_update(score,name)
            screen.fill(BLACK)
            self.draw_text("Ranking", RED, WIDTH / 8, HEIGHT / 5, screen, True)
            self.ranking_draw(screen)
            self.draw_text("Press C to play again", YELLOW, WIDTH / 5, HEIGHT / 3 + 300, screen, False)
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # ends pygame
                        os._exit(0)
                        sys.exit()  # ends the program
                        return False
                    if event.type == pygame.KEYUP:
                        if event.key == K_c:
                            return True
        elif self.wait_for_key_over() == "continue":
            return True
    
    def show_over_screen(self, screen, score):
        """
                Method that displays the geame over screen of the game and update the ranking
                :param  screen  --> Object display where the start screen will be display on
                        score --> score of the current game to be store
        """
        screen.fill(BLACK)
        img_ini = pygame.image.load("game_over_screen.jpg")
        screen.blit(img_ini, (0, 0))
        #self.draw_text("GAME OVER", RED, 40, HEIGHT/2, screen, True)
        #self.draw_text("press S to save your score", RED, 40, HEIGHT / 2 + 100, screen, True)
        pygame.display.flip()
        if self.wait_for_key_over()== "save":
            name = self.input_name_screen(screen)
            ranking_update(score,name)
            screen.fill(BLACK)
            self.draw_text("Ranking", RED, WIDTH / 8, HEIGHT / 5, screen, True)
            self.ranking_draw(screen)
            self.draw_text("Press C to play again", YELLOW, WIDTH / 5, HEIGHT / 3 + 300, screen, False)
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # ends pygame
                        os._exit(0)
                        sys.exit()  # ends the program
                        return False
                    if event.type == pygame.KEYUP:
                        if event.key == K_c:
                            return True
        elif self.wait_for_key_over() == "continue":
            return True


    def wait_for_key_over(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return False
                if event.type == pygame.KEYUP:
                    if event.key == K_s:
                        return "save"
                    if event.key == K_c:
                        return "continue"

    def input_name_screen(self, screen):
        screen.fill(BLACK)
        print("name")
        name_input = ""
        while True:
            self.draw_text("Input your name and press enter", RED, 40, HEIGHT / 6, screen, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return name_input
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                        screen.fill(BLACK)
                    else:
                        name_input += event.unicode
                        screen.fill(BLACK)
            self.draw_text(name_input, WHITE, WIDTH / 5 * 2, HEIGHT / 3, screen, False)
            pygame.display.flip()
    

    def tutorial(self, screen):
        screen.fill(BLACK)
        self.draw_text("TUTORIAL", RED, WIDTH / 8, HEIGHT / 5, screen, True)
        img1 = pygame.image.load("arrows2.png")
        img2 = pygame.image.load("arrows.jpg")
        screen.blit(img1, (60, HEIGHT/3))
        screen.blit(img2, (60 + 70, HEIGHT / 3))
        self.draw_text("Arrows - Move the hero", WHITE, WIDTH / 4, HEIGHT / 3, screen, False)
        self.draw_text("Mouse pointer - Rotate the hero", WHITE, WIDTH / 4, HEIGHT / 3 + 100, screen, False)
        self.draw_text("Left mouse click - Shoot", WHITE, WIDTH / 4, HEIGHT / 3 + 200, screen, False)
        self.draw_text("Press <- to go back to the menu", YELLOW, WIDTH / 5, HEIGHT / 3 + 300, screen, False)
        pygame.display.flip()
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
            k = len(scores)
        else:
            k = Game.top_ranking
        for i in range(0,k):
            txt=names[i]+" - "+str(scores[i])
            print(txt)
            print(k)
            self.draw_text(txt, WHITE, WIDTH / 4, HEIGHT / 3 + 100*i, screen, True)
        pygame.display.flip()


    
    def draw_text(self, text, color, x, y, screen, selected):
        if selected == True:
            text_surface = self.font_selected.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)
            
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, (x,y))


def ranking_update(newscore, newname):
    """
        This function save the name and the score in two files "names" and "scores", and order the lines from higher to lower score
    :param newscore: score obtained in the last game
    :param newname: name introduced by the user
    """
    # if the files do not exist we create them and write on the the name and score directly
    try:
        print("Abiertos lectura 1")
        file_scores_r = open("Ranking/scores.txt", 'r')
        file_names_r = open("Ranking/names.txt", 'r')
    except FileNotFoundError:
        print("Abiertos escritura 1")
        file_scores_w = open("Ranking/scores.txt", 'a+')
        file_names_w = open("Ranking/names.txt", 'a+')
        file_scores_w.write(str(newscore) + "\n")
        file_names_w.write(newname + "\n")
        print("Cerrados escritura 1")
        file_scores_w.close()
        file_names_w.close()
        return

    scores = []
    names = []
    newindex = []
    i = 0
    newscore_pos = -1
    for lines in file_scores_r.readlines():  # WE STORE THE POINTS
        scores += [lines]
    for lines in file_names_r.readlines():  # WE STORE THE NAMES
        names += [lines]
    # CLEAN THE LISTS
    for i in range(0, len(names)):
        names[i] = names[i][:len(names[i]) - 1]

    for i in range(0, len(scores)):
        scores[i] = int(scores[i][:len(scores[i]) - 1])
        print(scores[i])
        if newscore > scores[i]:
            print(i)
            print(newscore_pos)
            # we make sure we only fix the position of the new score once
            if newscore_pos == -1:
                newscore_pos = i
            newindex += [i + 1]  # new scorw position
        else:
            newindex += [i]  # new order for the current data in the file
    print("Cerrados lectura 3")
    file_scores_r.close()
    file_names_r.close()
    newscores = [0] * (len(scores) + 1)
    newnames = [0] * (len(scores) + 1)
    print(newscore)
    print(newscore_pos)
    if newscore_pos != -1:
        # we reorder the names and the scores
        newscores[newscore_pos] = str(newscore) + "\n"
        newnames[newscore_pos] = newname + "\n"
        for i in range(0, len(scores)):
            newscores[newindex[i]] = str(scores[i]) + "\n"
            newnames[newindex[i]] = names[i] + "\n"

        # we open the files to overwrite the content in mode "w"
        print("Abiertos escritura 3")
        file_scores_w = open("Ranking/scores.txt", 'w')
        file_names_w = open("Ranking/names.txt", 'w')
        file_scores_w.writelines(newscores)
        file_names_w.writelines(newnames)
        print("Cerrados escritura 3")
        file_scores_w.close()
        file_names_w.close()
    else:
        if len(scores) < 3:
            file_scores_w = open("Ranking/scores.txt", 'a+')
            file_names_w = open("Ranking/names.txt", 'a+')
            print("Abiertos escritura 2")
            file_scores_w.write(str(newscore) + "\n")
            file_names_w.write(newname + "\n")
            print("Cerrados escritura 2")
            file_scores_w.close()
            file_names_w.close()