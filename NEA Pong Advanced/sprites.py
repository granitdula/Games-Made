# Sprite classes in the game.
import pygame as py
from settings import *
import math
import random

class Paddle(py.sprite.Sprite):
    # This creates the Player class with its attributes and methods.
    # Used by the main.py file to create player objects for both player 1 and 2.
    # The parent class to the Player class and Computer class.
    def __init__(self, player_num):
        py.sprite.Sprite.__init__(self) #Initialises it as a sprite.
        self.player_num = player_num
        self.health = 100
        self.points = 0
        self.speed = 10
        self.minSpeed = 6
        self.length = 70
        self.maxLength = 90
        self.minLength = 50
        self.original_image = py.image.load(path.join(IMG_DIR, PADDLEFILE)).convert_alpha() #Creates image object.
        self.image = py.transform.scale(self.original_image, (PADDLEWIDTH, self.length)) #Scales the original image.
        self.rect = self.image.get_rect() #Uses get_rect method to determine paddle position
        # Positions paddle on the left or right of the screen depending on which player it is.
        if self.player_num == 1:
            self.rect.center = (WINDOWWIDTH - PADDLEOFFSET, WINDOWHEIGHT/2)
        else:
            self.rect.center = (PADDLEOFFSET, WINDOWHEIGHT/2)
        self.vy = 0 # Assigns initial paddle velocity of both paddles.

    def update(self):
        # Updates paddle position.
        self.vy = 0 #Paddle velocity stays at 0 if key not pressed.
        self.keyPressInput()
        #Increments y position of paddle depending on its velocity.
        self.rect.y += self.vy

        #Makes sure paddle can't move past the top or bottom of the screen.
        if self.rect.top < BORDERTHICKNESS:
            self.rect.top = BORDERTHICKNESS
        elif self.rect.bottom > (WINDOWHEIGHT - BORDERTHICKNESS):
            self.rect.bottom = WINDOWHEIGHT - BORDERTHICKNESS

class Player(Paddle):
    def __init__(self, player_num):
        super().__init__(player_num) # Inherits from parent class.

    def keyPressInput(self):
        self.keys = py.key.get_pressed() #Uses get_pressed method to take input from the keyboard.
        # The paddles for each player will move depending on the key pressed.
        if self.player_num == 1:
            if self.keys[py.K_UP]:
                self.vy = -self.speed
            elif self.keys[py.K_DOWN]:
                self.vy = self.speed
        else:
            if self.keys[py.K_w]:
                self.vy = -self.speed
            elif self.keys[py.K_s]:
                self.vy = self.speed

