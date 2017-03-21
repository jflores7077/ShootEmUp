'''
Jet Developers
Shoot-Em-Up
'''


from JDfile import *
import math

#Helps to look at start of debug
print('--Game Start--')

game = Game(800,600,'Shoot-Em-Up')

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

#Assign curMap a map object
curMap = Map(maps['level1'], game)

blk = blocks(curMap,game)
bullets = []
ld = Animation('SSimg\\Amenu.png',25,game,160/5,160/5,1)
ld.resizeTo(game.width-(game.width/3),game.height-(game.height/3))
ld.y = 220
crs = Image('SSimg\\crosshair.png',game)
bk = (0)
frame = 0
crs.resizeBy(-90)
bttn1 = bttn(game.width/2, -150,150,50,'start',game)
bttnss = []
for i in range(6):
    #bttn(200,300,50,50,'||',game)
    bttnss.append(bttn(100,150+i*75,50,50,'||',game))
    
#       y, acc
bttns = [game.height+150, 12.5]
breach = False
bty = 150
store = False
guys = [player(200,100,maps['level1'],bullets,game),
        guy(200,200,maps['level1'],bullets,-50,game),
        guy(400,250,maps['level1'],bullets,-50,game),
        guy(100,200,maps['level1'],bullets,-50,game)]
car = False
controls = Image('SSimg\\controls.png',game)
controls.resizeBy(-60)
controls.moveTo(game.width/2,game.height-170)

redy = Image('SSimg\\GET-READY.png',game)
redy.resizeBy(80)
redy.moveTo(game.width/2,70)

prices = [1, 1, 1, 1, 1, 1]
time = 3

powers = power(300,300, game)
while not game.over:
    game.processInput()
    frame +=1
    if str(state.st) == 'menu':
        game.clearBackground(bk)
        ld.draw()
        game.drawText('By Jet Developers',((game.width/2)-150),game.height-90,Font(black, 50, blue))
        if frame >= 20:
            #state.change('menu')
            ld.stop()
            if bttn1.y >= (game.height-(game.height/5)) and breach == False:
                bttns[0]-=bttns[1]
            else:
                breach = True
                
        bk = 0
        bttn1.y = bttns[0]
        if bttn1.draw():
            state.change('inst')
            frame = 0
    elif str(state.st) == 'inst':
        game.clearBackground((55))
        #game.drawText('Get Ready!', game.width/2-(230), 20, Font(black,150))
        #game.drawText(time, game.width/2-(time*60)/2, game.height/2-(time*60)/2, Font(black,120 + (time*90)))

        game.drawText('T opens Shop and G closes Shop',170,150,Font(white,40))
        game.drawText('Click or Hold Mouse To Shoot',190,200,Font(white,40))
        controls.draw()
        redy.draw()
        if frame >= 95:
            time-=1
            frame = 0
        if time <= 0:
            state.change('game')
        
    elif str(state.st) == 'game':
        curMap.render(blk,guys[0])
        pygame.display.set_caption('Shoot-Em-Up/Score:'+str(game.score))

        powers.display()
        if powers.touchedBy(guys):
            powers.img.moveTo(-20,-20)
            
        if store:
            game.clearBackground((25))
            game.drawText('SHOP',game.width/2-100,20, Font(white,100,blue))

            for i in enumerate(bttnss):
                
                if bttnss[i[0]].draw():
                    if i[0] == 0 and guys[0].coins >= prices[i[0]]:
                        guys[0].coins -= prices[i[0]]
                        guys[0].speed[2] += 0.5
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
                
            game.drawText('Speed:'+str(guys[0].speed[2]),200,130)

            game.drawText('Health:'+str(guys[0].hp),200,130+75)

            game.drawText('Max Mag Size:'+str(guys[0].b['max']),200,130+75*2)

            game.drawText('Reload Time:'+str(guys[0].b['rr']) ,200,130+75*3)

            game.drawText('Shoot Delay:'+str(guys[0].b['time']) ,200,130+75*4)

            game.drawText('Bullet Damage:'+str(guys[0].b['damage']) ,200,130+75*5)
        else:
            for mkay in guys:
                mkay.move(guys[0])
                
                if mkay.shot(bullets):
                    mkay.hp-=mkay.b['damage']
                
                
                if mkay.hp <=0:
                    guys.remove(mkay)
                    guys[0].coins += 2+randint(-1,2)
                    game.score += 1

            if len(guys)<=1:
                for i in range(5+randint(-2,2)):
                    guys.append(guy(-20+randint(-10,10), randint(0 , game.height), maps['level1'], bullets, -50,game))
                  
            for i in bullets:
                i.move()
                    
                if i.image.isOffScreen():
                    bullets.remove(i)

            #Lazy Workaround for death
            try:
                guys[0].key(state)
                
            except Exception: 
                state.st = 'lose'
            
        game.drawText('Health:'+str(guys[0].hp),10,30)
        game.drawText('Bullets:'+str(guys[0].b['left'])+ '/' +str(guys[0].b['max']),10,80)
        game.drawText('Coins:'+str(guys[0].coins),game.width-80,30)

        if keys.Pressed[K_t]:
            store = True
        if keys.Pressed[K_g]:
            store = False
            
    elif str(state.st) == 'lose':
        bk = (200)
        game.clearBackground(bk)
        game.drawText('Game Over',200,120, Font(black,120))
        game.drawText('Score:'+str(game.score),310,game.height/2,Font(white,50))
    game.update(60)
game.quit()
