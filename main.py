import pygame
import math

#GLOBALS
SCREENSIZE = (1024,768)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

class Player(pygame.sprite.Sprite):
    """ Class for the player's character """
    
    def __init__(self, xPos, yPos):
        """ Constructor """

        #call parent constructor
        super(Player, self).__init__()

        #At some point make this an image not a square...
        width = 40
        height = 40
        self.image = pygame.Surface((width,height))
        self.image.fill(RED)

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
        

    def calc_physics(self):
        if self.direction == 1:
            self.rampUp += .65
            self.velocity_y = self.rampUp
            if self.energy < 300:
                self.energy += self.velocity_y
        elif self.direction == -1:
            self.rampUp = 0
            self.velocity_y = -.09*self.energy
            self.energy *= .935
            if self.energy < 2:
                self.energy = 2
        else:
            if self.energy < 2:
                self.energy = 2
            else:
                self.energy *= .98
            self.rampUp = 0
            self.velocity_y = 0
        print self.energy
            

def main():
    pygame.init()
    #initialize screen surface
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Wingsuit!")

    #loop until player closes
    running = True

    #Manage screen updates
    clock = pygame.time.Clock()
    
    player = Player(512,384)

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
        player.update(angle)
        player.draw(screen, 0)
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        

if __name__ == "__main__":
      main()
