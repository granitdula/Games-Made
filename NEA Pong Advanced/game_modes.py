import pygame as py
import random
from settings import *
from sprites import *
from os import path

class GameModes(object):
    # This is a parent class for the Singleplayer, Multiplayer and Challenge classes.
    def __init__(self):
        self.screen = py.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Creates window
        self.score_font_name = py.font.match_font('verdana')
        self.ball_off_wall_sound = py.mixer.Sound(path.join(SND_DIR, 'ball_off_walls.wav'))
        self.missile_collision_sound = py.mixer.Sound(path.join(SND_DIR, 'missile_collision.wav'))
        self.missile_launch_sound = py.mixer.Sound(path.join(SND_DIR, 'missile_launch.wav'))
        self.ball_off_paddle_sound = py.mixer.Sound(path.join(SND_DIR, 'ball_off_paddle.wav'))
        self.length_up_sound = py.mixer.Sound(path.join(SND_DIR, 'length_up.wav'))
        self.length_down_sound = py.mixer.Sound(path.join(SND_DIR, 'length_down.wav'))
        self.speed_down_sound = py.mixer.Sound(path.join(SND_DIR, 'speed_down.wav'))
        self.ball_direct_sound = py.mixer.Sound(path.join(SND_DIR, 'ball_direct.wav'))
        self.barrier_power_up_sound = py.mixer.Sound(path.join(SND_DIR, 'barrier_power_up.wav'))
        self.gained_point_sound = py.mixer.Sound(path.join(SND_DIR, 'gained_point_sound.wav'))
        self.game_finished_sound = py.mixer.Sound(path.join(SND_DIR, 'game_finished_sound.wav'))
        self.clock = py.time.Clock() # Sets clock variable to optimise frame rate.
        self.running = True # Keeps the app running.

    def run(self):
        # Game loop.
        self.playing = True # Keeps the game mode playing until the game is over.
        while self.playing:
            self.clock.tick(FPS) # Gives the game a frame rate.
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - Events
        for event in py.event.get():
            # Checks for closing the window.
            if event.type == py.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False #This is so that both the game and the app stops running.
                    self.game.running = False

    def draw_text(self, surface, text, size, colour, x, y):
        # Function that allows text of a chosen font, colour and size to be drawn anywhere on the screen.
        self.font = py.font.Font(self.score_font_name, size) #Creates a font object with the font name and size.
        self.text_surface = self.font.render(text, True, colour) #Creates a surface object for the text so it can be assigned the string of text, the colour and whether it is anti-aliased (Which it is hence the True argument.)
        self.text_rect = self.text_surface.get_rect() #Uses get_rect method to determine text position.
        self.text_rect.midtop = (x, y) #Positions the text.
        surface.blit(self.text_surface, self.text_rect) #Draws the text.

    def draw_arena(self):
        #Draws the arena
        # locates the image and the directory it is in using path.join
        self.bgOriginalImage = py.image.load(path.join(IMG_DIR, ARENAFILE)).convert() #loads the image
        self.arenaBackground = py.transform.scale(self.bgOriginalImage, (WINDOWWIDTH, WINDOWHEIGHT)) #scales the image to window size
        self.arenaBackground_rect = self.arenaBackground.get_rect() #gets dimensions of the image
        self.screen.blit(self.arenaBackground, self.arenaBackground_rect) #draws the arena

    def draw(self):
        # Game Loop - Draw graphics.
        self.draw_arena()
        self.draw_text(self.screen, str(self.player1.points), POINTSFONTSIZE, WHITE, XPOSPOINTSP1, YPOSPOINTS) #Draws the scores.
        self.draw_text(self.screen, str(self.player2.points), POINTSFONTSIZE, WHITE, XPOSPOINTSP2, YPOSPOINTS)
        self.all_sprites.draw(self.screen)
        py.display.flip() # After everything is drawn, the game frame is displayed.

    def checkWin(self, p1score, p2score, sound_effect):
        #Checks which player has won.
        if p1score == 11:
            sound_effect.play()
            self.playing = False
            return 1
        elif p2score == 11:
            sound_effect.play()
            self.playing = False
            return 2
        else:
            return ''

    def detectBallPlayerCollision(self):
        #Below is the code for the ball collision which makes use of the calculateBallAngle
        #method from the Ball class. This makes the ball change direction and speed depending
        #on what part of the paddle the ball hit.
        self.ballPlayerCollision = py.sprite.spritecollide(self.ball, self.playerGroup, False)
        if self.ballPlayerCollision:
            self.ball_off_paddle_sound.play()
            if self.ball.vx > 0:
                # line below was necessary to prevent a bug where the ball
                # gets stuck on the paddle.
                self.ball.rect.x = WINDOWWIDTH - (PADDLEOFFSET + (PADDLEWIDTH/2) + BALLSIDE)
                self.ball.vy = self.ball.calculateBallAngle(self.ball.rect.centery, self.player1.rect.centery, self.player1.length)
            elif self.ball.vx < 0:
                self.ball.rect.x = PADDLEOFFSET  + (PADDLEWIDTH/2)
                self.ball.vy = self.ball.calculateBallAngle(self.ball.rect.centery, self.player2.rect.centery, self.player2.length)
            #Reverses ball velocity.
            self.ball.vx *= -1
            if (random.random() > 0.9) and self.powerUpNotInArena:
                # Randomly generates a power up at random time and position.
                self.powerUp = Powerup()
                self.all_sprites.add(self.powerUp)
                self.powerUpGroup.add(self.powerUp)
                self.powerUpNotInArena = False

    def detectBallPowerUpCollision(self):
        # Performs correct power depending on which one was collected.
        self.ballPowerUpCollision = py.sprite.spritecollide(self.ball, self.powerUpGroup, True)
        if self.ballPowerUpCollision:
            if self.powerUp.type == 'length up':
                self.length_up_sound.play()
                self.powerUp.lengthChange(self.powerUp.type, self.ball.vx, self.player1, self.player2, self) # Ball velocity used to determine which player recieves power up.
            elif self.powerUp.type == 'length down':
                self.length_down_sound.play()
                self.powerUp.lengthChange(self.powerUp.type, self.ball.vx, self.player1, self.player2, self)
            elif self.powerUp.type == 'speed down':
                self.speed_down_sound.play()
                self.powerUp.speedDown(self.ball.vx, self.player1, self.player2, self)
            elif self.powerUp.type == 'balldirect':
                self.ball_direct_sound.play()
                self.powerUp.ballDirect(self.ball, self)
            elif self.powerUp.type == 'barrier':
                self.barrier_power_up_sound.play()
                self.barrier = self.powerUp.barrier(self.ball, self)
                self.all_sprites.add(self.barrier)
                self.barrierGroup.add(self.barrier)

    def detectBallBarrierCollision(self):
        # This is used if the barrier power up is collected. It reflects the ball
        # if it hits the barrier.
        self.ballBarrierCollision = py.sprite.spritecollide(self.ball, self.barrierGroup, False)
        if self.ballBarrierCollision:
            self.ball_off_wall_sound.play()
            self.ball.vx *= -1

    def show_game_over_screen(self):
        # Game's game over screen.
        self.gameOver = True
        self.yesOrNo = 0
        while self.gameOver:
            for event in py.event.get():
                # Checks for closing the window.
                if event.type == py.QUIT:
                    self.running = False
                    self.gameOver = False
                    self.game.running = False

                elif event.type == py.MOUSEMOTION:
                    # Controls mouse events.
                    x, y = event.pos # locates mouse position on the screen.
                    withinYesButton = (79 < x < 213) and (259 < y < 319)
                    withinNoButton = (262 < x < 396) and (259 < y < 319)
                    # Prompts the user on whether they want to quit or restart the game.
                    if withinYesButton:
                        self.yesOrNo = 'yes'
                    elif withinNoButton:
                        self.yesOrNo = 'no'
                    else:
                        self.yesOrNo = 0
                # Checks to see which button the mouse has clicked on
                # and responds accordingly.
                if py.mouse.get_pressed()[0] and withinYesButton:
                    self.playing = True
                    self.gameOver = False
                elif py.mouse.get_pressed()[0] and withinNoButton:
                    self.running = False
                    self.gameOver = False

            self.draw_game_over_text(self.yesOrNo)
            py.display.flip()
            self.clock.tick(FPS) # Adds a frame rate to the game over screen.

    def draw_game_over_text(self, option):
        #This is used to add effect to the buttons as well as draw the game over
        #screen. When the mouse hovers over one of the buttons it highlights itself.
        if option == 0:
            self.load_image('game_over_text')
        elif option == 'yes':
            self.load_image('game_over_text_yes')
        elif option == 'no':
            self.load_image('game_over_text_no')

    def load_image(self, image_file):
        self.image = py.image.load(path.join(IMG_DIR, str(image_file) + str(self.winner) + '.png')).convert()
        self.image_rect = self.image.get_rect()
        self.screen.blit(self.image, self.image_rect)

