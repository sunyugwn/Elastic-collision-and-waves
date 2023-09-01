'''
particle = [[x좌표, y좌표], [x속도, y속도], 반지름, 질량]
wall = [[x1, y1], [x2, y2], [x속도, y속도], [충격 흡수율]]
space = [[공간 가로길이, 공간 세로길이], [particle], [wall]]]
'''
#모듈 호출
import math
import random
from copy import deepcopy
import time
#함수 정의
##만들기##
###공간 만들기
'''
size = [공간 가로길이, 공간 세로길이]
'''
def make_space(size):
    return [size, [], []]


###벽 만들기
'''
walls = [[[x1, y1], [x2, y2], [x속도, y속도], 충격 흡수율], ...]
'''
def make_walls(space, walls):
    space[2] += walls
    return space


###입자 만들기
'''
space = 공간
v = 속도
r = 반지름
m = 질량
l = 최대 입자 수
'''
def make_particles(space, v, r, m, l):
    for _ in range(l):
        x = random.uniform(r, space[0][0]-r)     #랜덤 좌표 부여
        y = random.uniform(r, space[0][1]-r)
        TF = True

        for cw in space[2]:    #벽과 겹치는지 검사
            if cw[0][0]-r<=x<=cw[1][0]+r and cw[0][1]-r<=y<=cw[1][1]+r:     #입자가 벽과 겹칠 가능성이 있는 범위에 있는가
                if cw[0][0]<=x<=cw[1][0] or cw[0][1]<=y<=cw[1][1]:          #입자가 벽의 모서리와 겹치는가
                    TF = False
                    break

                #입자가 벽의 꼭지점과 겹치는지 검사
                if cw[1][0]<x:     #x좌표가 벽의 오른쪽보다 큰가
                    cx = cw[1][0]   #검사할 꼭지점의 x좌표를 벽의 오른쪽으로 설정
                else:
                    cx = cw[0][0]   #검사할 꼭지점의 x좌표를 벽의 왼쪽으로 설정
                
                if cw[0][1]>y:     #y좌표가 벽의 위쪽보다 큰가
                    cy = cw[0][1]   #검사할 꼭지점의 y좌표를 벽의 위쪽으로 설정
                else:
                    cy = cw[1][1]   #검사할 꼭지점을 y좌표를 벽의 아래쪽으로 설정
                
                if calculate_line((x, y), (cx, cy)) < r:   #꼭지점과 겹치는지 검사
                    TF = False
                    break

        if TF == True:
            for cp in space[1]:     #다른 입자들과 닿아있는지 검사
                if calculate_line((x, y), cp[0]) < (r+cp[2]):
                    TF = False
                    break
            
            if TF == True:
                pv = random.uniform(0, 2*v)
                pd = math.radians(random.uniform(0, 360))
                space[1].append([[x, y], [pv*math.sin(pd), pv*math.cos(pd)], r, m])
    
    return space



##측정##
###두 점의 좌표가 주어졌을때 두 점 사이의 거리 계산
'''
p = [x좌표, y좌표]
'''
def calculate_line(p1, p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5   #피타고라스 정리 이용


###두 점의 좌표가 주어졌을때 두 점 사이의 거리의 제곱 계산
'''
p = [x좌표, y좌표]
'''
def calculate_line_square(p1, p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2   #피타고라스 정리 이용


###두 점의 좌표가 주어졌을때 첫번째 점에서 두번째 점을 바라본 뱡향 계산
'''
p = [x좌표, y좌표]
'''
def calculate_direction(p1, p2):
    if p2[0]-p1[0] == 0:     #탄젠트 90, 270일때 에러 안나도록 예외
        return 180*(0>p2[1]-p1[1])
    
    return 90-math.degrees(math.atan((p2[1]-p1[1])/(p2[0]-p1[0])))+(p2[0]-p1[0]<0)*180   #탄젠트 값을 구하고 역탄젠트를 이용하여 방향 구하기

def calculate_directionr(p1, p2):
    if p2[0]-p1[0] == 0:     #탄젠트 90, 270일때 에러 안나도록 예외
        return math.pi*(0>p2[1]-p1[1])
    
    return math.pi/2-math.atan((p2[1]-p1[1])/(p2[0]-p1[0]))+(p2[0]-p1[0]<0)*math.pi   #탄젠트 값을 구하고 역탄젠트를 이용하여 방향 구하기


##계산##
###벡터 합
'''
v = [x속도, y속도]
'''
def plus_vector(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1]]


####벡터 차
'''
v = [x속도, y속도]
'''
def minus_vector(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1]]


