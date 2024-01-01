# Pygame tic tac toe implementation
import pygame, random

SIZE = (800,800)
FPS = 144
CLOCK = pygame.time.Clock()
MouseRaw = [0,0]

# Game Settings
BoardSize = (3,3)
CursorSize = 5

# Game Functions
class GameManager():

    def __init__(self,size,screen):
        self.size = size
        self.screen = screen
        self.GetDividerSize()

        self.mouseDelta = [0,0]
        self.prevMouse = pygame.mouse.get_pos()


    def GetDividerSize(self):
        self.dividers = (self.screen.get_width()/self.size[0],
                         self.screen.get_height()/self.size[1])

    # --------------------- Draw ---------------------    
    def DrawBoard(self):
        # Draw lines for each grid section
        Xpos = 0
        Ypos = 0
        
        for x in range(0,self.size[0]-1):
            Xpos += self.dividers[0]
            pygame.draw.line(self.screen,(255,255,255),(Xpos,0),(Xpos,self.screen.get_height()))
        
        for y in range(0,self.size[1]-1):
            Ypos += self.dividers[1]
            pygame.draw.line(self.screen,(255,255,255),(0,Ypos),(self.screen.get_width(),Ypos))

    def DrawMouse(self):
        # Switch to nice sprites at some point
        match pygame.mouse.get_pressed():
            case (1,0,0):
                pygame.draw.circle(self.screen,(100,100,100),pygame.mouse.get_pos(),CursorSize)
            case _:
                pygame.draw.circle(self.screen,(255,255,255),pygame.mouse.get_pos(),CursorSize)

    # Draw all screen things
    def Draw(self):
        self.DrawBoard()
        self.DrawMouse()

    # --------------------- Logic ---------------------    
    def GetMouseDelta(self):
        newpos = pygame.mouse.get_pos()
        self.mouseDelta = (newpos[0] - self.prevMouse[0],newpos[1] - self.prevMouse[1])
        print(self.mouseDelta)
        self.prevMouse = newpos


# For Fun
def ChangingSize(GM):
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if GM.size[0]-1 >= 3:
            GM.size = (GM.size[0]-1,GM.size[1])
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        GM.size = (GM.size[0]+1,GM.size[1])
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        GM.size = (GM.size[0],GM.size[1]+1)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if GM.size[1]-1 >= 3:
            GM.size = (GM.size[0],GM.size[1]-1)

    GM.GetDividerSize()
    print(GM.size)


def Game():
    # Setup
    pygame.init()
    screen = pygame.display.set_mode(SIZE,)
    pygame.mouse.set_visible(0)
    running = True
    GM = GameManager(BoardSize,screen)
    # Game Loop
    while running:
        screen.fill((0,0,0))
        GM.Draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
            if event.type == pygame.KEYDOWN:
                ChangingSize(GM)
        CLOCK.tick(FPS)