from gamelib import *
arms = {
    'blank':{
            #Bullets left
            'left': 0,
            #maximum bullets per mag
            'max': 0,
            #time for next bullet shoot
            'time': 0,
            #time til next bulet shoot (keep 0)
            'rtime': 0,
            #time to reload finishes (keep 0)
            'reload': 0,
            #time til reload finishses
            'rr':500,

            'damage':5,

            
    },
    'pistol':{
            'left':3,
            'max':3,
            'time':50,
            'rtime':0,
            'reload':0,
            'rr':70,

            'damage':3,

            'acc': 10,
    },
    'pistol2':{
            'left':2,
            'max':2,
            'time':55,
            'rtime':0,
            'reload':0,
            'rr':75,
            'damage':1
    },

    'op':{
            'left':50,
            'max':155,
            'time':5,
            'rtime':0,
            'reload':0,
            'rr':100,

            'damage':3
    },
    'shotgun':{
            #Bullets le,ft
            'left': 5,
            #maximum bullets per mag
            'max': 5,
            #time for next bullet shoot
            'time': 0,
            #time til next bulet shoot (keep 0)
            'rtime': 0,
            #time to re,load finishes (keep 0)
            'reload': 0,
            #time til reload finishses
            'rr':100,

            'damage':5,
    }
}
class blocks(object):
    def __init__(self,a,game):
        self.game = game
        self.a = a
        self.blockType = {
            'grass':Image('SSimg\\Grass.png',self.game),
            'dirt': Image('SSimg\\dirt.png',self.game),
            'wood': Image('SSimg\\Wood.png',self.game),
            'brick': Image('SSimg\\Brick.jpg',self.game),
            'brown': Image('SSimg\\brown.png',self.game),
        }
        for i in self.blockType.keys():
            self.blockType[i].resizeTo(a.iw,a.ih)
            
class bullet(object):
    def __init__(self,player,game,shotBy):
        self.game = game
        self.player = player
        self.x,self.y = self.player.p.x,self.player.p.y
        self.rotate = self.player.rr-90
        #+randint(-self.player.b['acc'],-self.player.b['acc'])
        #max speed, angle
        self.speed = [25,0]
        self.shotBy = shotBy
        self.image = Image('SSimg\\bulletJF.png',self.game)
        self.image.rotateTo(self.rotate)
        self.image.moveTo(self.x+math.sin(self.rotate)*3,self.y+math.cos(self.rotate)*3)
        self.image.setSpeed(self.speed[0],self.rotate)

    def move(self):
        self.image.move()
        
class Map(object):
    def __init__(self,array,game):
        self.a = array
        self.game = game
        #Find the first ','. This will mark the width of string.
        self.w = len(self.a[0])

        #Count the ','. This will mark the 'height' of the string
        self.h = len(self.a)

        #x is the row which the image is in
        self.x = 0

        #Images width and heigh4 ***if strw < 5 else 4***
        self.iw = round(self.game.width/(self.w))
        self.ih = round(self.game.height/(self.h))
        self.x = 0,
        self.y = 0
        self.type = 'n/a'
        self.collided = False
        
    def render(self,blk,player):
        self.blk = blk
        self.p = player
        self.pa = player.p
        #Go through every letter in curMap and return (count, value)
        
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                self.x = (self.iw/2)+((self.iw) * j)
                self.y = (self.ih/2)+((self.ih) * i )
                
                if self.a[i][j] == 0:
                    self.blk.blockType['grass'].moveTo(self.x,self.y)
                    self.type = 'grass'

                    self.blk.blockType['grass'].draw()
                elif self.a[i][j] == 1:
                    self.blk.blockType['dirt'].moveTo(self.x,self.y)
                    self.type = 'dirt'
                    self.blk.blockType['dirt'].draw()
                    
                elif self.a[i][j] == 2:
                    self.blk.blockType['wood'].moveTo(self.x,self.y)
                    self.type = 'wood'
                    self.blk.blockType['wood'].draw()
                    
                elif self.a[i][j] == 3:
                    self.blk.blockType['brick'].moveTo(self.x,self.y)
                    self.blk.blockType['brick'].draw()
                    self.type = 'brick'
                    
                elif self.a[i][j] == 4:
                    self.blk.blockType['brown'].moveTo(self.x,self.y)
                    self.type = 'brown'
                    self.blk.blockType['brown'].draw()
                if self.p.x >=self.x-self.iw/2 and self.p.x<=self.x+self.iw/2 and self.p.y>=self.y-self.ih/2 and self.p.y<=self.y+self.ih/2:
                    self.collided = True
                else:
                    self.collided = False
        
class State(object):
    def __init__(self,start):
        self.strt= str(start)
        self.st = self.strt
    def change(self,s):
        self.s = str(s)
        self.st = self.s
    def eq(self,EqTo):
        self.eq = str(EqTo)
        if str(self.st) == EqTo:
            return True
        else:
            return False
    def get(self):
        return self.state
    