###입자 이동시키기
'''
p = [[x좌표, y좌표], [x속도, y속도]]
'''
def move_particle(p, time=1):
    return [p[0][0]+p[1][0]*time, p[0][1]+p[1][1]*time]


def move_wall(w, time=1):
    move = [w[2][0]*time, w[2][1]*time]
    return [plus_vector(w[0], move), plus_vector(w[1], move)]

##충돌 시간 계산##
###입자끼리 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x속도, y속도], 반지름]
'''
def check_crash_particle(p1, p2):
    if p1[1] == p2[1]:
        return False
    
    #p1이 (0, 0)에 있고, p2의 속도가 (0, 0)이라고 가정했을때 그려지는 직선과 p2가 중심인 반지름이 r1+r2인 원의 교점과 (0, 0)사이의 거리를 이용해서 구한다
    np2_pos = (p2[0][0]-p1[0][0], p2[0][1]-p1[0][1])   #p1이 (0, 0)에 있다고 가정할때, p2의 좌표 구하기
    p3_pos = minus_vector(p1[1], p2[1])               #p3 = p1이 (0, 0)에 있고, p2의 속도가 (0, 0)이라고 가정할때, p1이 이동했을때의 좌표
    aq = calculate_line_square((0, 0), np2_pos)       #p1과 p2사이의 거리의 제곱
    bq = calculate_line_square(p3_pos, np2_pos)       #p2와 p3사이의 거리의 제곱
    c = calculate_line((0, 0), p3_pos)                #p1과 p3사이의 거리
    x = (aq-bq+c**2)/(2*c)     #p2에서 선분p1-p3에 내린 수선의 발과 p1사이의 거리(x+y=c, aq-x**2=bq-y**2으로 방정식 풀면 나오는 결과)
    hq = aq-x**2               #수선의 길이의 제곱
    rq = (p1[2]+p2[2])**2      #p1과 p2의 반지름의 합의 제곱
    if hq >= rq:               #충돌하는가
        return False
    
    q = (rq-hq)**0.5    #원의 교점과 수선의 발 사이의 거리
    result = (x-q)/c    #걸린 시간
    if 1 > result >= 0:
        return [True, result]
    
    return False

###입자와 벽 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x속도, y속도], 반지름]
w = [[x1, y1], [x2, y2], [x속도, y속도]]
'''
def check_crash_wall(p, w):
    npv = minus_vector(p[1], w[2])
    
    x = (w[1][0]<p[0][0])-(w[0][0]>p[0][0])     #왼쪽:-1, 중간:0, 오른쪽:1
    y = (w[0][1]>p[0][1])-(w[1][1]<p[0][1])     #아래쪽:-1, 중간:0, 위쪽:1

    if (x, y) == (0, 0):
        return 'Error', 0/0
    
    #왼쪽 벽
    r = []
    if x == -1:
        if npv[0] > 0 and p[0][0]+p[2] <= w[0][0]:      #오른쪽으로 이동 중이고, 왼쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[0][0]-p[0][0]-p[2])/npv[0]          #걸린 시간
            if (t < 1) and (w[0][1] <= p[0][1]+npv[1]*t <= w[1][1]):   #걸린 시간이 0과 1사이고, 충돌지점이 벽인가
                r.append([True,  [t, 'l']])
    
    #오른쪽 벽
    elif x == 1:
        if npv[0] < 0 and p[0][0]-p[2] >= w[1][0]:     #왼쪽으로 이동 중이고, 오른쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[1][0]-p[0][0]+p[2])/npv[0]         #걸린 시간
            if (t < 1) and (w[0][1] <= p[0][1]+npv[1]*t <= w[1][1]):   #걸린 시간이 0과 1사이고, 충돌지점이 벽인가
                r.append([True, [t, 'r']])
    
    #아래쪽 벽
    if y == -1:
        if npv[1] < 0 and p[0][1]-p[2] >= w[1][1]:     #위로 이동 중이고, 아래쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (-p[0][1]+p[2]+w[1][1])/npv[1]         #걸린 시간
            if (t < 1) and (w[0][0] <= p[0][0]+npv[0]*t <= w[1][0]):   #걸린 시간이 0과 1사이고, 충돌지점이 벽인가
                r.append([True,[t, 'd']])
    
    #위쪽 벽
    elif y == 1:
        if npv[1] > 0 and p[0][1]+p[2] <= w[0][1]:     #아래로 이동 중이고, 위쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[0][1]-p[0][1]-p[2])/npv[1]         #걸린 시간
            if (t < 1) and (w[0][0] <= p[0][0]+npv[0]*t <= w[1][0]):   #걸린 시간이 0과 1 사이고, 충돌지점이 벽인가
                r.append([True, [t, 'u']])
    
    if r != []:
        rr = [False, [10]]
        for i in r:
            if i[1][0] < rr[1][0]:
                rr = i
        
        return rr
    
    #벽의 꼭지점
    f = lambda x:(x+1)//2    #-1 >>> 0, 1 >>> 1
    check = 10     #시간이 가장 적게 걸린 것을 고르기 위한 리스트(시간)
    if x == 0:   #(0, -1) 또는 (0, 1)에 있는 경우
        for i in [0, 1]:
            a = check_crash_particle(p, ([w[i][0], w[1-f(y)][1]], w[2], 0))     #충돌 검사
            if a != False and a[1] < check:     #충돌했고, 가장 적은 시간이 걸렸나
                check = a[1]                #충돌 시간과 충돌한 대상 저장
                check_point = [i, 1-f(y)]
    
    elif y == 0:   #(-1, 0) 또는 (1, 0)에 있는 경우
        for i in [0, 1]:
            a = check_crash_particle(p, ([w[f(x)][0], w[i][1]], w[2], 0))     #충돌 검사
            if a != False and a[1] < check:     #충돌했고, 가장 적은 시간이 걸렸나
                check = a[1]                #충돌 시간과 충돌한 대상 저장
                check_point = [f(x), i]
    
    else:   #나머지 경우
        for i1 in [0, 1]:
            for i2 in [0, 1]:
                if (i1, i2) != (1-f(x), f(y)):   #충돌가능한 위치인가
                    a = check_crash_particle(p, ([w[i1][0], w[i2][1]], w[2], 0))   #충돌 검사
                    if a != False and a[1] < check:   #충돌했고, 가장 적은 시간이 걸렸나
                        check = a[1]        #충돌 시간과 충돌한 대상 저장
                        check_point = [i1, i2]
    
    if check == 10 or check >= 1:   #초기값이 안 바뀌었다면 충돌하지 않았다는 뜻
        return False
    
    return [True, [check, [w[check_point[0]][0], w[check_point[1]][1]]]]




