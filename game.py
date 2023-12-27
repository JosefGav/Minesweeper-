# Fill me in!
import random

cursor = [Image("https://drive.google.com/file/d/1KIDJ4FwBruXl1yVGS2--jtG5lxU7jMlw/view?usp=sharing",0,0,opacity=0),Label(15,0,0,opacity = 0)]

flagImage = "https://drive.google.com/file/d/1KIDJ4FwBruXl1yVGS2--jtG5lxU7jMlw/view?usp=sharing"
bombImage = "https://drive.google.com/file/d/1EJSjO8-gwbI9ioPuQ1EuRTSjoYThbW-p/view?usp=sharing"
try:
    explosion =  Sound("https://drive.google.com/file/d/1rEbFmrakUJjFIbCFIGcHYlN_tFpGPZrk/view?usp=sharing")
    winningSong = Sound("https://drive.google.com/file/d/1tXNOxpni6612wXSBD_b5-dlXMuV8Kyo1/view?usp=sharing")
except:
    pass

Image("https://drive.google.com/file/d/1sp6_YSAQMpmq9w8Pp_GoGdoxGf-cElJ-/view?usp=sharing",-50,-100)
explosionImage = Image("https://assets.stickpng.com/images/580b585b2edbce24c47b264d.png",-100,-100,visible=False)

militaryMan = Image("https://drive.google.com/file/d/1kAVXN0QfmrWmT9duGYwrTNIsD0SfRKmz/view?usp=sharing",135,120,opacity=0)

menu = Group(
    Label("Left click a tile to reveal it",200,100,opacity = 70,font = "caveat",size=25),
    Label("Hold space while left clicking to flag a tile",200,150,opacity = 70,font = "caveat",size=25),
    Label("Do this again to to remove the flag",200,200,opacity = 70,font = "caveat",size=25),
    Label("Reveal all safe tiles to win",200,250,opacity = 70,font = "caveat",size=25),
    Label("Press any tile to start",200,300,opacity = 70,font = "caveat",size=25)
    )

class Tile():
    def __init__(self,shape,x,y,visible,mine,flag):
        self.shape = shape
        self.x = x
        self.y = y 
        self.visible = visible
        self.mine = mine
        self.flag = flag
        self.surrounding = 0
        self.validLocation = True
        
    def reveal(self,board):
        self.visible = True
        if (self.mine == True):
            
            cursor[0].toBack()
            cursor[1].toBack()
            
            self.shape[2].visible = True
            explosion.sound.play()

            for i in board.mineList:
                sleep(0.15)
                i.shape[2].visible = True
            
            explosion.sound.play()
            explosionImage.visible = True
            board.gameState += 1
        elif self.y % 2 == 1 and self.x % 2 == 0 or self.y % 2 == 0 and self.x % 2 == 1:
            self.shape[0].fill = "darkKhaki"
            board.coveredTiles += 1
        else: 
            self.shape[0].fill = "khaki"
            board.coveredTiles += 1
        self.shape[1].visible = True
        
        if board.coveredTiles == board.tilesToCover:
            gameState = 4
            militaryMan.toFront()
            militaryMan.opacity = 50
            winningSong.play()
            
        
        

    def flood(self,board):
        board.flood(self.x,self.y)
        
    def flagTile(self,board):
        if board.flags > 0 and self.flag == False:
            self.flag = True
            self.shape.append(Image(flagImage,self.shape[0].left,self.shape[0].top,opacity=50))
            board.flags -= 1
            cursor[1].value = board.flags
        elif self.flag == True:
            self.flag = False
            self.shape[-1].opacity = 0
            board.flags += 1
            cursor[1].value = board.flags
        
