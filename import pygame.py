import pygame
from pygame.locals import *
import random, math, sys, time
pygame.init()
Surface = pygame.display.set_mode((800,600), pygame.FULLSCREEN)
global color
blue =  (0,0,150)
red = (150,0,0)
yellow = (255,255,0)
white = (255,255,255)
green = (0,128,0)

color = blue

global triggered
triggered = 1002

Circles = []
ECircles = [] 
Tcircles = []
ML = []
MR = []
sqrt = math.sqrt

for x in range(0,399): #This covers the x and y trajectory for the leftward magnetic field
    HalfCircleYLeft = (math.sqrt(200**2-(int(x)-200)**2)+50)#(math.sqrt(500^2-(((x-200))^2)))+50
    ML.append(HalfCircleYLeft)
for x in range(400,800):
    HalfCircleY_Right = (math.sqrt(200**2-(int(x)-600)**2)+50)
    MR.append(HalfCircleY_Right)



class Circle:
    def __init__(self): #Setting up paraameters for blue circles
        self.radius = 10
        self.x = random.randint(self.radius, 800-self.radius)
        self.y = random.randint(50+self.radius, 550-self.radius) #100 in the rand int so ball doesnt get stuck in the red bar, making a shower of red balls
        self.speedx = 0.5*(random.random()+1.0)+3
        self.speedy = 0.5*(random.random()+1.0)+3
        self.numCol = 0
        self.triggered = 1002
        self.add = 0
class ECircle:
    def __init__(self): #Setting up parameters for white dots/electrons
        self.radius = 2
        done = True
        x = 0
       
        while done:
            x = random.randint(102, 698)
            if x > 502 or x < 298:
                done = False
        #self.x = x
        #self.y = random.randint(52, 73) #100 in the rand int so ball doesnt get stuck in the red bar, making a shower of red balls
        self.x = random.randint(self.radius, 800-self.radius)
        self.y = random.randint(50+self.radius, 550-self.radius) 
        self.speedx = 0.5*(random.random()+1.0)
        self.speedy = 0.5*(random.random()+1.0)
    def drawE(self):
        #This draws the ECircles/electrons       
        pygame.draw.circle(Surface,white,(int(self.x),int(self.y)),self.radius) #draws individual blue circles
class Tcircle:
    def __init__(self):
        self.radius = 5
        #self.x = random.randint(self.radius, 800-self.radius)
        self.x = (lastTop) #this makes it so that it spawns in at the exact point hwere the ball hit
        self.y = 50 #50 for spawn at bottom of red bar
        self.speedx = 0 #no horizontal movement 
        self.speedy = 0.5 #set movement speed, helpful for no midair grouping
    def drawT(self):
        pygame.draw.circle(Surface,red,(int(self.x),int(self.y)),self.radius) #draws individual red circles

for x in range(20):
    ECircles.append(ECircle())

for x in range(20):
    Circles.append(Circle())

def main():
    #An infinite loop
    while True:
        #first check if you hit esc
        GetInput()
        #changes the position of the ball via incrementing
        Move()
        #is it going to collide with anything?
        CollisionDetect()
        #draw the balls
        Draw()
      
def addECircle(r,x,y,sX,sY,Circle):
     #creates a box around the atom
    leftX = Circle.x - Circle.radius+2        #     downY
    rightX = Circle.x + Circle.radius+2       #       .
    upY = Circle.y - Circle.radius+2          #leftX.....RightX
    downY = Circle.y + Circle.radius+2        #       .
    startingIncrement = 10                    #      upY
    #make an electron
    ball = ECircle()
    ball.radius = r
    ball.x = x+startingIncrement
    ball.y = y+startingIncrement

    #finishing up our decleration of the electron
    ball.speedx = sX
    ball.speedy = sY
    #adding to list of electrons
    ECircles.append(ball)


def deleteECircle(ball):
    temp=ball
    ECircles.remove(temp)


def CircleCollide(C1,C2): #interactions between blue balls
    C1Speed = math.sqrt((C1.speedx**2)+(C1.speedy**2))
    XDiff = -(C1.x-C2.x)
    YDiff = -(C1.y-C2.y)
    if XDiff > 0:
        if YDiff > 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff < 0:
        if YDiff > 0:
            Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff == 0:
        if YDiff > 0:
            Angle = -90
        else:
            Angle = 90
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    elif YDiff == 0:
        if XDiff < 0:
            Angle = 0
        else:
            Angle = 180
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    C1.speedx = XSpeed
    C1.speedy = YSpeed

def checkInArray(x,list):
    bol = False
    for y in list:
        if x==y:
            bol = True
    return bol
def Move(): #circles move
    factor = 0
    for Circle in Circles:
        if Circle.numCol % 2 == 0:
            factor = 5
        else:
            factor = 0
        Circle.x += Circle.speedx
        Circle.y += Circle.speedy
    for ECircle in ECircles:

        if ECircle.x in range(0,399):    
            if checkInArray(ECircle.y,ML):
                for x in range(0,399):
                #ECircle.speedx = 1
                #ECircle.speedy = (ECircle.x-600)/math.sqrt(100^2-(ECircle.x-600)^2)  #(x-a)/sqrt(r^2-(x-a)^2)=(dy)/(dx)
                    ECircle.x = int(x)
                    ECircle.y = ML[x]
        
        if ECircle.x in range(400,800):   
            if checkInArray(ECircle.y,MR):
                for x in range(400,800):
                    #ECircle.speedx = 1
                    #ECircle.speedy = (ECircle.x-600)/math.sqrt(100^2-(ECircle.x-600)^2)  #(x-a)/sqrt(r^2-(x-a)^2)=(dy)/(dx)
                    #ECircle.x += ECircle.speedx
                    #ECircle.y += ECircle.speedy
                    ECircle.x = int(x)
                    ECircle.y = MR[(x-400)] 
                    break 
        else:
            ECircle.x += ECircle.speedx
            ECircle.y += ECircle.speedy

    for Tcircle in Tcircles: #Red circles stop when they hit the green target
        Tcircle.y += Tcircle.speedy
        if Tcircle.y >= 550:
            Tcircle.speedy = 0
        for Tcircle2 in Tcircles:
            if Tcircle != Tcircle2:
                if math.sqrt(((Tcircle.x-Tcircle2.x)**2)+((Tcircle.y-Tcircle2.y)**2)) <= (Tcircle.radius+Tcircle2.radius):
                    Tcircle.speedy = 0