##충돌 처리##
###벽과 입자 충돌 처리
'''
particle = [[x, y], [x속도, y속도]]
time = 시간
side = 충돌한 측면 or 충돌한 좌표
wv = [벽의 x속도, 벽의 y속도]
b = 충격 흡수율
'''
def crash_wall(particle, time, side, wv, b):
    move = list(particle[1])
    if side in ['r', 'l']:
        move[0] = b*(wv[0]*2-move[0])
    
    elif side in ['u', 'd']:
        move[1] = b*(wv[1]*2-move[1])
    
    else:
        np1 = move_particle(particle, time)   #p1 이동시키기
        np1m = minus_vector(particle[1], wv)   #p2의 속도가 0일때 p1의 상대적 속도
        md = calculate_directionr((0, 0), np1m)   #이동방향의 방향
        d = calculate_directionr(np1, side)   #p1에서 바라본 p2
        v1 = calculate_line(np1m, (0, 0))   #p1의 속도(직선길이)
        sd = math.sin(d)
        cd = math.cos(d)
        mp = 2*v1*math.cos(abs(d-md))   #p1의 d방향으로 가려는 속도
        np1p = minus_vector(np1m, (mp*sd, mp*cd))   #p1의 속도 구하기
        move = plus_vector(np1p, wv)
    
    return move