class Multiplayer(GameModes):
    def __init__(self):
        super().__init__() # Inherits attributes and methods from parent.

    def new(self, game):
        # Start new game. Resets all initial variables and runs the game.
        self.game = game
        self.powerUpNotInArena = True
        self.all_sprites = py.sprite.Group() # Creates groups for sprites to allow for collision detection.
        self.playerGroup = py.sprite.Group()
        self.powerUpGroup = py.sprite.Group()
        self.barrierGroup = py.sprite.Group()
        self.player1 = Player(1) # Creates player and ball objects.
        self.player2 = Player(2)
        self.ball = Ball(self.screen, self.ball_off_wall_sound)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.ball)
        self.playerGroup.add(self.player1)
        self.playerGroup.add(self.player2)
        self.run()

    def update(self):
        # Game Loop - Update (variables and objects have been changed
        #during the game frame.)
        # Performs the update method for every sprite in the all_sprites group.
        self.all_sprites.update()

        self.detectBallPlayerCollision()

        if not self.powerUpNotInArena:
            self.detectBallPowerUpCollision()

        self.detectBallBarrierCollision()
        #This increments the score for the player that scores
        self.player1.points, self.player2.points = self.ball.countPoints(self.player1.points, self.player2.points, self.gained_point_sound)
        #Checks to see if a player has won and which one.
        self.winner = self.checkWin(self.player1.points, self.player2.points, self.game_finished_sound)

