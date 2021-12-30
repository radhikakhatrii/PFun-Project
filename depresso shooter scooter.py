import pygame
from pygame import mixer
from random import randint
from math import sqrt

#initializes pygame
pygame.init()

#screen size and background image
screen = pygame.display.set_mode((960, 540)) #creates the screen with the arguments passed as a tuple of (Width, Height)
background = background = pygame.image.load('images/classroom_habib.jpeg') #('Location of the background image')

#icon and title
icon = pygame.image.load('images/icon.png') #('icon location')
pygame.display.set_caption('depresso shooter scooter') #('Title of the game)
pygame.display.set_icon(icon) #display icon

#Background music
mixer.music.load('sounds/bg_music.mp3') #('file location')
mixer.music.play(-1) #-1 so it plays in a loop

#Player
class Player:
    def __init__(self): #To initlialise an object
        self.image = pygame.image.load('images/player.png')
        self.x = 480
        self.y = 465
        self.x_change = 0

    def draw(self): #draw method
        screen.blit(self.image, (self.x, self.y))

    def boundrycheck(self): #a check so the player doesnt mvove out of the boundry
        if self.x < 0:
            self.x = 0
        elif self.x > 736: #(Right side's y coordinate - player's size)
            self.x = 736

#Enemy
class Enemy:
    def __init__(self, image): #initialises every enemy object
        self.image = pygame.image.load(image) #loads the image
        self.x = randint(64, 896)
        self.y = randint(50,100)
        self.x_change = 0.5
        self.y_change = 40

    def draw(self): #draw method for the enemy objects
        screen.blit(self.image, (self.x, self.y))

    #speedy weedy function by radhika
    def newX(self, score): #returns a new speed with every increase in score
        if score >= 0 and score < 10:
            return 0.5
        elif score >= 10 and score < 20:
            return 0.65
        elif score >= 20 and score < 30:
            return 0.75
        elif score >= 40 and score < 50:
            return 0.9
        elif score >= 50 and score < 60:
            return 1.0
        elif score >= 60 and score < 70:
            return 1.1
        elif score >= 70 and score < 80:
            return 1.2
        elif score >= 80 and score < 90:
            return 1.3
        elif score >= 90 and score < 100:
            return 1.4
        else:
            return 1.5

    def over(self): #checks if the game is over
        if self.y > 440: #checks if the enemy has reached the bottom of the screen, if yes then
            for e in enemies:
                e.y = 2000 #remove all the enemies and place them at y=2000
            gameover.show() #show gameover text
            return True #returns a True for over whichll be used to break out of the enemy loop
        else:
            return False #returns False so the game runs as it should

#Bullet
class Tears:
    def __init__(self): #initialises the bullet/tears
        self.image = pygame.image.load('images/tear3.png') #loads tears image from its location
        self.x = 0
        self.y = player.y
        self.y_change = 5
        self.state = 'ready'  #ready = you cant see, fire = tear currently moving
        self.sound = mixer.Sound('sounds/laser.wav') #shooting sound

    def draw(self): #draws the tears/bullet
        self.state = 'fire' #sets it to fire so you cant shoot another bullet until it reaches the end or kill an enemy
        screen.blit(self.image, (self.x + 16, self.y + 10)) #16 and 10 added to centralise the tear

#Parent class for Text
class Text:
    def __init__(self, x, y, size, valtype): #initialises the text object with its given parameters
        self.value = 0
        self.font = pygame.font.Font('freesansbold.ttf', size) #font, size
        self.x = x
        self.y = y
        self.type = valtype
        self.text = ''

    def show(self): #draws text
        if self.type == 'score': #checks if the text type is score or gameover
            self.text = f'Score: {str(self.value)}' #if score, updates score
        if self.type == 'gameover': #if gameover
            self.text = "Hope you're feeling better now :)" #sets text to this
        text = self.font.render(self.text, True, (255, 255, 255)) #(r, g, b)
        screen.blit(text, (self.x, self.y)) #draw text with (x, y) co-ordinates

#Checks collision
def isCollision(enemyX, enemyY, bulletX, bulletY): #checks collision between bullet/teras and the enemy
    distance = sqrt(pow((enemyX - bulletX), 2) + pow((enemyY - bulletY), 2)) #calculates the distance between the enemy and the bullet/tears
    if distance < 35: #if the distance is less than 35, then returns a True for collison
        return True
    else:
        return False

