#pygame 이라는 모듈을 가져와 쓰겠다고 선언!
from mailbox import linesep
import random
from tkinter.tix import CELL
import pygame as pg
from tkinter import messagebox, Tk
import sys
import os

#pygame 시작해주기
pg.init()

#tkinter 설정
Tk().wm_withdraw()

#중요하게 쓰는 내용을 변수로 미리 지정해놓기(다른 변수들과 구분을 위해 모든 글자 대문자로 했음)
CAPTION = "MineSweeper"
ICON = pg.image.load("mine.png")
WIDTH = 1280
HEIGHT = 720
FPS = 144
FONT = pg.font.SysFont("arial", 32, True, True)
cellSize = 24
boardSize = 16
lineSize = 2
interfaceSize = 36
#창 설정
WINDOW = pg.display
WINDOW.set_caption(CAPTION)
WINDOW.set_icon(ICON)
SCREEN = WINDOW.set_mode((WIDTH, HEIGHT))

#색깔, 이미지, 폰트
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LEMONCHIFFON = (255, 250, 205)
SANDYBROWN = (244, 164, 96)

CELLFONT = pg.font.Font('fonts/godoRounded L.ttf', 20)
SYSFONT = pg.font.Font('fonts/godoRounded L.ttf', 26)

mineImage = pg.transform.scale(pg.image.load("image/mine.png"), [cellSize, cellSize])
flagImage = pg.transform.scale(pg.image.load("image/flag.png"), [cellSize, cellSize])
notMineImage = pg.transform.scale(pg.image.load("image/not_mine.png"), [cellSize, cellSize])

#지뢰 색깔
Mine1 = (1, 0, 250)
Mine2 = (0, 126, 0)
Mine3 = (253, 1, 0)
Mine4 = (1, 0, 127)
Mine5 = (124, 1, 0)
Mine6 = (0, 127, 126)
Mine7 = (0, 0, 0)
Mine8 = (128, 128, 128)

numColor = [LEMONCHIFFON, Mine1, Mine2, Mine3, Mine4, Mine5, Mine6, Mine7, Mine8]

RUNNING = True
lose = False
vic = False


#클래스
class board:
    def __init__(self):
        self.content = [[cell(self,i,j) for i in range(16)] for j in range(16)] #내용물은 16*16짜리 칸들
        self.leftMine = 40
    
    def init(self):
        self.mineSetting(40)
    
    def mineSetting(self,n):
        setMine = 0
        while setMine <= 40:
            picked = random.choice(random.choice(self.content))
            if picked.hasMine == True:
                continue
            if picked.isRevealed == True:
                continue
            picked.setMine()
            setMine += 1
        self.cellContent()

    def cellContent(self):
        for i in range(16):
            for j in range(16):
                self.content[j][i].numOfMine = 0
                for k in range(-1,2):
                    for l in range(-1,2):
                        if 0 <= j+k < 16:  
                            if 0 <= i+l < 16:
                                if self.content[j+k][i+l].hasMine:
                                    self.content[j][i].numOfMine += 1
    
    def render(self):
        txt = pg.font.SysFont("arial", 26, True, False).render("Mine Left: %d" % self.leftMine, True, BLACK)
        SCREEN.blit(txt, [5, 5])
        for i in self.content:
            for j in i:
                j.render()



class cell: #1칸에 대한 클래스
    def __init__(self, masterBoard, xcor, ycor):    #전체보드와 정보교환을 위한 masterBoard, 칸의 x좌표, 칸의 y좌표
        self.hasMine = False    #지뢰 여부
        self.isFlag = False     #깃발 설치여부
        self.isRevealed = False #클릭을 통한 공개된 칸 여부
        self.numOfMine = None   #해당칸에 지뢰가 몇개인지 숫자(주위에 지뢰없음 아무것도 없음)
        self.x = xcor           #x좌표
        self.y = ycor           #y좌표
        self.master = masterBoard   #전체보드와의 연결
    
    #지뢰가 설치되면
    def setMine(self):
        self.hasMine = True
    #깃발이 설치되면
    def setFlag(self):
        self.isFlag = True  
        self.master.leftMine -= 1
    #깃발을 제거하면
    def noFlag(self):
        self.isFlag = False
        self.master.leftMine += 1
    
    #칸의 공개
    def open(self):
        if self.isRevealed or self.isFlag:
            return
        self.isRevealed = True
        if self.hasMine:
            defeat()
        elif self.numOfMine == None:
            self.master.init()
            if self.numOfMine == 0:
                for i in range(-1,2):
                    for j in range(-1,2):
                        if 0<= self.y+i < 16 and 0 <= self.x+j < 16:
                            self.master.content[self.y+i][self.x+j].open()
        elif self.numOfMine == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= self.x+j < 16 and 0 <= self.y+i < 16:
                        self.master.content[self.y+i][self.x+j].open()


    #칸 그리기
    def render(self):
        xposition = lineSize + (cellSize + lineSize) * self.x #칸의 우상단(시작점) x좌표 지정하기
        yposition = interfaceSize + lineSize + (cellSize + lineSize) * self.y #칸의 우상단(시작점) y좌표 지정하기
        xline = yline = cellSize    #칸의 한 변 길이 지정

        if self.isRevealed:
            if not self.hasMine:
                pg.draw.rect(SCREEN, LEMONCHIFFON, [xposition, yposition, xline, yline])    #공개x, 지뢰x, 게임시작시 기본 칸 렌더링
                if self.numOfMine != None and self.numOfMine != 0:
                    text = CELLFONT.render(str(self.numOfMine), True, numColor[self.numOfMine])
                    rect = text.get_rect()
                    rect.center = (xposition + xline/2, yposition + yline/2)
                    SCREEN.blit(text,rect)
            else:   #지뢰 밟은 상태 칸 렌더링
                pg.draw.rect(SCREEN, SANDYBROWN, [xposition, yposition, xline, yline])
                SCREEN.blit(mineImage, [xposition, yposition])
        else:
            pg.draw.rect(SCREEN, SANDYBROWN, [xposition, yposition, xline, yline])
            if self.isFlag:
                if not self.hasMine and lose != False:
                    SCREEN.blit(notMineImage, [xposition, yposition])
                else:
                    SCREEN.blit(flagImage, [xposition, yposition])
                    
