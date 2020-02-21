#!/usr/bin/env python3
# -*- coding: utf-8 -*-

names = ['11', '22', '33']
for name in names:
    print(name)

sum = 0
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    sum = sum + x
print(sum)

sul = 0
for x in range(101):
    sul = sul + x
print(sul)

sun = 0
n = 99
while n > 0:
    sun = sun + n
    n = n - 2
print(sun)

L = ['Bart', 'Lisa', 'Adam']
for bzd in L:
    print(bzd)

b = 1
while b < 100:
    if b > 10:  # 当b = 11时，条件满足，执行break语句
        break  # break语句会结束当前循环
    print(b)
    b = b + 1
print('END')

B = 0
while B < 10:
    B = B + 1
    if B % 2 == 0:  # 如果n是偶数，执行continue语句
        continue  # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(B)

K = 1
while K > 0:
    K = K + 1
    print(K)

d = {'111': 111, '222': 222, '333': 333 }
d['333']
d['333'] = 666
d['333']
'444' in d
d.get('444')
d.get('444',-100)
d.pop('333')
d

o = '111'
g = {o: 111,'222': 222,'333': 333}
g[o]

q = ['111','222','333']
u = set(q)
u
u.add(444)
u
u.remove(444)
u
u1 = {'222','333','444'}
u & u1
u | u1

a = 'abc'
a.replace('a','A')
a

j = (11,22,33)
J = {'44': 44,'55': 55}
J['44'] = j
J
e = set(j)
e
w = (1,[2,3])
J['55'] = w
J
s = set(w)
s

print(hex(255))
hex(1000)

f = int(input('abs:'))
def know(F):
    if not isinstance(F,(int,float)):
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
r = move(100,100,60,math.pi / 6)
print(x,y)
# stop

