# Pygame tic tac toe implementation
import pygame
import sys
import pprint

SIZE = (800,800)
FPS = 144
CLOCK = pygame.time.Clock()
MouseRaw = [0,0]

# Game Settings
BoardSize = (3,3)
CursorSize = 5
dividerSpacing = 10 #px

# Game Functions
class GameManager():
    def __init__(self,size,screen):
        self.size = size    # (x/y)
        self.screen = screen
        self.GetDividerSize()
        self.GridRecs = []

        self.mouseDelta = [0,0]
        self.prevMouse = pygame.mouse.get_pos()

        self.Board = GameManager.MakeBoard(self.size) 
        # print(self.Board)

        self.Cross = True


    # --------------------- Helpers ---------------------
    def MakeBoard(BoardDimensions):
        return [[0 for x in range(0,BoardDimensions[0])] for y in range(0,BoardDimensions[1])]

    def GetDividerSize(self):
        self.dividers = (self.screen.get_width()/self.size[0],
                         self.screen.get_height()/self.size[1])

    def pprintBoard(self):
        print('-----------------------------------------------')
        # prstr = ''
        # for i,x in enumerate(self.Board):
        #     prstr += str(self.Board[i])
        #     prstr += '\n'
        # print(prstr)
        print(self.Board)
        print('-----------------------------------------------')

    # --------------------- Logic ---------------------    
    def GetMouseDelta(self):
        newpos = pygame.mouse.get_pos()
        self.mouseDelta = (newpos[0] - self.prevMouse[0],newpos[1] - self.prevMouse[1])
        print(self.mouseDelta)
        self.prevMouse = newpos

    def MakeGrid(self):
        # Draws PreProcessed Grid Squares 
        if self.GridRecs != []:
            for i,x in enumerate(self.GridRecs):
                for j,space in enumerate(x):
                    # print(i,j)
                    match self.Board[j-1][i-1]:
                        case 2:
                            pygame.draw.rect(self.screen,(255,255,0),space)
                        case 1:
                            pygame.draw.rect(self.screen,(0,255,255),space)
                        case _:
                            pygame.draw.rect(self.screen,(0,255,0),space)
            return

        #Calculate grid positions if none were specified before
        Xpos = 0
        for x in range(0,self.size[0]+1):
            Ypos = 0
            grid = []   # Mirror 2d array
            for y in range(0,self.size[1]+1):
                grid.append(pygame.Rect(Xpos+dividerSpacing,
                                                        Ypos+dividerSpacing,
                                                        self.dividers[0]-(dividerSpacing*2),
                                                        self.dividers[1]-(dividerSpacing*2)
                                                        ))
                Ypos += self.dividers[1]
            self.GridRecs.append(grid)
            Xpos += self.dividers[0]

    # User Input Turns
    def Turn(self):
        if pygame.mouse.get_pos()[0]:
            for i,x in enumerate(self.GridRecs):
                for j,square in enumerate(x):
                    if square.collidepoint(pygame.mouse.get_pos()):
                        self.SetSquare(i,j)
                        self.CheckWinner()

    def SetSquare(self,x,y):
        x=x-1
        y=y-1
        if self.Board[y][x] != 0:
            return
        if self.Cross:
            self.Board[y][x] = 1
        else:
            self.Board[y][x] = 2
        self.Cross = not self.Cross
        self.pprintBoard()
    
    #TODO: Checks if someone has won -- 2D ARRAYS NEED WORKING ON - if i cant tell how its structured, then i cant fix it :/
    def CheckWinner(self):
        #    x-1y-1,xy-1,x+1y-1
        # check x-1y,xy,x+1y
        #    x-1y+1,xy+1,x+1y+1
        
        for y,col in enumerate(self.Board):
            # Check horizontals
            for x,row in enumerate(col):
                # above = [self.Board[i-1][j-1],self.Board[i][j-1],self.Board[i+1][j-1]]

                # this is not the way brother
                if x == 0:
                    above = col[x]
                else:
                    above = col[x+1]

                if len(col)-1 == x:
                    below = col[x]
                else:
                    below = col[x-1]

                print(f'above: {above} - below: {below}')
                print(self.Board[i][j])


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
                if self.Cross:
                    pygame.draw.circle(self.screen,(0,255,255),pygame.mouse.get_pos(),CursorSize)
                else:
                    pygame.draw.circle(self.screen,(255,255,0),pygame.mouse.get_pos(),CursorSize)

    # Draw all screen things
    def Draw(self):
        self.DrawBoard()
        self.MakeGrid()
        self.DrawMouse()

# For Fun
def ChangingSize(GM):
    changed = False
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if GM.size[0]-1 >= 3:
            GM.size = (GM.size[0]-1,GM.size[1])
            changed = True

    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        GM.size = (GM.size[0]+1,GM.size[1])
        changed = True
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        GM.size = (GM.size[0],GM.size[1]+1)
        changed = True
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if GM.size[1]-1 >= 3:
            GM.size = (GM.size[0],GM.size[1]-1)
            changed = True

    if not changed:
        return
    GM.GetDividerSize()
    GM.GridRecs = []
    GM.Board = GameManager.MakeBoard(GM.size) 
    print(GM.Board)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    GM.Turn()
        CLOCK.tick(FPS)