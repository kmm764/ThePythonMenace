import pygame, sys, os
from pygame.locals import *
from setting import *



menu_left_margin = 180
INTRO_X_INI=50
INTRO_Y_INI=50
TIME_TYPING = 100
EXTRA_SCORE = 100

#pygame.font.init()
#myfont = pygame.font.SysFont('8-Bit Madness', 50)

class Game:
    max_options = 3
    top_ranking = 3
    
    def __init__(self):
        self.font = pygame.font.SysFont('8-Bit Madness', 50)
        self.font_selected = pygame.font.SysFont('8-Bit Madness', 70)
        self.font_ending = pygame.font.SysFont('8-Bit Madness', 135)
        self.option = 1
    
    def show_start_screen(self, screen):
        """
            Method that displays the start screen of the game
                :param screen --> Object display where the start screen will be displayed on
        """
        screen.fill(BLACK)
        img_ini = pygame.image.load("img/Menu/start_screen_game.jpg")
        screen.blit(img_ini, (0, 0))
        pygame.display.flip()
        while True:
            if self.wait_for_anykey():
                return


    def show_intro(self, screen):
        """
            Method that displays the intro of the game
                :param screen --> Object display where the intro will be displayed on
        """
        nextline = 50
        screen.fill(BLACK)
        txt = ""
        intro = ["Moodle Programming announcements"," Thursday, 20 December 2018, 13:59PM:","","Alert to all the students. Demonstration","cancelled. Waves of zombies are invading"," the Earth. If somebody is reading this,","please, save us all.","Letting us die would be even worse than","repeating code.","Best regards.","Isaac and Thorsten"]
        pygame.mixer.music.load("snd/intro/keyboard.wav")
        pygame.mixer.music.play(4)
        lines = 0
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
                        pygame.time.delay(TIME_TYPING)
                        txt = txt[:-1]
                        screen.fill(BLACK)
                        for j in range(0, lines):
                            self.draw_text(intro[j], WHITE, INTRO_X_INI, INTRO_Y_INI + nextline * j, screen, False)
                        self.draw_text(txt, WHITE, INTRO_X_INI, currentline, screen, False)
                        pygame.display.flip()
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
            lines += 1
            currentline = INTRO_Y_INI+nextline*lines
            txt = ""
        pygame.mixer.music.stop()
        return

    def wait_for_anykey(self):
        """
            Method that waits for any key to be pressed
        :return: False if "quit" is pressed and True if any other key is pressed
        """
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
        """
            Method that displays the menu
        :param screen: Object display where the menu will be displayed on
        :return: True if the option "Play" is selected.
        """
        self.options_draw(screen)
        self.wait_for_key_menu(screen)
        if self.option == 1:
            return True
        elif self.option == 2:
            return self.tutorial(screen)
        else:
            return self.ranking(screen)

    def wait_for_key_menu(self, screen):
        """
            Method that reads the keys pressed by the user to move through the options in the menu
        :param screen: Object display where the options will be displayed on
        """
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
                            return
                        elif self.option == 2:
                            self.tutorial(screen)
                        else:
                            self.ranking(screen)
                    self.options_draw(screen)

    def options_draw(self, screen):
        img_menu = pygame.image.load("img/Menu/menu_screen_game.jpg")
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
        """
            Method that display the 3 screens of instructions, for 10 seconds each, and allow the user to skip each one of
            them pressing any key
        :param screen: Object display where the instructions will be displayed on
        :return:
        """
        img_instructions = pygame.image.load("img/Menu/intro/intro_lifebar_score.jpg")
        screen.blit(img_instructions, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500) #this if to avoid that the function watchdog reads inmediately the previous event and skip it directly
        #the total time we show the screen is 10s, but every second we check if the user wants to skip it
        self.watchdog()
        img_instructions = pygame.image.load("img/Menu/intro/intro_hero_platform.jpg")
        screen.blit(img_instructions, (0, 0))
        pygame.display.flip()
        self.watchdog()
        img_instructions = pygame.image.load("img/Menu/intro/intro_shotgun.jpg")
        screen.blit(img_instructions, (0, 0))
        pygame.display.flip()
        self.watchdog()

    def watchdog(self):
        """
            Method that returns if no key is pressed in 10 seconds
        """
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
                :param screen --> Object display where the game complete screen will be displayed on
        """
        screen.fill(BLACK)
        score += EXTRA_SCORE  # 100 extra score when finished the game
        img_ini = pygame.image.load("img/Menu/end/end_win_screen.jpg")
        screen.blit(img_ini, (0, 0))
        self.draw_text(str(score), WHITE, WIDTH / 2, HEIGHT / 2 -147, screen, "end")
        #screen.blit(score, (WIDTH/2, HEIGHT/2))
        pygame.display.flip()
        choice = self.wait_for_key_over()
        if choice == "save":
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
        elif choice == "continue":
            return True
    
    def show_over_screen(self, screen, score):
        """
                Method that displays the geame over screen of the game and update the ranking
                :param  screen  --> Object display where the game over will be displayed on
                        score --> score of the current game to be store
        """
        screen.fill(BLACK)
        img_ini = pygame.image.load("img/Menu/end/end_game_over.jpg")
        screen.blit(img_ini, (0, 0))
        #self.draw_text("GAME OVER", RED, 40, HEIGHT/2, screen, True)
        #self.draw_text("press S to save your score", RED, 40, HEIGHT / 2 + 100, screen, True)
        pygame.display.flip()
        choice = self.wait_for_key_over()
        if choice == "save":
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
        elif choice == "continue":
            return True


    def wait_for_key_over(self):
        """
            Method that waits for the user to press "c" to continue or "s" to save the score when they finish the game
        :return: False if the user press quit, "save" if the user press 's', "continue" is the user press 'c'
        """
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
        """
            Methods that waits for the user to input their name, while it displays the inputs. It stops when
            the user press Enter.
        :param screen: Object display where the input name screen will be displayed on
        :return: a string with the name the user has input
        """
        screen.fill(BLACK)
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

    def pause_screen(self, screen):
        """
            Method that displays the pause screen and waits for the user to press p to restart the game
        :param screen: Object display where the pause screen will be displayed on
        :return:
        """
        tutorial_img = pygame.image.load("img/Menu/pause_screen.png")
        tutorial_img_scale = pygame.transform.scale(tutorial_img, (WIDTH, HEIGHT))
        screen.blit(tutorial_img_scale, (0, 0))
        pygame.display.flip()
        self.waiting_for(K_p)

    def tutorial(self, screen):
        """
            Method that displays the tutorial screen and waits for the user to press left arrow to go back to the menu
        :param screen: Object display where the tutorial will be displayed on
        :return:
        """
        tutorial_img = pygame.image.load("img/Menu/tutorial_screen.jpg")
        tutorial_img_scale=pygame.transform.scale(tutorial_img, (WIDTH, HEIGHT))
        screen.blit(tutorial_img_scale, (0, 0))
        pygame.display.flip()
        self.waiting_for(K_LEFT)

    def ranking(self,screen):
        """
            Method that displays the background of the ranking, draw it, and wait for the user to press left arrow
            to go back to the menu
        :param screen: Object display where the ranking screen will be displayed on
        """
        tutorial_img = pygame.image.load("img/Menu/ranking_screen.jpg")
        tutorial_img_scale = pygame.transform.scale(tutorial_img, (WIDTH, HEIGHT))
        screen.blit(tutorial_img_scale, (0, 0))
        self.ranking_draw(screen)
        pygame.display.flip()
        self.waiting_for(K_LEFT)

    def waiting_for(self, key):
        """
            Method that waits for the user to press a given key
            :param key: key awaited
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # ends pygame
                    os._exit(0)
                    sys.exit()  # ends the program
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == key:
                        return

    def ranking_draw(self, screen):
        """
            Method that read the files of the names and scores and display the 3 firsts (or less names if there
            are less than 3 names)
        :param screen: Object display where the ranking will be displayed on
        :return:
        """
        try:
            file_scores_r = open("Ranking/scores.txt", 'r')
            file_names_r = open("Ranking/names.txt", 'r')
        except FileNotFoundError:
            self.draw_text("No scores yet", WHITE, WIDTH / 5 * 2, HEIGHT / 3 + 100, screen, True)
            return

        scores = []
        names = []
        k = 0
        txt = ""

        for lines in file_scores_r.readlines():  # WE STORE THE POINTS
            scores += [lines]

        for lines in file_names_r.readlines():  # WE STORE THE NAMES
            names += [lines]

        # CLEAN THE LISTS
        for i in range(0, len(names)):
            names[i] = names[i][:len(names[i]) - 1]

        for i in range(0, len(scores)):
            scores[i] = int(scores[i][:len(scores[i]) - 1])
        # close the files
        file_scores_r.close()
        file_names_r.close()
        if len(scores) <= 3:
            k = len(scores)
        else:
            k = Game.top_ranking
        for i in range(0, k):
            txt=names[i]+" - "+str(scores[i])
            self.draw_text(txt, WHITE, WIDTH / 4, HEIGHT / 3 + 100*i, screen, True)
        pygame.display.flip()


    def draw_text(self, text, color, x, y, screen, selected):
        """
            Method that displays text
        :param text: text to be drawn
        :param color: color of the text
        :param x: x coordinate when the position of the text starts
        :param y: y coordinate when the position of the text starts
        :param screen: Object display where the text will be displayed on
        :param selected: value that indicates the font object to be used
        :return:
        """
        if selected is True:
            text_surface = self.font_selected.render(text, True, color)
        elif selected is False:
            text_surface = self.font.render(text, True, color)
        elif selected == "end":
            text_surface = self.font_ending.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, (x,y))