class Singleplayer(GameModes):
    def __init__(self):
        super().__init__() # Inherits from parent class.

    def new(self, game):
        # Start new game.
        self.game = game
        self.powerUpNotInArena = True
        self.all_sprites = py.sprite.Group() # Creates groups for sprites to allow for collision detection.
        self.playerGroup = py.sprite.Group()
        self.powerUpGroup = py.sprite.Group()
        self.barrierGroup = py.sprite.Group()
        self.ball = Ball(self.screen, self.ball_off_wall_sound)
        self.player1 = Player(1) # Creates player and ball objects.
        self.player2 = Computer('computer', self.difficulty, self.ball, self.player1)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.ball)
        self.playerGroup.add(self.player1)
        self.playerGroup.add(self.player2)
        self.run()

    def update(self):
        # Updates variables during game.
        self.all_sprites.update()

        self.detectBallPlayerCollision()
        # Only checks if ball collides with powerup if powerup is available.
        if not self.powerUpNotInArena:
            self.detectBallPowerUpCollision()

        self.detectBallBarrierCollision()

        self.player1.points, self.player2.points = self.ball.countPoints(self.player1.points, self.player2.points, self.gained_point_sound)
        #Checks to see if a player has won and which one.
        self.winner = self.checkWin(self.player1.points, self.player2.points, self.game_finished_sound)
        if self.winner == 2:
            # This is to make sure the correct game over screen image, for the
            # computer winning, is selected.
            self.winner = 3

    def difficultyMenu(self, game, clock):
        self.selectingDifficulty = True # flag variables.
        self.windowOpen = True
        while self.selectingDifficulty:
            self.choice = '' # Placeholder value to prevent syntax error.
            for event in py.event.get():
                # Checks for closing the window.
                if event.type == py.QUIT:
                    if self.selectingDifficulty:
                        self.selectingDifficulty = False
                        self.running = False #This is so that both the game and the app stops running.
                        game.running = False
                        self.windowOpen = False

                self.difficultyMenuButtonHover()
                # Checks which difficulty is selected.
                if py.mouse.get_pressed()[0] and self.withinEasyMode:
                    self.difficulty = 'easy'
                    self.selectingDifficulty = False
                elif py.mouse.get_pressed()[0] and self.withinIntermediateMode:
                    self.difficulty = 'intermediate'
                    self.selectingDifficulty = False
                elif py.mouse.get_pressed()[0] and self.withinHardMode:
                    self.difficulty = 'hard'
                    self.selectingDifficulty = False

                self.displayDifficultyMenu(self.choice)
            clock.tick(FPS)

    def difficultyMenuButtonHover(self):
        # Checks which button the mouse is hovering over. Allows buttons to
        # highlight when mouse hovers over them.
        x, y = py.mouse.get_pos()
        self.withinEasyMode = (30 < x < 150) and (170 < y < 220)
        self.withinIntermediateMode = (179 < x < 299) and (170 < y < 220)
        self.withinHardMode = (328 < x < 448) and (170 < y < 220)

        if self.withinEasyMode:
            self.choice = 'easy'
        elif self.withinIntermediateMode:
            self.choice = 'intermediate'
        elif self.withinHardMode:
            self.choice = 'hard'

    def displayDifficultyMenu(self, choice):
        if choice == 'easy':
            self.load_menu_image('_easy')
        elif choice == 'intermediate':
            self.load_menu_image('_intermediate')
        elif choice == 'hard':
            self.load_menu_image('_hard')
        else:
            self.load_menu_image('')
        py.display.flip()

    def load_menu_image(self, choice):
        self.image = py.image.load(path.join(IMG_DIR, 'difficulty_menu{}.png'.format(choice))).convert()
        self.image_rect = self.image.get_rect()
        self.screen.blit(self.image, self.image_rect)