def CollisionDetect(): #turns balls around
    global lastTop
    for Circle in Circles:
        if Circle.x < Circle.radius or Circle.x > 800-Circle.radius:
            Circle.speedx *= -1 
        if Circle.y < Circle.radius+50: 
            if Circle.numCol % 2 != 0:
                lastTop = int(Circle.x) #lastTop is changed
                Circle.speedx = 0
                Circle.speedy = 0
                if Circle.add == 0:          
                    Tcircles.append(Tcircle())#adds another circle
                    Circle.add = 1 
            Circle.speedy *= -1    
        if Circle.y > 550-Circle.radius:
            Circle.speedy *= -1
    
    for ECircle in ECircles:
        if ECircle.x < ECircle.radius or ECircle.x > 800-ECircle.radius:
            ECircle.speedx *= -1 
        if ECircle.y < ECircle.radius+50: #red rectangle is hit
            ECircle.speedy *= -1
        if ECircle.y > 550-ECircle.radius:
            ECircle.speedy *= -1
   
    for Circle in Circles:
        for Circle2 in Circles:
            if Circle != Circle2:
                if Circle.add == 1 and Circle2.add == 1:  
                    if math.sqrt(((Circle.x-Circle2.x)**2)+((Circle.y-Circle2.y)**2)) <= (Circle.radius+Circle2.radius):
                        Circle2.speedy = 0
                        Circle2.speedx = 0
                else: 
                    if math.sqrt(((Circle.x-Circle2.x)**2)+((Circle.y-Circle2.y)**2)) <= (Circle.radius+Circle2.radius):
                            CircleCollide(Circle,Circle2)
    
    
    
    for ECircle in ECircles:     
        for ECircle2 in ECircles:

            if ECircle != ECircle2:
                if math.sqrt(((ECircle.x-ECircle2.x)**2)+((ECircle.y-ECircle2.y)**2)) <= (ECircle.radius+ECircle2.radius):
                    CircleCollide(ECircle,ECircle2)
    
    for Circle in Circles:
        for ECircle in ECircles:
            if math.sqrt(((Circle.x-ECircle.x)**2)+((Circle.y-ECircle.y)**2)) <= (Circle.radius+ECircle.radius):
                CircleCollide(ECircle,Circle)
                CircleCollide(Circle,ECircle)
                if Circle.numCol % 2 == 0:
                    addECircle(ECircle.radius, ECircle.x, ECircle.y, ECircle.speedx, ECircle.speedy, Circle)
                    Circle.speedy = -2.5
                else:
                    deleteECircle(ECircle)
                    if Circle.add == 1:
                        Circle.y += 2
                        Circle.speedx = 0.5*(random.random()+1.0)
                        Circle.speedy = 0.5*(random.random()+1.0)
                        Circle.add = 0
                Circle.numCol = Circle.numCol + 1
                Circle.triggered = 0 

def Draw():
    factor = 1
    Surface.fill((0,0,0))
    pygame.draw.rect(Surface, (150,0,0), (0, 0, 800, 50)) #draws red bar
    pygame.draw.rect(Surface, (0,150,0), (0,550, 800, 50)) #draws green bar
    #pygame.draw.rect(Surface, green, (100,50, 200, 75)) #draws yellow bar
    #pygame.draw.rect(Surface, green, (500,50, 200, 75)) #draws yellow bar
    for x in range(0,398):
        pygame.draw.line(Surface,white,(x, ML[x]), (x+1, ML[x+1]), 3)
    for x in range(400,799):
        pygame.draw.line(Surface,white,(x, MR[(x-400)]), (x+1, MR[(x-400)+1]), 3)

    for Circle in Circles:
        if Circle.numCol % 2 == 0:
            if Circle.triggered < 4:
                Circle.triggered += 1
                color = white 
            else:
                color = blue
        else:
            color = yellow
            
        #print (color)
        pygame.draw.circle(Surface,color,(int(Circle.x),int(Circle.y)),Circle.radius) #draws individual blue circles
        factor = 0

    for ECircle in ECircles:
        ECircle.drawE()
    for Tcircle in Tcircles:
        Tcircle.drawT()
    pygame.display.flip()
def GetInput():
    #checking for pressed keys
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        #if you hit esc...
        if event.type == QUIT or keystate[K_ESCAPE]: #if Esc is pressed, quit window
            #quit program
            pygame.quit(); sys.exit()
        #if you hit "u", everyting speeds up
        if keystate[K_u]:
            for ECircle in ECircles:
                ECircle.speedx += 2
                ECircle.speedy += 2
            for Circle in Circles:
                Circle.speedx += 2
                Circle.speedy += 2



if __name__ == '__main__': main() 