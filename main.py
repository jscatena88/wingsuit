import pygame

#GLOBALS
SCREENSIZE = (1024,768)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

class Player(pygame.spriteSprite):
    """ Class for the player's character """
    
    def __init__(self):
        """ Constructor """

        #call parent constructor
        super().__init__()

        #At some point make this an image not a square...
        width = 40
        height = 60
        self.image = pygame.Surface((width,height))
        self.image.fill(RED)

        #define rect for collision and such
        self.rect = self.image.get_rect()

        #set speed vectors
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.calc_physics()

    def calc_physics(self):




def main():
    pygame.init()

    #initialize screen surface
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Wingsuit!")

    #loop until player closes
    running = True

    #Manage screen updates
    clock = pygame.time.Clock()

    #----- Main Game Loop-----
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