class Challenge(GameModes):
    def __init__(self):
        super().__init__()

    def new(self, game):
        self.game = game
        self.scored = False
        self.obstacleUp = False # Flag
        self.missileUp = False
        self.obstacle_timer = py.time.get_ticks()
        self.missile_timer = py.time.get_ticks()
        self.generate_obstacle_time = random.randrange(MINGENERATETIME, MAXGENERATETIME, 1000)
        self.generate_missile_time = random.randrange(MINSPAWNTIME, MAXSPAWNTIME, 1000)
        self.all_sprites = py.sprite.Group() # Creates groups for sprites to allow for collision detection.
        self.playerGroup = py.sprite.Group()
        self.goalPostGroup = py.sprite.Group()
        self.obstacleGroup = py.sprite.Group()
        self.missileGroup = py.sprite.Group()
        self.player = Player(1)
        self.ball = Ball(self.screen, self.ball_off_wall_sound)
        self.goalPost = Goalpost(self.goalPostGroup)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.goalPost)
        self.goalPostGroup.add(self.goalPost)
        self.playerGroup.add(self.player)
        self.run()

    def update(self):
        self.all_sprites.update()
        self.sideWallCollision()
        self.goalPost.goalPostBallCollision(self, self.ball, self.player, self.ball_off_paddle_sound, self.gained_point_sound)
        self.detectBallPlayerCollision()
        # Checks for obstacle and missile collision if they exist.
        if self.obstacleUp:
            self.obstacle.detectObstacleBallCollision(self.ball, self.ball_off_wall_sound)
            if self.missileUp:
                self.missile.detectMissileObstacleCollision(self.missile_collision_sound)
        if self.missileUp:
            self.missile.detectMissilePlayerCollision(self.missile_collision_sound)
        if self.player.health <= 0:
            # The game is over if player's health reaches 0.
            self.game_finished_sound.play()
            self.playing = False

        self.now = py.time.get_ticks()
        if self.now - self.obstacle_timer > self.generate_obstacle_time:
            # Generates obstacles at a random time.
            self.scored = False
            self.generate_obstacle()
            self.obstacleUp = True
        if self.now - self.missile_timer > self.generate_missile_time:
            # Spawns missile at a random time.
            self.spawn_missile()
            self.missileUp = True

    def generate_obstacle(self):
        # Generates obstacle.
        self.obstacle = Obstacle(self, self.obstacleGroup)
        self.all_sprites.add(self.obstacle)
        self.obstacleGroup.add(self.obstacle)
        self.obstacle_timer = py.time.get_ticks() # Resets spawn timer.
        self.generate_obstacle_time = random.randrange(MINGENERATETIME, MAXGENERATETIME, 1000)

    def spawn_missile(self):
        # Spawns missile.
        self.missile_launch_sound.play()
        self.missile = Missile(self, self.player)
        self.all_sprites.add(self.missile)
        self.missileGroup.add(self.missile)
        self.missile_timer = py.time.get_ticks()
        self.generate_missile_time = random.randrange(MINSPAWNTIME, MAXSPAWNTIME, 1000)

    def draw(self):
        # Game Loop - Draw graphics.
        self.draw_arena()
        self.draw_text(self.screen, str(self.player.points), POINTSFONTSIZE, WHITE, WINDOWWIDTH/2, 30)
        self.draw_health_bar(self.screen, WINDOWWIDTH - 145, 30, self.player.health)
        self.all_sprites.draw(self.screen)
        py.display.flip() # After everything is drawn, the game frame is displayed.

    def draw_arena(self):
        # Draws the arena
        # locates the image and the directory it is in using path.join
        self.bgOriginalImage = py.image.load(path.join(IMG_DIR, CHALLENGEARENAFILE)).convert() #loads the image
        self.arenaBackground = py.transform.scale(self.bgOriginalImage, (WINDOWWIDTH, WINDOWHEIGHT)) #scales the image to window size
        self.arenaBackground_rect = self.arenaBackground.get_rect() #gets dimensions of the image
        self.screen.blit(self.arenaBackground, self.arenaBackground_rect) #draws the arena

    def draw_game_over_text(self, option):
        #This is used to add effect to the buttons as well as draw the game over
        #screen. When the mouse hovers over one of the buttons it highlights itself.
        if option == 0:
            self.load_image('challenge_game_over_text')
        elif option == 'yes':
            self.load_image('challenge_game_over_text_yes')
        elif option == 'no':
            self.load_image('challenge_game_over_text_no')
        self.draw_text(self.screen, 'Score: {}'.format(self.player.points), POINTSFONTSIZE, WHITE, 240, 120)

    def load_image(self, image_file):
        self.image = py.image.load(path.join(IMG_DIR, str(image_file) + '.png')).convert()
        self.image_rect = self.image.get_rect()
        self.screen.blit(self.image, self.image_rect)

    def detectBallPlayerCollision(self):
        # Below is the code for the ball collision which makes use of the calculateBallAngle
        # method from the Ball class. This makes the ball change direction and speed depending
        # on what part of the paddle the ball hit.
        self.ballPlayerCollision = py.sprite.spritecollide(self.ball, self.playerGroup, False)
        if self.ballPlayerCollision:
            self.ball_off_paddle_sound.play()
            if self.ball.vx > 0:
                # Line below was necessary to prevent a bug where the ball
                # gets stuck on the paddle.
                self.ball.rect.x = WINDOWWIDTH - (PADDLEOFFSET + (PADDLEWIDTH/2) + BALLSIDE)
                self.ball.vy = self.ball.calculateBallAngle(self.ball.rect.centery, self.player.rect.centery, self.player.length)
            # Reverses ball velocity.
            self.ball.vx *= -1

    def sideWallCollision(self):
        # Reduces player's health if it hits their side of the wall.
        if self.ball.rect.left < BORDERTHICKNESS:
            self.ball_off_wall_sound.play()
            self.ball.rect.left = BORDERTHICKNESS
            self.ball.vx *= -1
        elif self.ball.rect.right > WINDOWWIDTH - BORDERTHICKNESS:
            self.ball_off_wall_sound.play()
            self.player.health -= 20
            self.ball.rect.right = WINDOWWIDTH - BORDERTHICKNESS
            self.ball.vx *= -1

    def draw_health_bar(self, surface, x, y, percentage):
        # Draws health bar according to the player's amount of health.
        if percentage < 0:
            percentage = 0
        self.fill = (percentage / 100) * HEALTHBARLENGTH
        self.outline_rect = py.Rect(x, y, HEALTHBARLENGTH, HEALTHBARHEIGHT)
        self.fill_rect = py.Rect(x, y, self.fill, HEALTHBARHEIGHT)
        py.draw.rect(surface, GREEN, self.fill_rect)
        py.draw.rect(surface, WHITE, self.outline_rect, 2)

