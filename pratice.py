#pygame 이라는 모듈을 가져와 쓰겠다고 선언!
import pygame as pg

#pygame 시작해주기
pg.init()

#중요하게 쓰는 내용을 변수로 미리 지정해놓기(다른 변수들과 구분을 위해 모든 글자 대문자로 했음)
CAPTION = "MineSweeper"
ICON = pg.image.load("mine.png")
WIDTH = 640
HEIGHT = 360
FPS = 144

WINDOW = pg.display
WINDOW.set_caption(CAPTION)
WINDOW.set_icon(ICON)
SCREEN = WINDOW.set_mode((WIDTH, HEIGHT))

#자주쓸것같은 내용들은 미리 선언해두기
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

RUNNING = True

#While 문으로 True 무한루프 돌려서 창이 안꺼지게 만들기
while RUNNING:
    pg.time.Clock().tick(FPS)   #프레임갱신을 내가 지정한 FPS로 설정하기

    #지뢰찾기 코드가 들어갈곳!

    SCREEN.fill(BLUE) #스크린 색칠하기
    pg.draw.rect(SCREEN, RED, [32, 64, 96, 128]) #사각형그리기 - 위치, 색깔, 왼쪽변 끝으로부터 떨어진 거리, 오른쪽 변 끝으로 부터 떨어진 거리, 가로길이, 세로길이

    #플레이어가 조작을 통해 변경된 내용을 갱신하여 화면에 표시해주기
    pg.display.update() 

    #X버튼 눌렀을 때 종료가 되도록 만들기
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            RUNNING = False