class Ball(py.sprite.Sprite):
    #This creates the Ball class with its attributes and methods, used in main.py
    def __init__(self, screen, sound):
        py.sprite.Sprite.__init__(self) # Initialise as a sprite.
        self.screen = screen
        self.ball_off_wall_sound = sound
        self.image = py.image.load(path.join(IMG_DIR, BALLFILE)).convert_alpha() #Dimensions of ball.
        self.image = py.transform.scale(self.image, (BALLSIDE, BALLSIDE))
        self.rect = self.image.get_rect()
        # Assigns initial position of the ball.
        self.rect.center = (int(WINDOWWIDTH/2) + 1, int(WINDOWHEIGHT/2))
        self.speed = 12 # Initial speed of the ball when game starts.
        # Randomises the direction the ball initially moves at.
        self.angle = random.uniform((math.pi/6), (math.pi * (5/6)))
        # Calculates velocity components using the speed and angle.
        self.vx = math.sin(self.angle) * self.speed
        self.vy = math.cos(self.angle) * self.speed

    def update(self):
        # Updates ball position.
        self.rect.x += self.vx # The ball is continuously moving.
        self.rect.y += self.vy
        #When the ball hits the top or bottom of the screen it will rebound off it.
        if self.rect.top < BORDERTHICKNESS:
            self.ball_off_wall_sound.play()
            self.rect.y = BORDERTHICKNESS #This fixes a bug where the ball can get stuck at the top or bottom of the screen.
            self.vy *= -1
        if self.rect.bottom > (WINDOWHEIGHT - BORDERTHICKNESS):
            self.ball_off_wall_sound.play()
            self.rect.y = (WINDOWHEIGHT - BORDERTHICKNESS) - BALLSIDE
            self.vy *= -1

    def calculateBallAngle(self, ballY, paddleY, paddleLength):
        #This function determines the velocity of the ball depending on where the
        #ball hits the paddle. e.g: if it hits at the top of the paddle, it will
        #move quicker. This makes the motion of the ball more realistic.
        return (self.speed * (((ballY-paddleY))/(paddleLength/2)))

    def countPoints(self, p1points, p2points, sound_effect):
        #It increases the points of the scoring player.
        if self.rect.left < 0:
            sound_effect.play()
            p1points += 1
            #It also re-positions the ball at the centre once a player scores.
            self.spawnBall(-1)
        elif self.rect.right > WINDOWWIDTH:
            sound_effect.play()
            p2points += 1
            self.spawnBall(1)
        return p1points, p2points

    def spawnBall(self, xDir):
        self.rect.center = (int(WINDOWWIDTH/2) + 1, int(WINDOWHEIGHT/2))
        self.angle = random.uniform((math.pi/6), (math.pi * (5/6)))
        self.vx = math.sin(self.angle) * self.speed * xDir
        self.vy = math.cos(self.angle) * self.speed

    def getBallDirection(self):
        # Used by one of the Powerup methods to determine the direction of ball.
        xDir = (self.vx > 0) - (self.vx < 0)
        yDir = (self.vy > 0) - (self.vy < 0)
        return xDir, yDir

class Powerup(py.sprite.Sprite):
    #This creates the Powerup class with its attributes and methods. It is used
    #in the main.py file to spawn random power ups at random times which players
    #use to gain advantages.
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        # Randomise the position of the power up spawn around the center of the arena.
        self.center = (random.randrange(180, 300), random.randrange(60, 300))
        self.powerUpImages = {} # Stores power up icons.
        # Loads all power up images and stores them in a dictionary
        self.powerUpImages['length up'] = py.image.load(path.join(IMG_DIR, 'length_up.png')).convert()
        self.powerUpImages['length down'] = py.image.load(path.join(IMG_DIR, 'length_down.png')).convert()
        self.powerUpImages['speed down'] = py.image.load(path.join(IMG_DIR, 'speed_down.png')).convert()
        self.powerUpImages['barrier'] = py.image.load(path.join(IMG_DIR, 'barrier.png')).convert()
        self.powerUpImages['balldirect'] = py.image.load(path.join(IMG_DIR, 'ball_direct.png')).convert()
        for key in self.powerUpImages:
            # Transform all images in the dictionary to appropriate size.
            self.powerUpImages[key] = py.transform.scale(self.powerUpImages[key], (POWERUPSIZE, POWERUPSIZE))
        # Selects random power up.
        self.type = random.choice(['length up', 'length down', 'speed down', 'barrier', 'balldirect'])
        self.image = self.powerUpImages[self.type] # Assigns image object.
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def lengthChange(self, upOrDown, ballVelocityX, player1, player2, multiplayer):
        # Changes the lengths of the appropriate paddle that collects the length
        # up or length down power up.
        if upOrDown == 'length up':
            self.changeInLength = 20
        else:
            self.changeInLength = -20

        if ballVelocityX < 0:
            # Player1 has shot the ball last.
            if (player1.length < player1.maxLength) and self.changeInLength == 20:
                self.lengthTransform(player1, multiplayer)
            elif (player1.length > player1.minLength) and self.changeInLength == -20:
                self.lengthTransform(player1, multiplayer)
        elif ballVelocityX > 0:
            # Player2 has shot the ball last.
            if (player2.length < player2.maxLength) and self.changeInLength == 20:
                self.lengthTransform(player2, multiplayer)
            elif (player2.length > player2.minLength) and self.changeInLength == -20:
                self.lengthTransform(player2, multiplayer)

    def lengthTransform(self, player, multiplayer):
        player.length += self.changeInLength
        # The original_image variable maintains the quality of the image for every
        # transformation performed on the image.
        player.image = py.transform.scale(player.original_image, (PADDLEWIDTH, player.length))
        center = player.rect.center
        player.rect = player.image.get_rect()
        player.rect.center = center
        multiplayer.powerUpNotInArena = True

    def speedDown(self, ballVelocityX, player1, player2, multiplayer):
        # Reduces the speed of the enemy paddle.
        if ballVelocityX < 0:
           # Player 1 has shot the ball last.
           if player2.speed > player2.minSpeed:
               player2.speed -= 2
               multiplayer.powerUpNotInArena = True

        if ballVelocityX > 0:
           # Player 2 has shot the ball last.
           if player1.speed > player1.minSpeed:
               player1.speed -= 2
               multiplayer.powerUpNotInArena = True

    def ballDirect(self, ball, multiplayer):
        # Changes the direction of the ball depending on its current direction.
        xDir, yDir = ball.getBallDirection()
        if xDir > 0 and yDir < 0:
            # If its moving diagonally downwards it changes to move diagonally
            # upwards.
            angle = math.pi / 4
        else: # And vice versa.
            angle = (3 * math.pi) / 4
        ball.vx = math.sin(angle) * ball.speed * xDir
        ball.vy = math.cos(angle) * ball.speed * yDir
        multiplayer.powerUpNotInArena = True

    def barrier(self, ball, multiplayer):
        # Creates a barrier for the player who collects the power up temporarily
        if ball.vx < 0: # Player 1
            leftSideOfBarrier = WINDOWWIDTH - BARRIERWIDTH
            barrier = Barrier(leftSideOfBarrier) # Creates barrier object.
            multiplayer.powerUpNotInArena = True
            return barrier
        else: # Player 2
            leftSideOfBarrier = 0
            barrier = Barrier(leftSideOfBarrier)
            multiplayer.powerUpNotInArena = True
            return barrier

