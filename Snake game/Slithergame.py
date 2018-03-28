import pygame
import time
import random
#Tutorial PART 42. 
pygame.init() # Initialise pygame
white = (255,255,255) # (|RED|GREEN|BLUE|)
black = (0, 0, 0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode([display_width,display_height]) # Sets up the game display and the window
pygame.display.set_caption("Slither")# Sets the game title

icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon) #a function which edits the icon at the top left. BEST TO USE A 32 by 32 image for icon.

#pygame.display.update()  Updates whats on the screen. DO THIS EVERY TIME YOU EDIT WINDOW

img = pygame.image.load("snakehead.png") # pygame.image.load loads an image. IMAGE HAS TO BE IN THE SAME DIRECTORY AS THE CODE. arg 'image.png'
appleimg = pygame.image.load("apple.png")

AppleThickness = 30
block_size = 20
FPS = 30
clock = pygame.time.Clock() # sleep function in pygame.

direction = "right" # initial direction of the snake.

smallfont = pygame.font.SysFont("comicsansms", 25) #Takes a font object from the "SysFont" library. arg1: font arg2: font size.
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def game_intro(): #Intro screen

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither", green, -100, size="large")
        message_to_screen("The objective of the game is to eat red apples", black, -30) #These will be given a "small" font by default
        message_to_screen("The more apples you eat the longer you get", black, 10)
        message_to_screen("If you run into yourself or the edges, you die!", black, 50)
        message_to_screen("Press C to play or Q to quit.", black, 180)
        pygame.display.update()
        clock.tick(4)

def pause():

    paused = True
    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press C to continue, P to pause or Q to quit", black, 25)

    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)
        clock.tick(5)


def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))
    randAppleY = round(random.randrange(0, display_height - AppleThickness))
    return randAppleX, randAppleY



def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(img, 270) #the function rotates an image anti-clockwise arg1: image arg2: degrees

    if direction == "left":
        head = pygame.transform.rotate(img, 90)

    if direction == "up":
        head = img

    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size]) ## (Location to draw, Colour, [Location along X (Starts from top left of screen), Loc along Y, Width, Height])
    
def text_object(text, colour, size):
    if size == "small":
        textSurface = smallfont.render(text, True, colour)
    elif size == "medium":
        textSurface = medfont.render(text, True, colour)
    elif size == "large":
        textSurface = largefont.render(text, True, colour)
    return textSurface, textSurface.get_rect() # .get_rect() is a function that turns the text into a rectangle,

def message_to_screen(msg,colour, y_displace=0, size="small"): 
    textSurf, textRect = text_object(msg,colour,size)
    #screen_text = font.render(msg, True, colour) #creates the text and assigns it to the variable. arg1: text arg2: True arg3:colour
    #gameDisplay.blit(screen_text, [display_width/2,display_height/2]) #prints text on gameDisplay arg1: text arg2: location in form of a list (width,height).
    textRect.center = (display_width / 2), (display_height / 2) + y_displace # .center is the center point of the rectangle. that can be assigned a new value by giving an x and y value it tuple form.
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    global direction
    direction = "right" # Did this to reset the direction to right.
    gameExit = False
    gameOver = False
 
    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    randAppleX, randAppleY = randAppleGen()

    snakeList = []
    snakeLength = 1
    while not gameExit:
        if gameOver == True:
            message_to_screen(("Game over"), red, -50, size="large")
            message_to_screen("Press C to play again or Q to quit", black, 50)
            pygame.display.update()
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    
            
        for event in pygame.event.get(): # All the events in pygame
            #print(event)  #Its like the serial monitor in Arduino
            if event.type == pygame.QUIT: # Search in Google "pygame.event" for all the events such as KEYDOWN
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
            '''if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #Moves whilst holding key.
                    lead_x_change = 0'''

        if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0: #exits the game when you move out of the screen.
            gameOver = True
           #print(snakeLength - 1)     

        lead_x += lead_x_change #continuously increments by 10.
        lead_y += lead_y_change
            
        gameDisplay.fill(white)
        
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        gameDisplay.blit(appleimg, (randAppleX, randAppleY))


        
        snakeHead = [] 
        snakeHead.append(lead_x) #forming a head block into a list.
        snakeHead.append(lead_y)
        snakeList.append(snakeHead) #appending snakeHead to snakeList to form the body of the snake aswell as the head in form of a 2D array.

        if len(snakeList) > snakeLength:
            del snakeList[0] # this prevents the snake from growing constantly

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
                #print(snakeLength - 1)
        snake(block_size, snakeList)

        score(snakeLength-1)
        
        pygame.display.update()
        #gameDisplay.fill(red, rect = [200, 200, 50, 50]) # Another way of Drawing than the method above.
##        if lead_x == randAppleX and lead_y == randAppleY: #EAT APPLE
##            randAppleX = round(random.randrange(0, display_width - block_size)/10.0)*10.0
##            randAppleY = round(random.randrange(0, display_height - block_size)/10.0)*10.0
##            while lead_x == randAppleX and lead_y == randAppleY:# Makes Sure apple spawns in different area and not the same place it was eaten in.
##                randAppleX = round(random.randrange(0, display_width - block_size)/10.0)*10.0
##                randAppleY = round(random.randrange(0, display_height - block_size)/10.0)*10.0
##            snakeLength += 1    
            

##        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness:
##            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
##                randAppleX = round(random.randrange(0, display_width - block_size))#/10.0)*10.0
##                randAppleY = round(random.randrange(0, display_height - block_size))#/10.0)*10.0
##                while lead_x == randAppleX and lead_y == randAppleY:
##                    randAppleX = round(random.randrange(0, display_width - block_size))#/10.0)*10.0
##                    randAppleY = round(random.randrange(0, display_height - block_size))#/10.0)*10.0
##                snakeLength += 1


        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                #randAppleX = round(random.randrange(0, display_width - AppleThickness))#/10.0)*10.0
                #randAppleY = round(random.randrange(0, display_height - AppleThickness))#/10.0)*10.0
                randAppleX, randAppleY = randAppleGen() #This is the same thing as the commented code directly above but called from a function to make the code more easy to maintain.
                while lead_x == randAppleX and lead_y == randAppleY:
                    randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                while lead_x == randAppleX and lead_y == randAppleY:
                    randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS) # sleep function with FPS taken as the arg.

    pygame.quit()
    quit

game_intro()
gameLoop()
    