#Player
player = Player() #Creates a player object of class Player

#Enemies #Creating objects of class Enemy
sel = Enemy('images/sel2.jpg')
d_grade = Enemy('images/d_grade.png')
plagiarism = Enemy('images/plagiarism.png')
canvas = Enemy('images/canvas3.png')
zoom = Enemy('images/zoom.png')
hackerrank = Enemy('images/hackerrank.png')
fail = Enemy('images/fail.png')
panopto = Enemy('images/panopto.png')
corona = Enemy('images/corona.png')
outlook = Enemy('images/outlook.png')
enemies = [d_grade, plagiarism, canvas, zoom, hackerrank, fail, sel, panopto, corona, outlook] #List of all the enemy objects

#Tears
tears = Tears() #object tears of class Tears

#Texts
score = Text(10, 10, 32, 'score') #x, y, size, type --- #object score of class Text
gameover = Text(80, 160, 50, 'gameover') #x, y, size, type -- #object gameover of class Text

#Game loop
running = True #Initialise with True to run the gamme
while running: #checks if game is still running
    screen.fill((45, 48, 51)) #draw a background of color (r, g, b)
    screen.blit(background, (0,0)) #draw background image

    #Check keystrokes
    for event in pygame.event.get(): #iterates through all the eventss in event.get()
        if event.type == pygame.QUIT: #Checks if the X button has been pressed on the window, if yes then
            running = False #sets running to False so the game breaks
        if event.type == pygame.KEYDOWN:  #if button pressed -- #check keystroke for Left or Right
            if event.key == pygame.K_LEFT: #if left key pressed then,
                player.x_change = -1.2 #move player 1.2 x units to the left
            if event.key == pygame.K_RIGHT: #if right key pressed then,
                player.x_change = 1.2 #move player 1.2 x units to the right
            if event.key == pygame.K_SPACE: #if space pressed then,
                if tears.state == 'ready': #check if the bullet is ready and not 'fire', if it's ready then
                    tears.x = player.x #set bullet's x coordinate to player's x coordinate
                    tears.sound.play() #play bullet shooting sound
                    tears.draw() #draw the bullet, which also sets the state to 'fire'
        if event.type == pygame.KEYUP: #if button released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #check if left or right key's released, if yes then
                player.x_change = 0 #set player's x_change to 0 back

    #Check player's boundries
    player.x += player.x_change
    player.boundrycheck() #Check for player boundry

    #enemy movement
    for enemy in enemies: #Iterates through every enemy in the enemies list
        #Game Over
        if enemy.over(): #checks if one of the enemy has reached the bottom, too close to the player, if yes then removes them all (refer to function)
            break #breaks out of the enemies loop

        #enemy movement
        enemy.x += enemy.x_change #add x units of change to the enemy's x
        if enemy.x < 0: #checks if the enemy has hit the left boundry, if yes then
            enemy.x_change = enemy.newX(score.value) #get new x_change from the speedy weedy function
            enemy.y += enemy.y_change #add y_change units y to the enemy's y
        elif enemy.x > 896: #checks if the enemy has hit the right boundry, if yes then
            enemy.x_change = -enemy.newX(score.value) #get new negative x_change from the speedy weedy function
            enemy.y += enemy.y_change #add y_change units y to the enemy's y

        #collision
        collision = isCollision(enemy.x, enemy.y, tears.x, tears.y) #returns a True/False for the collision between the enemy and the tears/bullet
        if collision == True: #if the tears killed the enemy then
            tears.y = player.y #set tear's y back to player's y
            tears.state = 'ready' #set the state back to 'ready' so the player can shoot the tears/bullet again
            score.value += 1 #add 1 to the score
            
            #draw the killed enemy back
            enemy.x = randint(64, 896)
            enemy.y = randint(50,100)

        enemy.draw() #draw each enemy

    #tears movement
    if tears.y <= 0: #checks if the tear has missed the enemy and reached the top boundry, if yes then
        tears.y = player.y #set tear's y back to player's y
        tears.state = 'ready' #set the state back to 'ready' so the player can shoot the tears/bullet again
 
    if tears.state == 'fire': #if the tear has been shot, then
        tears.draw() #draw the tear with decreasing y value
        tears.y -= tears.y_change #decreases y value of the tears with y_change units y

    player.draw() #draws player
    score.show() #draws score
    pygame.display.update() #updates display within the loop