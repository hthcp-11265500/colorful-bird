#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def power(h,n): # 1
    s = 1
    while n > 0:
        n = n - 1
        s = s * h
    return h * h

def quadratic(a,b,c):
    if x == ((-b+math.sqrt(b*b-4*a*c)) / 2*a):
        ax = a * power(x)
        bx = b * x
        cx = c
    return ax,bx,cx

def power(h, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * h
    return s
o = (float(input('底数：')),float(input('指数:'))) # o = float(input('\'#请用逗号隔开\'底数,指数:'))
print(power(o))

def enroll(name,gender,age=6,city='Beijing'):
    print('name:',name)
    print('gender:',gender)
    print('age:',age)
    print('city:',city)

def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
