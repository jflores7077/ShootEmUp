'''
Jet Developers
Shoot-Em-Up
'''

#Import our function file and math library
from JDfile import *
import math

#Helps to look at start of debug
print('--Game Start--')

#Create game
game = Game(800,600,'Shoot-Em-Up')

#A dictionary of maps, no purpose now.
'''
0 = grass
1 = dirt
2 = wood
3 = brick
4 = Brown Block
'''
maps = {
    'level1':[[0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0]],
}

#Current State
state = State('menu')

#Assign curMap a map array
curMap = Map(maps['level1'], game)

#Define the block that can be used
blk = blocks(curMap,game)

#Create a array to hold bullets
bullets = []

#Logo Animation at begining
ld = Animation('SSimg\\Amenu.png',25,game,160/5,160/5,1)
ld.resizeTo(game.width-(game.width/3),game.height-(game.height/3))
ld.y = 220

#Crosshair image
crs = Image('SSimg\\crosshair.png',game)

#Background color
bk = (0)

#Current Frame
frame = 0

crs.resizeBy(-90)

#Create a new button called bttn1
bttn1 = bttn(game.width/2, -150,150,50,'start',game)

#A array to hold buttons
bttnss = []

#Add 6 buttons, and each being 75 pixels away from each other
for i in range(6):
    #bttn(200,300,50,50,'||',game)
    bttnss.append(bttn(100,150+i*75,50,50,'||',game))

#Movement for button animation at beginning
#       y, acc
bttns = [game.height+150, 12.5]

#Is the animation complete?
breach = False
bty = 150

#Is the store open?
store = False

#Array of people, including enemies and the player
#The player will *always* be guys[0]
guys = [player(200,100,maps['level1'],bullets,game),
        guy(200,200,maps['level1'],bullets,-50,game),
        guy(400,250,maps['level1'],bullets,-50,game),
        guy(100,200,maps['level1'],bullets,-50,game)]

#Is guys[0] a car
car = False

#Control image
controls = Image('SSimg\\controls.png',game)
controls.resizeBy(-60)
controls.moveTo(game.width/2,game.height-170)

#Get ready font
redy = Image('SSimg\\GET-READY.png',game)
redy.resizeBy(80)
redy.moveTo(game.width/2,70)

#Prices for the shop
prices = [1, 1, 1, 1, 1, 1]

#Time until game changes from instructions to game
time = 3

#Power object
powers = power(300,300, game)

#Menu
menu = Menu(game)

#Add menu animation
a_menu = move()