#함수
def fill_background():
    SCREEN.fill(WHITE)

def mouse_position():
    return pg.mouse.get_pos()

def is_LMBdown_event(e):
    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
        return True
    return False

def is_LMB_able(b):
     if b != None and not b.isRevealed and not b.isFlag:
         return True
     return False

def is_RMBdown_event(e):
    if e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
        return True
    return False

def is_RMB_able(b):
     if b != None and not b.isRevealed:
         return True
     return False

def button_with_cursor():
    mp = list(mouse_position())
    mp[0], mp[1] = mp[1] - 36, mp[0] #tab_size subtraction
    if lineSize <= mp[0] % (cellSize + lineSize) and lineSize <= mp[1] % (cellSize + lineSize):
        if (cellSize + lineSize) * 16 <= mp[0] or (cellSize + lineSize) * 16 <= mp[0] <= mp[1]:
            return None
        return gameBoard.content[mp[0] // (cellSize + lineSize)][mp[1] // (cellSize + lineSize)]
    else:
        return None

def defeat():
    global gameBoard, lose
    for i in gameBoard.content:
        for j in i:
            if j.hasMine:
                j.isRevealed = True
    lose = True

def all_found():
    num = 0
    for i in gameBoard.content:
        for j in i:
            if j.isRevealed or j.hasMine:
                num += 1
    if num == 16 ** 2:
        return True
    return False

def victory():
    global vic
    vic = True

gameBoard = board()



#While 문으로 True 무한루프 돌려서 창이 안꺼지게 만들기
while RUNNING:
    """ pg.time.Clock().tick(FPS)   #프레임갱신을 내가 지정한 FPS로 설정하기
    
    #지뢰찾기 코드가 들어갈곳!

    
    SCREEN.fill(WHITE) #스크린 색칠하기
    # SCREEN.blit(text, [800, 100])
    for a in range(0,17):
        pg.draw.line(SCREEN, BLACK, (a*40,0), (a*40,640), 1)
        pg.draw.line(SCREEN, BLACK, (0,a*40), (640, a*40), 1)
    event = pg.event.poll()
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 :
        pos = pg.mouse.get_pos()
        if pos[0]>=50 and pos[0]<=250 and pos[1]>=50 and pos[1]<=200 :
            text = FONT.render("GAME OVER", True, WHITE)
        
        print(pg.mouse.get_pos())
    elif event.type == pg.KEYDOWN and event.key == pg.K_a:
        text = FONT.render("A button down", True, WHITE)

    #pg.draw.rect(SCREEN, RED, [32, 64, 96, 128]) #사각형그리기 - 위치, 색깔, 왼쪽변 끝으로부터 떨어진 거리, 오른쪽 변 끝으로 부터 떨어진 거리, 가로길이, 세로길이

    #플레이어가 조작을 통해 변경된 내용을 갱신하여 화면에 표시해주기
    pg.display.update() 

    #X버튼 눌렀을 때 종료가 되도록 만들기
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            RUNNING = False """

    pg.time.Clock().tick(FPS)
    
    fill_background()
    gameBoard.render()

    if vic == True:
        if messagebox.askretrycancel("Game Over!", "Victory! ^.^\nRetry?"):
            game_board = board()
            vic = False
        else:
            exit(0)


    elif lose == 2:
        if messagebox.askretrycancel("Game Over!", "You Step On A Mine... T.T\nRetry?"):
            gameBoard = board()
            lose = False
        else:
            exit(0)

    if all_found():
        victory()

    WINDOW.update()

    for event in pg.event.get():
        if is_LMBdown_event(event):
            current_button = button_with_cursor()
            if is_LMB_able(current_button):
               current_button.open()
        elif is_RMBdown_event(event):
            current_button = button_with_cursor()
            if is_RMB_able(current_button):
               if current_button.isFlag:
                   current_button.noFlag()
               else:
                   current_button.setFlag()
        elif event.type == pg.QUIT:
            if messagebox.askyesno("Exit?", "You Really Want To Quit?"):
                pg.display.quit()
                RUNNING = False