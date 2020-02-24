o = int(input('底数:'))
p = int(input('指数:'))
def power(h, n=2): # 2
    s = 1
    while n > 0:
        n = n - 1
        s = s * h
    return s
print(power(o,p))