class Barrier(py.sprite.Sprite):
    # Produces the actual barrier for the barrier power up.
    def __init__(self, leftSide):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load(path.join(IMG_DIR, 'barrierImage3.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = leftSide
        self.power_time = py.time.get_ticks() # Barrier starting time.

    def update(self):
        self.now = py.time.get_ticks() # Gets current time as game runs.
        # Barrier is destroyed once 8 seconds are over.
        if self.now - self.power_time >= BARRIERUPTIME:
            self.kill()

class Goalpost(py.sprite.Sprite):
    # Displays a goal and detects whether the ball goes in and so increase player points.
    def __init__(self, goalPostGroup):
        py.sprite.Sprite.__init__(self)
        self.goalPostGroup = goalPostGroup
        self.image = py.image.load(path.join(IMG_DIR, 'goalpost.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = BORDERTHICKNESS
        self.rect.centery = (WINDOWHEIGHT / 2) - 5

    def goalPostBallCollision(self, challenge, ball, player, collision_sound, point_sound):
        withinPostX = ball.rect.left <= GOALPOSTWIDTH + BORDERTHICKNESS - GOALDEPTH
        withinTopPostY = 116 < ball.rect.centery < 124
        withinBottomPostY = 226 < ball.rect.centery < 234
        withinGoalRegion = 127 < ball.rect.centery < 223
        self.ballGoalPostCollision = py.sprite.spritecollide(ball, self.goalPostGroup, False)
        if withinPostX and withinGoalRegion:
            challenge.scored = True
            point_sound.play()
            player.points += 1
            ball.spawnBall(1)
        elif self.ballGoalPostCollision:
            collision_sound.play()
            if ball.rect.centery < WINDOWHEIGHT / 2:
                ball.vy = abs(ball.vy) * (-1) - 1
            else:
                ball.vy = abs(ball.vy) + 1

class Obstacle(py.sprite.Sprite):
    def __init__(self, challenge, obstacleGroup):
        py.sprite.Sprite.__init__(self)
        self.challenge = challenge
        self.starting_time = py.time.get_ticks() # timer for randomly generating obstacles.
        self.obstacleGroup = obstacleGroup
        self.center = (random.randrange(170, 250), random.randrange(167, 193))
        self.obstacleImages = {}
        # Stores variety of obstacle shapes and sizes.
        self.obstacleImages['tiny'] = py.image.load(path.join(IMG_DIR, 'tiny_obstacle.png')).convert()
        self.obstacleImages['small'] = py.image.load(path.join(IMG_DIR, 'small_obstacle.png')).convert()
        self.obstacleImages['medium'] = py.image.load(path.join(IMG_DIR, 'medium_obstacle.png')).convert()
        self.obstacleImages['large'] = py.image.load(path.join(IMG_DIR, 'large_obstacle.png')).convert()
        self.size = random.choice(['tiny', 'small', 'medium', 'large'])
        self.image = self.obstacleImages[self.size]
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def update(self):
        # Destroys obstacle once it reaches its time limit of 5 seconds or if player scores.
        self.now = py.time.get_ticks()
        if (self.now - self.starting_time > OBSTACLEUPTIME) or self.challenge.scored:
            self.challenge.scored = False
            self.challenge.obstacleUp = False
            self.challenge.timer = py.time.get_ticks()
            self.kill()

    def detectObstacleBallCollision(self, ball, sound_effect):
        self.topCollide = ball.rect.centery <= self.rect.top
        self.withinLength = (ball.rect.top <= self.rect.bottom) and (ball.rect.bottom >= self.rect.top)
        self.leftCollide = (self.rect.left <= (ball.rect.centerx + 10) <= self.rect.left + 8) and self.withinLength
        self.rightCollide = (self.rect.right - 8 <= (ball.rect.centerx - 10) <= self.rect.right) and self.withinLength
        self.ballObstacleCollide = py.sprite.spritecollide(ball, self.obstacleGroup, False)
        if self.leftCollide:
            ball.vx = abs(ball.vx) * (-1)
            sound_effect.play()
        elif self.rightCollide:
            ball.vx = abs(ball.vx)
            sound_effect.play()

        elif self.ballObstacleCollide:
            if self.topCollide:
                ball.vy = abs(ball.vy) * (-1)
            else:
                ball.vy = abs(ball.vy)
            sound_effect.play()

class Missile(py.sprite.Sprite):
    def __init__(self, challenge, player):
        py.sprite.Sprite.__init__(self)
        self.player = player
        self.challenge = challenge
        # Below generates random starting height value of missile.
        self.y = random.randrange(5 + BORDERTHICKNESS, WINDOWHEIGHT - BORDERTHICKNESS - 5)
        self.image = py.image.load(path.join(IMG_DIR, 'missile.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.centery = self.y
        self.rect.centerx = MISSILEPOSX
        self.acceleration = 0.2 # missile changes velocity to add realism to motion
        # and to also give an element of unpredictability to the motion of the missile.
        self.vx = 8
        self.vy = 4

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vx += self.acceleration
        if self.rect.centerx > WINDOWWIDTH + 70:
            # Destroys missile if it goes past the side wall.
            self.challenge.missileUp = False
            self.kill()
        self.followPaddle()

    def followPaddle(self):
        # Follow y position of paddle.
        if self.rect.centery < self.player.rect.centery:
            self.vy = abs(self.vy)
        elif self.rect.centery > self.player.rect.centery:
            self.vy = abs(self.vy) * (-1)

    def detectMissileObstacleCollision(self, sound_effect):
        # Destroys missile if it collides with obstacle.
        self.missileObstacleCollide = py.sprite.spritecollide(self.challenge.obstacle, self.challenge.missileGroup, True)
        if self.missileObstacleCollide:
            sound_effect.play()
            self.challenge.missileUp = False

    def detectMissilePlayerCollision(self, sound_effect):
        # Destroys missile if it hits player paddle and reduces players health by 50%.
        self.missilePlayerCollide = py.sprite.spritecollide(self.challenge.player, self.challenge.missileGroup, True)
        if self.missilePlayerCollide:
            sound_effect.play()
            self.challenge.missileUp = False
            self.challenge.player.health -= 50

class Computer(Paddle):
    # This Computer class is used to make the computer paddle be controlled by
    # the computer and have varying difficulty.
    def __init__(self, player_num, difficulty, ball, player):
        super().__init__(player_num) # Inherits from parent class.
        self.difficulty = difficulty
        self.ball = ball
        self.player = player

    def update(self):
        # Updates paddle position.
        # Depending on the difficulty the player chose, the computer will run
        # a certain algorithm for its motion.
        if self.difficulty == 'easy':
            self.easyMode()
        elif self.difficulty == 'intermediate':
            self.intermediateMode()
        else:
            self.hardMode()
        #Increments y position of paddle depending on its velocity.
        self.rect.y += self.vy

        #Makes sure paddle can't move past the top or bottom of the screen.
        if self.rect.top < BORDERTHICKNESS:
            self.rect.top = BORDERTHICKNESS
        elif self.rect.bottom > (WINDOWHEIGHT - BORDERTHICKNESS):
            self.rect.bottom = WINDOWHEIGHT - BORDERTHICKNESS

    def easyMode(self):
        # Easy mode means the paddle will be moving at minimum speed.
        self.speed = 6
        # Follows balls y position.
        if self.ball.rect.centery < self.rect.centery:
            self.vy = -self.speed
        elif self.ball.rect.centery > self.rect.centery:
            self.vy = self.speed
        # The line below fixes a bug where the computer begins vibrating up and
        # down when the ball is moving almost at a horizontal angle.
        if self.ball.rect.centery - 13 < self.rect.centery < self.ball.rect.centery + 13:
            self.vy = 0

    def intermediateMode(self):
        # In intermediate mode the paddle will move slightly faster than easy
        # mode, but still slower than the player.
        self.speed = 8
        if self.ball.rect.centery < self.rect.centery:
            self.vy = -self.speed
        elif self.ball.rect.centery > self.rect.centery:
            self.vy = self.speed
        if self.ball.rect.centery - 13 < self.rect.centery < self.ball.rect.centery + 13:
            self.vy = 0

    def hardMode(self):
        # default speed is 10 (Same as player).
        # Implements a more sophisticated algorithm than just following the
        # ball's y position.
        # if player is up, computer tries to hit with the top of the paddle,
        # and vice versa when the player is down, in order to make the ball move
        # in an inconvenient position for the player and at a faster speed.
        self.preparePosition()
        if (self.ball.rect.x < WINDOWWIDTH / 2) and (self.ball.vx < 0):
            if self.player.rect.bottom < self.ball.rect.centery: # higher
                if self.ball.rect.centery < self.rect.top:
                    self.vy = -self.speed
                elif self.ball.rect.centery > self.rect.top:
                    self.vy = self.speed

            elif self.player.rect.top > self.ball.rect.centery: # lower
                if self.ball.rect.centery < self.rect.bottom:
                    self.vy = -self.speed
                elif self.ball.rect.centery > self.rect.bottom:
                    self.vy = self.speed
        elif self.ball.vx < 0:
            if self.ball.rect.centery < self.rect.centery:
                self.vy = -self.speed
            elif self.ball.rect.centery > self.rect.centery:
                self.vy = self.speed

        if self.ball.rect.centery - 10 < self.rect.centery < self.ball.rect.centery + 10:
            self.vy = 0

    def preparePosition(self):
        # Computer returns to ideal positio (middle) once it returns the ball, to
        # better prepare for the players shot, by covering space more efficiently.
        if self.ball.vx > 0:
            if self.rect.centery < (WINDOWHEIGHT / 2) - 10:
                self.vy = self.speed
            elif self.rect.centery > (WINDOWHEIGHT / 2) + 10:
                self.vy = -self.speed
            elif (WINDOWHEIGHT / 2) - 10 < self.rect.centery < (WINDOWHEIGHT / 2) + 10:
                self.vy = 0