class Board():
    def __init__(self,size,mines):
        self.coveredTiles = 0
        self.tilesToCover = size * size - mines
        self.board = []
        self.mines = mines
        self.discovered = 0
        self.flags = mines
        self.size = size
        self.gameState = 0
        self.mineList = []
        self.populated = False
        
        self.minesUnplaced = mines
        
        
        for y in range(size):
            row = []
            for x in range(size):
                if y % 2 == 1 and x % 2 == 0 or y % 2 == 0 and x % 2 == 1:
                    row.append(Tile([Rect(50+x*(300/size),50+y*(300/size),300/size,300/size,opacity=95,fill = "grey",borderWidth = 0.1),Label("",50+x*(300/size)+150/size,50+y*(300/size)+150/size,visible=False)],x,y,False,False,False))
                else:
                    row.append(Tile([Rect(50+x*(300/size),50+y*(300/size),300/size,300/size,opacity=95,fill = "darkGrey",borderWidth = 0.1),Label("",50+x*(300/size)+150/size,50+y*(300/size)+150/size,visible=False)],x,y,False,False,False))
            self.board.append(row)
        
        menu.toFront()
        cursor[0].toFront()
        cursor[1].toFront()
        
    def populateBoard(self,r,c):
        
        self.board[r][c].validLocation = False

        try:
            self.board[r+1][c+1].validLocation = False
        except:
            pass
        try:
            self.board[r-1][c+1].validLocation = False
        except: 
            pass
        try:
            self.board[r+1][c-1].validLocation = False
        except:
            pass
        try:
            self.board[r-1][c-1].validLocation = False
        except:
            pass
        try:
            self.board[r+1][c].validLocation = False
        except:
            pass
        try:
            self.board[r-1][c].validLocation = False
        except:
            pass
        try:
            self.board[r][c-1].validLocation = False
        except:
            pass
        try:
            self.board[r][c+1].validLocation = False
        except:
            pass
        
        while self.minesUnplaced > 0:
            x = random.randint(0,self.size-1)
            y = random.randint(0,self.size-1)
            
            if self.board[y][x].mine != True and self.board[y][x].validLocation == True:
                self.board[y][x].mine = True
                self.board[y][x].shape.append(Image(bombImage,self.board[y][x].shape[0].centerX-10,self.board[y][x].shape[0].centerY-10,visible=False))
                self.minesUnplaced -= 1
                self.mineList.append(self.board[y][x])
            
        for y in range(self.size):
            for x in range(self.size):
                try:
                    if self.board[y][x+1].mine == True and x + 1 < self.size:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                try:
                    if self.board[y][x-1].mine == True and x - 1 >= 0:
                        self.board[y][x].surrounding += 1
                except: 
                    pass
                try:
                    if self.board[y+1][x].mine == True and y + 1 < self.size:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                try:
                    if self.board[y-1][x].mine == True and y - 1 >= 0:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                try:
                    if self.board[y+1][x+1].mine == True and x + 1 < self.size and y + 1 < self.size:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                try:
                    if self.board[y-1][x-1].mine == True and x - 1 >= 0 and y - 1 >= 0:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                try:
                    if self.board[y+1][x-1].mine == True and y + 1 < self.size and x - 1 >= 0:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                try:
                    if self.board[y-1][x+1].mine == True and y - 1 >= 0 and x + 1 < self.size:
                        self.board[y][x].surrounding += 1
                except:
                    pass
                
                if (self.board[y][x].surrounding > 0 and self.board[y][x].mine == False):
                    self.board[y][x].shape[1].value = self.board[y][x].surrounding
                    
    def flood(self,x,y):
        if x >= self.size or y >= self.size or x < 0 or y < 0: 
            return
        
        if self.board[y][x].visible == True:
            return
        
        self.board[y][x].reveal(b)
        
        if self.board[y][x].shape[1].value != "":
            return
        
        if self.board[y][x].mine == True:
            return 
        
        self.flood(x+1,y+1)
        self.flood(x-1,y-1)
        self.flood(x+1,y)
        self.flood(x,y+1)
        self.flood(x-1,y)
        self.flood(x,y-1)
        self.flood(x+1,y-1)
        self.flood(x-1,y+1)
b =  Board(10,15)


def onMousePress(x,y):
    if b.gameState == 0 and cursor[0].opacity == 0:
        for r in range(b.size):
            for tile in b.board[r]:
                if tile.shape[0].hits(x,y) and b.populated == False:
                    b.populateBoard(tile.y,tile.x)
                    b.populated = True
                    tile.flood(b)
                    b.gameState += 1
                    menu.visible = False
    elif b.gameState == 1 and cursor[0].opacity == 0:
        for r in range(b.size):
            for tile in b.board[r]:
                if tile.shape[0].hits(x,y) and tile.flag == False:
                    tile.flood(b)
    elif b.gameState == 1 and cursor[0].opacity == 70:
        for r in range(b.size):
            for tile in b.board[r]:
                if tile.shape[0].hits(x,y) and tile.visible == False:
                    tile.flagTile(b)
def onMouseMove(x,y):
    cursor[0].centerX = x + 10
    cursor[0].centerY = y - 10
    cursor[1].centerX = x + 10
    cursor[1].centerY = y 

def onKeyHold(k):
    if "space" in k:
        cursor[0].opacity = 70
        cursor[1].opacity = 70
    else:
        cursor[0].opacity = 0
        cursor[1].opacity = 0
        
def onKeyRelease(k):
    cursor[0].opacity = 0
    cursor[1].opacity = 0
