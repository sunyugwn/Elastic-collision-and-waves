import math
import function as f
import pygame as pg
openn = int(input('몇번째 파일을 열까요? >>> '))
a = open(f'./files/video_{openn}.txt', 'r')
white = [255, 255, 255]
black = [0, 0, 0]
pg.init()
FPS = 20
clock = pg.time.Clock()
window = pg.display.set_mode((1920, 1080))
def real_pos(p):
    return [p[0]+460, p[1]+40]


end = False
while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            end = True
    
    op = a.readline().strip()
    if not op:
        end = True
    
    if end:
        break

    s = eval(op)
    window.fill(white)
    for p in s[1]:
        pg.draw.circle(window, [0]*3, real_pos(p[0]), p[2])
        pg.draw.circle(window, [int(255/(f.calculate_line((0, 0), p[1])/25+1))]*3, real_pos(p[0]), p[2]-1)
    
    for w in s[2]:
        pg.draw.rect(window, black, (real_pos(w[0])+f.minus_vector(w[1], w[0])), 2)
    
    pg.display.update()
    clock.tick(FPS)

pg.quit()
a.close()