###입자끼리의 충돌 처리
'''
p = [[x좌표, y좌표], [x속도, y속도], 반지름, 질량]
'''
def crash_particle(p1, p2, time):
    np1 = move_particle(p1, time)   #p1 이동시키기
    np2 = move_particle(p2, time)
    np1m = minus_vector(p1[1], p2[1])   #p2의 속도가 0일때 p1의 상대적 속도
    md = calculate_directionr((0, 0), np1m)   #이동방향의 방향
    d = calculate_directionr(np1, np2)   #p1에서 바라본 p2
    v1 = calculate_line(np1m, (0, 0))   #p1의 속도(직선길이)
    sd = math.sin(d)
    cd = math.cos(d)
    pv1c = v1*math.cos(abs(d-md))   #p1의 d방향으로 가려는 속도
    v1c = (p1[3]-p2[3])*pv1c/(p1[3]+p2[3])  #d방향으로 가려는 속도 중 충돌 후 반사된 후 여전히 그쪽으로 가려는 속도
    v2c = 2*pv1c*p1[3]/(p1[3]+p2[3])        #d방향으로 가려는 충돌 후 p2의 속도
    mp = pv1c-v1c   #p2에게 전달된 속도의 크기
    np1p = minus_vector(np1m, (mp*sd, mp*cd))   #p1의 속도 구하기
    return [plus_vector(np1p, p2[1]), plus_vector(p2[1], (v2c*sd, v2c*cd))]   #절대적인 속도 구해서 반환

