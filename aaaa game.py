#code from pythonprogamming.net
#imports
import pygame
import time
import random


#initialize pygame 
pygame.init()

#window size 
display_width = 800
display_height = 600

#colors 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
brown = (100,40,0)
pink = (255,100,180)

#color for block to be dodged 
block_color = (127,127,127)

#size of player in game 73 so that its not too big
player_width = 73

#game screen 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Tightrope Dodge')
clock = pygame.time.Clock()

#image of player 
playerImg = pygame.image.load('player.png')

#counter of objects dodged 
def blocks_dodged(count):
    font = pygame.font.SysFont(None, 25) #size of font
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

#blocks to be dodged with its x y, width height and colour 

def blocks(blockx, blocky, blockw, blockh, color):
    pygame.draw.rect(gameDisplay, color, [blockx, blocky, blockw, blockh])

#the player 
class Player():
    
    def player(image,x,y):
        gameDisplay.blit(playerImg,(x,y))

#to put text 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#code for quit button
def quitgame():
    pygame.quit()

#button function    
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20) #size of font
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)    

#sound
hit_sound = pygame.mixer.Sound("hit.wav")

#how to indicate that the player lost
def hit():
    
    #calling the sound when hit
    pygame.mixer.Sound.play(hit_sound)
    largeText = pygame.font.SysFont("comicsansms",115) #size of font
    TextSurf, TextRect = text_objects("You Got Hit", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

#game over screen buttons
        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15) #refresh rate

#start menu
def start_menu():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(pink)
        #for the title
        largeText = pygame.font.SysFont("comicsansms",100)
        TextSurf, TextRect = text_objects("Tightrope Dodge", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
#start or quit buttons
        button("Start",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)


        pygame.display.update()
        clock.tick(15)    
    

#loop of game so that it runs    
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    x_change = 0
 
 #to indicate that the blocks would generate randomly
    block_startx = random.randrange(0, display_width)
    block_starty = -600 #so that blocks form off screen
    block_speed = 4 #starting speed
    block_width = 100
    block_height = 100
 
    blockCount = 1
 
    dodged = 0
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
            #to make the player move
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(white)
 
        #to make the blocks that will fall
        blocks(block_startx, block_starty, block_width, block_height, block_color)

        #adding a rope to the screen
        rope = pygame.Rect(0,558,800,5)
        pygame.draw.rect(gameDisplay,brown,rope)
        pygame.display.flip()
 
 
        
        block_starty += block_speed
        p = Player()
        p.player(x,y)
        blocks_dodged(dodged)
 
        #to calculate if the player goes out of bounds
        if x > display_width - player_width or x < 0:
            hit()
 
        if block_starty > display_height:
            block_starty = 0 - block_height
            block_startx = random.randrange(0,display_width)
            #to count up how many blocks dodged
            dodged += 1
            #make blocks fall faster
            block_speed += 1
            #make blocks bigger
            block_width += (dodged * 1.2)
 
#to calculate if a block hits a player 
        if y < block_starty+block_height:
 
            if x > block_startx and x < block_startx + block_width or x+player_width > block_startx and x + player_width < block_startx+block_width:

                hit()
        
        pygame.display.update()
        clock.tick(60)

#all the loops
start_menu()
game_loop()
pygame.quit()
quit()