class player(object):
    def __init__(self,x,y,a,ba,game):
        self.x = x
        self.y = y
        self.game = game
        self.canShoot = True
        self.bullets = ba
        self.type = 'player'
        #             x,y,max,dec
        self.speed = [0,0,2.5,0.6]
        self.coins = 5
        self.hp = 100 
        self.r = 0
        self.a = a
        self.tr = ["0102910010221001"]
        self.pew = Sound('Audio//pew_JD.wav',1)
        self.w = len(self.a[0])*3.5
        self.h = len(self.a)*3.5
        self.max = 3
        self.vel = 0.2
        self.b = arms['pistol']
        self.p = Animation('SSimg\\playerEJD.png',3,self.game,48/3,20,12)
        self.p.stop()
        self.p.resizeTo(self.w,self.h)
        self.rr = self.p.rotate_angle * 180 / math.pi
        #           right, left, down, up
        self.col = [False,False,False,False]
    def move(self, k = 0):
        self.rr = self.p.rotate_angle * 180 / math.pi
        self.tr = self.speed
        
        self.y+=self.speed[1]
        self.x+=self.speed[0]
        self.p.moveTo(self.x,self.y)
        self.p.rotateTowards(mouse)
        
    def shot(self,bArray):
        self.ba = bArray
        
        for BU_i in self.ba:
            if BU_i.image.collidedWith(self.p) and BU_i.shotBy != 'player':
                return True
            
    def key(self, lmao):
        if keys.Pressed[K_UP] or keys.Pressed[K_w]:
            self.speed[1]=-self.speed[2]
            self.p.play()
        elif keys.Pressed[K_DOWN] or keys.Pressed[K_s]:
            self.speed[1]=self.speed[2]
            self.p.play()
        else:
            self.speed[1] *= self.speed[3]
            self.p.stop()
            
        if keys.Pressed[K_LEFT] or keys.Pressed[K_a]:
            self.speed[0]=-self.speed[2]
        elif keys.Pressed[K_RIGHT] or keys.Pressed[K_d]:
            self.speed[0]=self.speed[2]
        else:
            self.speed[0] *= self.speed[3]

        #Bullets
        if keys.Pressed[K_SPACE] and self.canShoot or mouse.LeftButton and self.canShoot:
            self.canShoot = False
            
        #Keep increasing rtime
        self.b['rtime']+=1
        
        if self.canShoot == False:
            #if rtime has reached its max time, reset it
            if self.b['rtime'] >= self.b['time'] :
                self.b['rtime'] = 0
                self.canShoot = True

            #if any bul,lets are left and rtime is 0, then add a bullet to the array
            if  self.b['left'] > 0 and self.b['rtime'] == 0 and self.canShoot:
                self.bullets.append(bullet(self,self.game,'player'))
                self.pew.play()
                #subtract one bullet
                self.b['left']-=1
                self.canShoot = True
        '''
        else:
            self.canShoot = True
        '''

        #if no more bul,lets leftdw
        if self.b['left'] <= 0:
            self.b['reload'] += 1
            if self.b['reload'] >= self.b['rr']:
                self.b['reload'] = 0
                self.b['left'] = self.b['max']
    def explode(self):
        print(2)
class guy(object):
    def __init__(self,x,y,a,ba,dist,game):
        self.x = x
        self.y = y
        self.dist = dist
        self.coins = 0
        self.game = game
        self.bullets = ba
        self.expl = False
        #self.explosion = Animation('SSimg\\explode.jpg', 12, self.game, 600/3, 538/4, 5)
        #             x,y,max,dec
        self.speed = [0,0,2.5,0.6]
        self.pew = Sound('Audio\\pew_JD.wav',2)
        #Rotate
        self.r = 0
        self.a = a
        self.tr = ["0102910010221001"]
        self.w = len(self.a[0])*3.5
        self.h = len(self.a)*3.5
        self.max = 3+randint(-1,2)
        self.vel = 0.2
        self.pb = arms['pistol2']
        self.b = self.pb
        self.p = Animation('SSimg\\guyEJD.png',3,self.game,48/3,20,12)
        self.p.moveTo(self.x,self.y)
        self.p.stop(),
        self.p.resizeTo(self.w,self.h)
        self.rr = self.p.rotate_angle * 180 / math.pi
        self.follow = False
        self.shoot = False
        self.hp = 2 + randint(-1, 5)
    def shot(self,bArray):
        self.ba = bArray
        
        for BU_i in self.ba:
            if BU_i.image.collidedWith(self.p) and BU_i.shotBy != 'enemy':
                #self.ba.remove(BU_i)
                return True
            
            
    def move(self,p1):
        self.rr = self.p.rotate_angle * 180 / math.pi
        self.tr = self.speed

        self.p1 = p1
        
        self.p.rotateTowards(p1)

        self.p.draw()
        
        if sqrt( (self.p1.x  - self.p.x)**2 + (self.p1.y - self.p.y)**2 ) >= 195+self.dist:
            self.follow = True
            self.shoot = True,
        else:
            self.follow = False
            
        if self.follow:
            self.p.moveTowards(self.p1.p,self.max)
            self.p.play()
        else:
            self.p.draw()
            self.p.frame = 0
            self.p.stop()
            
        if self.shoot:
            #if rtime has reached its max time, reset it
            if self.b['rtime'] >= self.b['time']:
                self.b['rtime'] = 0
            else:
                #Keep increasing rtime
                self.b['rtime']+=1
            

            #if any bullets are left and rtime is 0, then add a bullet to the array
            if  self.b['left'] > 0 and self.b['rtime'] == 0:
                self.bullets.append(bullet(self,self.game,'enemy'))
                #subtract one bullet
                self.b['left']-=1
                self.pew.play()
        else:
            self.b['rtime'] = 0

        if self.b['left'] <= 0:
            self.b['reload'] += 1
            if self.b['reload'] >= self.b['rr']:
                self.b['reload'] = 0
                self.b['left'] = self.b['max']
                
        #self.explosion.moveTo(self.x,self.y)
    def explode(self):
        self.explosion.draw()
        self.shoot = False
        

