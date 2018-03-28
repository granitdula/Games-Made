# Pong Advanced. Main Code.
# All Art created by me. Sound effects created by me
# using www.bfxr.net
import pygame as py
import random
from game_modes import *
from os import path

class Game:
    def __init__(self):
        # initialize game window.
        py.init()
        py.mixer.init() #Initialises mixer method so sound can be played.
        self.screen = py.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        py.display.set_caption(CAPTION) #Title that appears on the top of the window
        py.mixer.music.load(path.join(SND_DIR, 'Main_menu_theme.wav'))
        self.clock = py.time.Clock() # Sets clock variable to optimise frame rate.
        self.running = True #Keeps the app running.

    def events(self):
        # Game Loop - Events (key press, mouse clicked etc).
        self.option = 0
        for event in py.event.get():
            # Checks for closing the window.
            if event.type == py.QUIT:
                self.running = False #This is so that both the game and the app stops running.

            self.checkButtonHover()
            # Checks which button has been clicked in main menu and returns
            # appropriate option variable.
            if py.mouse.get_pressed()[0] and self.withinSingleplayer:
                return self.option
            elif py.mouse.get_pressed()[0] and self.withinMultiplayer:
                return self.option
            elif py.mouse.get_pressed()[0] and self.withinChallenge:
                return self.option
            elif py.mouse.get_pressed()[0] and self.withinSettings:
                return self.option

            self.draw_main_menu(self.option)

    def checkButtonHover(self):
        # Checks if mouse is hovering over one of the buttons and highlights
        # that button.
        self.x, self.y = py.mouse.get_pos()
        self.withinSingleplayer = (172 < self.x < 305) and (110 < self.y < 160)
        self.withinMultiplayer = (172 < self.x < 305) and (170 < self.y < 220)
        self.withinChallenge = (172 < self.x < 305) and (230 < self.y < 280)
        self.withinSettings = (172 < self.x < 305) and (290 < self.y < 340)

        if self.withinSingleplayer:
            self.option = 'singleplayer'
        elif self.withinMultiplayer:
            self.option = 'multiplayer'
        elif self.withinChallenge:
            self.option = 'challenge'
        elif self.withinSettings:
            self.option = 'settings'

    def load_menu_image(self, choice):
        self.image = py.image.load(path.join(IMG_DIR, 'Main_menu{}.png'.format(str(choice)))).convert() #loads the image
        self.image_rect = self.image.get_rect() # Gets dimensions of the image
        self.screen.blit(self.image, self.image_rect) # Draws image on screen.

    def draw_main_menu(self, option):
        # Performs the animation of highlighting the button.
        if option == 'singleplayer':
            self.load_menu_image(1)
        elif option == 'multiplayer':
            self.load_menu_image(2)
        elif option == 'challenge':
            self.load_menu_image(3)
        elif option == 'settings':
            self.load_menu_image(4)
        else:
            self.load_menu_image('')

    def main_menu(self):
        # Game's start screen
        self.option = self.events()
        if self.option == 'singleplayer':
            # Runs singleplayer mode if selected.
            self.singleplayer = Singleplayer()
            while self.singleplayer.running:
                # First gets the player to choose a difficulty.
                self.singleplayer.difficultyMenu(game, self.clock)
                if self.singleplayer.windowOpen:
                    self.singleplayer.new(game)
                if self.singleplayer.running:
                    self.singleplayer.show_game_over_screen()

        elif self.option == 'multiplayer':
            # Runs multiplayer if selected.
            self.multiplayer = Multiplayer()
            while self.multiplayer.running:
                self.multiplayer.new(self)
                if self.multiplayer.running:
                    self.multiplayer.show_game_over_screen()

        elif self.option == 'challenge':
            # Runs challenge mode
            self.challenge = Challenge()
            while self.challenge.running:
                self.challenge.new(game)
                if self.challenge.running:
                    self.challenge.show_game_over_screen()

        elif self.option == 'settings':
            self.settings = Settings(game)
            while self.settings.running:
                self.settings.events()

        py.display.flip() # After everything is drawn, the game frame is displayed.
        self.clock.tick(FPS)

    def main_menu_music(self):
        # Loops the background music once it finishes.
        py.mixer.music.play(loops = -1)

game = Game() #Creates the game object.
game.main_menu_music()
while game.running: #Runs the app in a loop
    game.main_menu()

py.quit()
quit()