def ranking_update(newscore, newname):
    """
        This function saves the name and the score in two files "names" and "scores", and order the lines from higher to lower score
    :param newscore: score obtained in the last game
    :param newname: name introduced by the user
    """
    # if the files do not exist we create them and write on the the name and score directly
    try:
        file_scores_r = open("Ranking/scores.txt", 'r')
        file_names_r = open("Ranking/names.txt", 'r')
    except FileNotFoundError:
        file_scores_w = open("Ranking/scores.txt", 'a+')
        file_names_w = open("Ranking/names.txt", 'a+')
        file_scores_w.write(str(newscore) + "\n")
        file_names_w.write(newname + "\n")
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
        if newscore > scores[i]:
            # we make sure we only fix the position of the new score once
            if newscore_pos == -1:
                newscore_pos = i
            newindex += [i + 1]  # new scorw position
        else:
            newindex += [i]  # new order for the current data in the file
    file_scores_r.close()
    file_names_r.close()
    newscores = [0] * (len(scores) + 1)
    newnames = [0] * (len(scores) + 1)
    if newscore_pos != -1:
        # we reorder the names and the scores
        newscores[newscore_pos] = str(newscore) + "\n"
        newnames[newscore_pos] = newname + "\n"
        for i in range(0, len(scores)):
            newscores[newindex[i]] = str(scores[i]) + "\n"
            newnames[newindex[i]] = names[i] + "\n"

        # we open the files to overwrite the content in mode "w"
        file_scores_w = open("Ranking/scores.txt", 'w')
        file_names_w = open("Ranking/names.txt", 'w')
        file_scores_w.writelines(newscores)
        file_names_w.writelines(newnames)
        file_scores_w.close()
        file_names_w.close()
    else:
        if len(scores) < 3:
            file_scores_w = open("Ranking/scores.txt", 'a+')
            file_names_w = open("Ranking/names.txt", 'a+')
            file_scores_w.write(str(newscore) + "\n")
            file_names_w.write(newname + "\n")
            file_scores_w.close()
            file_names_w.close()