#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def power(h, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * h
    return s
o = (float(input('底数：')),float(input('指数:'))) # o = float(input('\'#请用逗号隔开\'底数,指数:'))
print(power(o))