class power(object):
    def __init__(self, x, y, game):
        self.x = x
        self.y = y

        self.game = game
        
        self.type = 'ayye'
        self.rand = randint(1, 3)
        
        if self.rand == 1:
            self.type = 'delay'
            
        elif self.rand == 2:
            self.type = 'coin'
            
        elif self.rand == 3:
            self.type = 'speed'
            
        '''  
        else:
            self.type = 'bomb'
        '''
    
        #self.type = 'delay'
        self.img = Image('SSimg\\'+self.type+'.png',self.game)
        self.img.resizeBy(randint(70,85))
        self.frame = 0
        self.touchAudio = 0
        self.touched = False
        self.timeTil = randint(40,150)
    def display(self):
        self.frame+=1
        
        if self.touched == False:
            self.img.moveTo(self.x+math.sin(self.frame*0.05)*20,self.y+math.cos(self.frame*0.02)*20)
            self.img.draw()
        else:
            if self.frame >= self.timeTil:
                self.touched = False
                self.x = randint(10, self.game.width-20)
                self.y = randint(10, self.game.height-20)
                
                if self.rand == 1:
                    self.type = 'delay'
                    
                elif self.rand == 2:
                    self.type = 'coin'
                    
                elif self.rand == 3:
                    self.type = 'speed'
                """
                elif self.rand == 4:
                    self.type = 'bomb'
                """
                self.img = Image('SSimg\\'+self.type+'.png',self.game)
                self.img.resizeBy(randint(70,85))
                
    def touchedBy(self, player):
        self.ar = player
        self.p1 = player[0]
        self.p = self.img
        
        if sqrt( (self.p1.x  - self.p.x)**2 + (self.p1.y - self.p.y)**2 ) <= 20:
            self.touched = True
            self.timeTil = randint(250,500)
            self.frame = 0
            self.rand = randint(1, 5)
            
            if self.type == 'coin':
                self.p1.coins+=randint(15,55)
                
            if self.type == 'speed':
                self.p1.speed[2]+=1.25

            if self.type == 'delay':
                self.p1.b['time'] -= 1
            """
            if self.type == 'bomb':
                self.p1.coins+=randint(5,10)
                for i in self.ar:
                    i.explode()
            """
            return True

class bttn(Image):
    def __init__(self,x,y,w,h,txt,game):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = 0
        self.txt = txt
        self.g = game
        self.start = False
        if self.txt == 'start':
            self.btn = Image('SSimg\\startBttn.png',self.g)
            
        else:
            self.btn = Image('SSimg\\button-A.png',self.g)
        self.btn.resizeTo(self.w,self.h)
            
        self.d = -3
        self.sx = self.x + self.d
        self.sy = self.y - self.d
        self.over = False
        self.click = False
        self.t = 0
        self.t2 = 0
    def draw(self):
        self.btn.draw()
        self.btn.moveTo(self.x,self.y)

        if mouse.x >=self.x-self.w/2 and mouse.x<=self.x+self.w/2 and mouse.y>=self.y-self.h/2 and mouse.y<=self.y+self.h/2:
            self.over = True
                
            if mouse.LeftButton:
                self.click = True
            else:
                self.click = False
        else:
            
            self.over = False
        if self.click and self.t2 == 0:
            self.t2+=1
            #If the user clicks the button
            return True
        elif self.t2 > 0 and self.click == False:
            self.t2 = 0
            #Once the user has finished clicking
            return False
        if self.over:
            self.t+=1
            self.x = self.sx
            self.y = self.sy

            #If the user is over the button
            
        elif self.t > 0 and self.over == False:
            self.x = self.sx-self.d
            self.y = self.sy+self.d
            self.t = 0
            #Once the user is not over the button
            
        
        