#Game loop
while not game.over:
    game.processInput()
    menu.display()
    
    #Add 1 to frame until game.over is false
    frame +=1
    
    #If state.st is equal to menu
    if str(state.st) == 'menu':

        #Display the menu, and if the button is pressed, show the instruction menu
        if menu.display():
            #Change the game state to the intruction page
            state.change('inst')
            menu.frame = 0
        
        a_menu.start(menu)

    #If the state is inst display the instructions
    elif str(state.st) == 'inst':
        game.clearBackground((55))
        #game.drawText('Get Ready!', game.width/2-(230), 20, Font(black,150))
        #game.drawText(time, game.width/2-(time*60)/2, game.height/2-(time*60)/2, Font(black,120 + (time*90)))

        game.drawText('T opens Shop and G closes Shop',170,150,Font(white,40))
        game.drawText('Click or Hold Mouse To Shoot',190,200,Font(white,40))
        controls.draw()
        redy.draw()
        
        #Automatically change the state to game
        if frame >= 95:
            time-=1
            frame = 0
        if time <= 0:
            state.change('game')
    #If state is game
    elif str(state.st) == 'game':
        #Renders a background from the 2d array
        curMap.render(blk,guys[0])
        #Change the games caption
        pygame.display.set_caption('Shoot-Em-Up/Score:'+str(game.score))

        #Show the powers
        powers.display()
        #if powers collides with guys[0]
        if powers.touchedBy(guys):
            #Move the image to -20,-20)
            powers.img.moveTo(-20,-20)
        
        #If the store is open
        if store:
            game.clearBackground((25))
            game.drawText('SHOP',game.width/2-100,20, Font(white,100,blue))
            
            #Enumerate bttnss, returns (times i was reapted, value of i)
            for i in enumerate(bttnss):
                
                #Draw the bttnss, check for mouse collision and check if mouse clicked on the button (all in one line ;^)))
                if bttnss[i[0]].draw():
                    #If i[0] is x and the player has enough coins
                    if i[0] == 0 and guys[0].coins >= prices[i[0]]:
                        #give the player _____ and remove prices[i[0]] from the players coins
                        guys[0].coins -= prices[i[0]]
                        guys[0].speed[2] += 0.5
                        
                        #Add 2 to the price
                        prices[i[0]]+=2
                        
                    if i[0] == 1 and guys[0].coins >= prices[i[0]]:
                        guys[0].coins -= prices[i[0]]
                        guys[0].hp += 4
                        prices[i[0]]+=2
                        
                    if i[0] == 2 and guys[0].coins >= prices[i[0]]:
                        guys[0].coins -= prices[i[0]]
                        guys[0].b['max'] += 1
                        prices[i[0]]+=2
                        
                    if i[0] == 3 and guys[0].coins >= prices[i[0]]:
                        guys[0].coins -= prices[i[0]]
                        guys[0].b['rr'] -= 0.5
                        prices[i[0]]+=2
                        
                    if i[0] == 4 and guys[0].coins >= prices[i[0]]:
                        guys[0].coins -= prices[i[0]]
                        guys[0].b['time'] -= 0.5
                        prices[i[0]]+=2
                        
                    if i[0] == 5 and guys[0].coins >= prices[i[0]]:
                        guys[0].coins -= prices[i[0]]
                        guys[0].b['damage'] += 1
                        prices[i[0]]+=2
                        
            for i in enumerate(prices):
                game.drawText('Price:'+str(prices[i[0]]),200,150+75*i[0])
            #Another easier way to do this(but, im assuming takes more ram) is to create a array of strings and loop through the array
            game.drawText('Speed:'+str(guys[0].speed[2]),200,130)
            game.drawText('Health:'+str(guys[0].hp),200,130+75)
            game.drawText('Max Mag Size:'+str(guys[0].b['max']),200,130+75*2)
            game.drawText('Reload Time:'+str(guys[0].b['rr']) ,200,130+75*3)
            game.drawText('Shoot Delay:'+str(guys[0].b['time']) ,200,130+75*4)
            game.drawText('Bullet Damage:'+str(guys[0].b['damage']) ,200,130+75*5)
        #If the store is closed   
        else:
            #Draw all the people
            for mkay in guys:
                mkay.move(guys[0])
                
                #If someone got hit
                if mkay.shot(bullets):
                    #Hurt that player
                    mkay.hp-=mkay.b['damage']
                
                #If a player has less than 0 hp
                if mkay.hp <=0:
                    #Remove them from the game and give the player coins and score
                    guys.remove(mkay)
                    guys[0].coins += 2+randint(-1,2)
                    game.score += 1
            
            #If the length of array guys if less than or equal to 1
            if len(guys)<=1:
                #Spawn more enemies
                for i in range(5+randint(-2,2)):
                    guys.append(guy(-20+randint(-10,10), randint(0 , game.height), maps['level1'], bullets, -50,game))
            
            #draw the bullets
            for i in bullets:
                i.move()
                
                #To run the game faster, remove any bullets outside the screen
                if i.image.isOffScreen():
                    bullets.remove(i)

            #Lazy Workaround for guys[0]'s death
            #Try doins guys[0].key(state)
            try:
                guys[0].key(state)
            #If you get an error back, make state to lose screen
            except Exception: 
                state.st = 'lose'
        #Display information for the player 
        game.drawText('Health:'+str(guys[0].hp),10,30)
        game.drawText('Bullets:'+str(guys[0].b['left'])+ '/' +str(guys[0].b['max']),10,80)
        game.drawText('Coins:'+str(guys[0].coins),game.width-80,30)
        
        #Lazy keys to open and close store
        if keys.Pressed[K_t]:
            store = True
        if keys.Pressed[K_g]:
            store = False
    #If state is lose
    elif str(state.st) == 'lose':
        #Lazy lose state
        bk = (200)
        game.clearBackground(bk)
        game.drawText('Game Over',200,120, Font(black,120))
        game.drawText('Score:'+str(game.score),310,game.height/2,Font(white,50))
    game.update(60)
game.quit()
#ded
