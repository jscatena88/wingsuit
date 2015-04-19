import pygame
import Queue
import random
import math
import collections 

#GLOBALS
PLAYER_SIZE=35
SCREENSIZE = (1024,768)
WIDTH,HEIGHT=SCREENSIZE
GRAY= (96,96,96)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (150,204,204)
SCROLLSPEED= 5

#### LEVEL CLASS
class Level(): 
    def __init__(self, x, y, height, envheight): #screensize x, screensize y, distance between roof and floor, height of envelope
        self.x=int(math.sqrt(x*x+y*y)) #sqrt of width^2 +height^2
        print self.x
        self.y=self.x
        self.height=height
        self.envheight=envheight
        self.roofy= y/2+height/2 #y coordinate of roof 
        self.floory= y/2-height/2#y coordinate of floor
        self.ydir=1
        self.q=collections.deque()
        self.bigdisplay=pygame.Surface((self.x,self.y))
        self.oldy=y/2 # start generating from the middle of the map        
        self.rotatedScreen = pygame.Surface((1,1))
        for x in range(0, self.x):
            newy=self.getnexty()
            self.q.append(newy)#enque
            self.oldy=newy
        

    def getnexty(self):
        if random.randint(0,50)==25:
            self.ydir*=-1

        #if envelope butts up against roof
        if self.oldy>= self.roofy-self.envheight and self.ydir==1:
            self.ydir= -1

        #if envelope butts up against floor
        if self.oldy<= self.floory+self.envheight and self.ydir==-1:
            self.ydir=1
        return self.oldy + random.randint(0,2) *self.ydir
        

    def draw(self):
        self.bigdisplay.fill(BLUE)
        x=0
        # loop through q and x 
        for element in self.q:
            if x in range (0,self.x):
                #constructs two lines for every x value to make curves
                rand=random.randint(1,20)
                pygame.draw.line(self.bigdisplay, GRAY, (x, 0), (x, (element-self.envheight)))
                self.bigdisplay.set_at((x, element-self.envheight), BLACK)
                pygame.draw.line(self.bigdisplay, GRAY, (x, self.x), (x, element+self.envheight))
                self.bigdisplay.set_at((x, element+self.envheight), BLACK)
                x+=1
        self.rotatedScreen=pygame.transform.rotate(self.bigdisplay,-45)#.convert(),-45)
        return self.rotatedScreen

    #loops through top "shift" elements in q and pops them and appends new ones
    def generate(self, shift):
        for x in range(0,shift):
            self.q.popleft()#dequeue
            newy=self.getnexty()
            self.q.append(newy)#enqueue
            self.oldy=newy


    def collision(self, (x,y),surface):
        for i in range (x,x+PLAYER_SIZE):
            if surface.get_at((i, y))==GRAY or surface.get_at((i, y))==BLACK:
                return True
        for i in range (x,x+PLAYER_SIZE):
            if surface.get_at((i, y+PLAYER_SIZE))==GRAY or surface.get_at((i, y+PLAYER_SIZE))==BLACK:
                return True
        return False
          
            
        
#### END LEVEL CLASS


class Player(pygame.sprite.Sprite):
    """ Class for the player's character """
    
    def __init__(self, xPos, yPos):
        """ Constructor """

        #call parent constructor
        super(Player, self).__init__()

        #At some point make this an image not a square...
        width= height = PLAYER_SIZE
        self.levelimage = pygame.image.load("images/wingsuit.png").convert()
        self.levelimage.set_colorkey(WHITE)
        self.upimage = pygame.image.load("images/wingsuitup.png").convert()
        self.upimage.set_colorkey(WHITE)
        self.downimage = pygame.image.load("images/wingsuitdown.png").convert()
        self.downimage.set_colorkey(WHITE)
        self.image = self.levelimage

        #define rect for collision and such
        self.rect = self.image.get_rect()

        #Physics Vars
        self.velocity_y = 2
        self.direction = 0
        self.ANGLE_MAX = 130
        self.energy = 0
        self.rampUp = 0.0
        
        #Drawing vars
        self.xPos = xPos
        self.yPos = yPos


    def draw(self, screen, yVelocity):
        #print yVelocity + self.velocity_y
        self.yPos += yVelocity + self.velocity_y
        #print 'yPos:{0}'.format(self.yPos)
        self.rect.x = self.xPos
        self.rect.y = self.yPos
        screen.blit(self.image, self.rect)
        #pygame.draw.line(screen,RED, (self.rect.x+20, self.rect.y+20), (20+self.rect.x + 150*math.sin(math.radians(self.angle)), 20+self.rect.y+150*math.cos(math.radians(self.angle))), 3)

    def update(self,direction):
        self.direction = direction
        self.calc_physics()
        print 'In update: {0},{1}'.format(self.xPos, self.yPos + self.velocity_y)
        return (self.xPos, self.yPos + self.velocity_y)
        

    def calc_physics(self):
        if self.direction == 1:
            self.rampUp += .65
            self.velocity_y = self.rampUp
            if self.energy < 300:
                self.energy += self.velocity_y
            self.image = self.downimage
        elif self.direction == -1:
            self.rampUp = 0
            self.velocity_y = -.09*self.energy
            self.energy *= .935
            if self.energy < 2:
                self.energy = 2
            self.image = self.upimage
        else:
            if self.energy < 2:
                self.energy = 2
            else:
                self.energy *= .98
            self.rampUp = 0
            self.velocity_y = 0
            self.image = self.levelimage
        #print self.energy
    
    
            


    
def main():
    pygame.init()
    #initialize screen surface
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Wingsuit!")
    mylevel=Level(WIDTH, HEIGHT, 650, 175)
    #loop until player closes
    running = True

    #Manage screen updates
    clock = pygame.time.Clock()
    
    player = Player(412,270)

    #----- Main Game Loop-----
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        key = pygame.key.get_pressed()
        angle = 0
        if key[pygame.K_UP]:
            angle = -1
        elif key[pygame.K_DOWN]:
            angle = 1
        playerX, playerY = player.update(angle)
        print playerY
        playerxy= int(playerX), int(playerY)

        # Limit to 60 frames per second
        clock.tick(60)
        screen.fill(BLUE)
        mylevel.generate(SCROLLSPEED)
        screen2=mylevel.draw()
        screen.blit(screen2, (-WIDTH/1.95,-HEIGHT/1.95))
        print mylevel.collision(playerxy, screen)
        player.draw(screen, 0) 
        pygame.display.flip()
        # Go ahead and update the screen with what we've drawn.
        
        
        

if __name__ == "__main__":
      main()