def run_program(myfunction, firstspace, gps, slow):
    space = deepcopy(firstspace)
    def real_pos(p):
        return [p[0]+460, p[1]+40]
    
    black = [0, 0, 0]
    white = [255, 255, 255]
    end = False
    playtime = 0
    save = []
    save.append(deepcopy(space))
    Firsttime = time.time()

    while playtime < gps and not end:
        #print('playtime :', playtime)
        tt = time.time()
        playtime += 1
        print(f'\r{round(playtime/gps*10000)/100}%, {round(((tt-Firsttime)/playtime*(gps-playtime))*100)/100}sec left, {round(tt-Firsttime)}sec passed                           ', end='')
        myfunction(playtime, space)
        lp = len(space[1])
        lw = len(space[2])
        #이동 및 충돌 계산
        t = 0
        l = []
        Min = [10]
        for i in range(lp):
            for j in range(lp):
                if i >= j:
                    l.append([100])
                    continue
                else:
                    a = check_crash_particle(space[1][i], space[1][j])
                    
                    if a == False:
                        l.append([10])
                    else:
                        l.append([a[1]])
                
                if l[-1] != [10] and l[-1][0] < Min[0]:
                    Min = deepcopy(l[-1])
                    Mini = len(l)-1
            
            for j in range(lw):
                a = check_crash_wall(space[1][i], space[2][j])
                
                if a == False:
                    l.append([10])
                else:
                    l.append(a[1])
                
                if l[-1] != [10] and l[-1][0] < Min[0]:
                    Min = deepcopy(l[-1])
                    Mini = len(l)-1
            
            if end:
                break
        while not end:
            if t+Min[0] > 1:
                break

            i = Mini//(lp+lw)
            j = Mini%(lp+lw)
            
            for i2 in range(len(l)):
                if l[i2][0] <= 1:
                    l[i2][0] -= Min[0]
            
            for p in space[1]:
                p[0] = move_particle(p, Min[0])
            
            for p in space[2]:
                p[0], p[1] = move_wall(p, Min[0])
            
            if j >= lp:
                a = crash_wall(space[1][i], 0, Min[1], space[2][j-lp][2], space[2][j-lp][3])

                space[1][i][1] = a
                
                for j in range(lp):
                    if i == j:
                        continue
                    
                    a = check_crash_particle(space[1][i], space[1][j])
                    if a == False:
                        w = [10]
                    else:
                        w = [a[1]]
                    
                    if i < j:
                        l[i*(lp+lw)+j] = w
                    else:
                        l[j*(lp+lw)+i] = w
                
                for j in range(lw):
                    a = check_crash_wall(space[1][i], space[2][j])
                    if a == False:
                        w = [10]
                    else:
                        w = a[1]
                    
                    l[i*(lp+lw)+lp+j] = w
            
            else:
                a, b = crash_particle(space[1][i], space[1][j], 0)
                space[1][i][1] = a
                space[1][j][1] = b
                for j2 in range(lw):
                    a = check_crash_wall(space[1][i], space[2][j2])
                    if a == False:
                        w = [10]
                    else:
                        w = a[1]
                    
                    l[i*(lp+lw)+lp+j2] = w
                for i2 in range(lw):
                    a = check_crash_wall(space[1][j], space[2][i2])
                    if a == False:
                        w = [10]
                    else:
                        w = a[1]
                    
                    l[j*(lp+lw)+lp+i2] = w
                
                for j2 in range(lp):
                    if i == j2:
                        continue
                    a = check_crash_particle(space[1][i], space[1][j2])
                    if a == False:
                        w = [10]
                    else:
                        w = [a[1]]
                    
                    if i < j2:
                        l[i*(lp+lw)+j2] = w
                    else:
                        l[j2*(lp+lw)+i] = w
                
                for i2 in range(lp):
                    if j == i2:
                        continue
                    a = check_crash_particle(space[1][i2], space[1][j])
                    if a == False:
                        w = [10]
                    else:
                        w = [a[1]]
                    
                    if j < i2:
                        l[j*(lp+lw)+i2] = w
                    else:
                        l[i2*(lp+lw)+j] = w
            
            t += Min[0]
            Min = [10]
            nMini = -1
            for i, e in enumerate(l):
                if i != Mini and e[0] < Min[0]:
                    Min = deepcopy(e)
                    nMini = i
            
            Mini = nMini
        
        for i in space[1]:
            i[0] = move_particle(i, 1-t)
            i[1][0] *= slow
            i[1][1] *= slow
        
        for i in space[2]:
            i[0], i[1] = move_wall(i, 1-t)
        
        save.append(deepcopy(space))
    
    print(f'\rsaving...                                                                                                       ')
    import os.path
    n = -1
    while True:
        n += 1
        if not os.path.exists(f'./files/video_{n}.txt'):
            break

    a = open(f'./files/video_{n}.txt', 'w')
    for i in save:
        a.write(str(i)+'\n')

    a.close()
    print(f'complete, file_number:{n}, took {time.time()-Firsttime}sec')

if __name__ == '__main__':
    space = make_space((1000, 1000))
    b = 1
    space = make_walls(space, [[[0, 0], [950, 50], [0, 0], b], 
                                [[0, 50], [50, 650], [0, 0], b], 
                                [[950, 0], [1000, 650], [0, 0], b], 
                                [[50, 600], [450, 650], [0, 0], b], 
                                [[550, 600], [950, 650], [0, 0], b],  
                                [[0, 650], [370, 1500], [0, 0], b], 
                                [[630, 650], [1000, 1500], [0, 0], b], 
                                [[370, 970], [630, 1000], [0, 0], b]])

    space = make_particles(space, 3, 10, 1, 100)
    run_program(lambda a, b:0, space, 500, 0.998)
