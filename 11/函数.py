f = int(input('abs:'))
def know(F):
    if not isinstance(F, (int, float)):
        raise TypeError('bad operand type')
    if F > 0:
        return F
    else:
        return -F
print(know(f))

def nop():
    pass

import math

def move(x,y,step,angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx,ny
x,y = move(100,100,60,math.pi / 6) # x,y = r
print(x,y) # print(r)

import math
def power(h):
    return h * h

def quadratic(a,b,c):
    if x == ((-b+math.sqrt(b*b-4*a*c)) / 2*a):
        ax = a * power(x)
        bx = b * x
        cx = c
    return ax,bx,cx


    
        