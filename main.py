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
    GRAVITY = 0.0169706
    LIFT_COEF = .0015000
    DRAG_COEF = .0015000
    MOMENTUM_COEF = 0
    
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
        self.velocity = 2.8
        self.velocity_x = 2
        self.velocity_y = 2
        self.angle = 45
        self.ANGLE_MAX = 175
        
        #Drawing vars
        self.xPos = xPos
        self.yPos = yPos


    def draw(self, screen, yVelocity):
        self.yPos += yVelocity + self.velocity_x
        print 'yPos:{0}'.format(self.yPos)
        self.rect.x = self.xPos
        self.rect.y = self.yPos
        screen.blit(self.image, self.rect)
        pygame.draw.line(screen,RED, (self.rect.x+20, self.rect.y+20), (20+self.rect.x + 150*math.sin(math.radians(self.angle)), 20+self.rect.y+150*math.cos(math.radians(self.angle))), 3)

    def update(self,angle_change):
        self.angle += angle_change
        if self.angle > self.ANGLE_MAX:
            self.angle = self.ANGLE_MAX
        elif self.angle < 0:
            self.angle = 0
        self.calc_physics()
        

    def calc_physics(self):
        lift = Player.LIFT_COEF * self.velocity * self.velocity
        drag = Player.DRAG_COEF * self.velocity * self.velocity
        momentum = Player.MOMENTUM_COEF * self.velocity
        AngCos = math.cos(math.radians(self.angle))
        AngSin = math.sin(math.radians(self.angle))
        #print 'l:{0} d:{1} m:{2} Cos:{3} Sin:{4}'.format(lift,drag,momentum,AngCos,AngSin)
        self.velocity_x += lift*AngCos+momentum*AngSin-drag*AngSin
        self.velocity_y += -lift*AngSin+momentum*AngCos-drag*AngCos+Player.GRAVITY
        self.velocity = math.sqrt((self.velocity_x * self.velocity_x) + (self.velocity_y * self.velocity_y))

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
            angle = 5
        elif key[pygame.K_DOWN]:
            angle = -5
        player.update(angle)
        player.draw(screen, -2)
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        

if __name__ == "__main__":
      main()
