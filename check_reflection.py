#반사
import function as f
space = f.make_space((1000, 1000))
b = 1
space = f.make_walls(space, [[[-5, -5], [0, 1005], [0, 0], b], 
                             [[-5, -5], [1005, 0], [0, 0], b], 
                             [[1000, -5], [1005, 1005], [0, 0], b], 
                             [[-5, 1000], [1005, 1005], [0, 0], b], 
                             [[-5, 750], [0, 850], [0, 0], b], 
                             [[0, 845], [100, 850], [0, 0], b], 
                             [[0, 0], [1000, 500], [0, 0], b]])
space = f.make_particles(space, 0.1, 15, 1, 10000)
space[2][6] = [[0, 500], [1000, 1000], [0, 0], b]
space = f.make_particles(space, 0.05, 20, 10, 10000)
del space[2][6]
def myfunction(time, s, moving):
    if time == 35:
        del s[2][5]
        del s[2][4]

    elif 35 > time > 15:
        s[2][4][2] = moving[:]
        s[2][5][2] = moving[:]

a = [[3, -3], [3, -6], [6, -3]]

for i in range(3):
    print(f'{i+1} / 3')
    f.run_program(lambda t, s:myfunction(t, s, a[i]), space, 250, 0.985)