class Settings:
    def __init__(self, game):
        self.game = game
        self.screen = py.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.clock = py.time.Clock()
        self.controlsOn = False # Flag variables for each settings option.
        self.powerupsOn = False
        self.descriptionOn = False
        self.settingsOptionRunning = True
        self.running = True

    def quitEventCheck(self):
        for event in py.event.get():
            # Checks for closing the window.
            if event.type == py.QUIT:
                self.running = False
                self.settingsOptionRunning = False
                self.game.running = False

    def events(self):
        self.option = ''
        self.settingsOptionRunning = True
        self.quitEventCheck()
        self.checkButtonHover()
        # Checks which button has been clicked in main menu and returns
        # appropriate option variable.
        if py.mouse.get_pressed()[0] and self.withinControls:
            while self.settingsOptionRunning:
                self.controls_events()
        elif py.mouse.get_pressed()[0] and self.withinPowerups:
            while self.settingsOptionRunning:
                self.powerups_events()
        elif py.mouse.get_pressed()[0] and self.withinDescription:
            while self.settingsOptionRunning:
                self.description_events()
        elif py.mouse.get_pressed()[0] and self.withinMain:
            self.running = False

        self.draw_settings_menu()
        py.display.flip()
        self.clock.tick(FPS)

    def draw_settings_menu(self):
        # Draws the settings menu and highlight buttons that the mouse is hovering over.
        if not self.option == '':
            self.load_menu_image('_{}'.format(self.option))
        else:
            self.load_menu_image('')

    def load_menu_image(self, choice):
        self.image = py.image.load(path.join(IMG_DIR, 'settings_menu{}.png'.format(str(choice)))).convert() #loads the image
        self.image_rect = self.image.get_rect() #gets dimensions of the image
        self.screen.blit(self.image, self.image_rect)

    def checkButtonHover(self):
        self.x, self.y = py.mouse.get_pos()
        self.withinControls = (163 < self.x < 314) and (110 < self.y < 160)
        self.withinPowerups = (163 < self.x < 314) and (179 < self.y < 225)
        self.withinDescription = (165 < self.x < 316) and (244 < self.y < 294)
        self.withinMain = (30 < self.x < 140) and (300 < self.y < 350)

        if self.withinControls:
            self.option = 'controls'
        elif self.withinPowerups:
            self.option = 'powerups'
        elif self.withinDescription:
            self.option = 'description'
        elif self.withinMain:
            self.option = 'main'

    def settingsButtonHover(self):
        self.x, self.y = py.mouse.get_pos()
        self.withinMain = (30 < self.x < 140) and (300 < self.y < 350)

        if self.controlsOn:
            if self.withinMain:
                self.settingsOption = 'controls1'
            else:
                self.settingsOption = 'controls'
            self.controlsOn = False
        elif self.powerupsOn:
            if self.withinMain:
                self.settingsOption = 'powerups1'
            else:
                self.settingsOption = 'powerups'
            self.powerupsOn = False
        elif self.descriptionOn:
            if self.withinMain:
                self.settingsOption = 'description1'
            else:
                self.settingsOption = 'description'
            self.descriptionOn = False

    def draw_subsettings_menu(self):
        self.load_subsettings_image(self.settingsOption + '.png')

    def load_subsettings_image(self, choice):
        self.image = py.image.load(path.join(IMG_DIR, choice)).convert() #loads the image
        self.image_rect = self.image.get_rect() #gets dimensions of the image
        self.screen.blit(self.image, self.image_rect)

    def subsettings_procedure(self):
        # This is a common procedure each settings option goes over.
        self.quitEventCheck()
        self.settingsButtonHover()
        if py.mouse.get_pressed()[0] and self.withinMain:
            self.settingsOptionRunning = False
        self.draw_subsettings_menu()
        py.display.flip() # After everything is drawn, the game frame is displayed.
        self.clock.tick(FPS)
# Displays appropriate settings option.
    def controls_events(self):
        self.controlsOn = True
        self.subsettings_procedure()

    def powerups_events(self):
        self.powerupsOn = True
        self.subsettings_procedure()

    def description_events(self):
        self.descriptionOn = True
        self.subsettings_procedure()
