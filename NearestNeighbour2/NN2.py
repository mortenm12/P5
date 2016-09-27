import math

def cos(a,b):
    return dot(a,b) / (lenght_of_vector(a) * lenght_of_vector(b))

def dot(a,b):
    summer = 0
    if len(a) == len(b):
        for x in range(len(a)):
            summer += a[x] * b[x]
        return summer
    else:
        raise IndexError("a and b should be the same length.")

def lenght_of_vector(a):
    summer = 0

    for x in a:
        summer += x ** 2

    return math.sqrt(summer)

def rating(w,r):
    summer = 0
    if len(w) == len(r):
        for i in range(len(w)):
            summer += w[i] * r[i]
    else:
        raise IndexError("w and r should be equal.")
    return summer / sum(w)

lw = cos([2,3,5,4],[1,2,5,5])
dw = cos([2,3,5],[4,5,3])

print("Lucy and Eric: ", lw)
print("Diane and Eric: ", dw)
print("Erics rating for titanic is: ", rating([lw,dw],[5,3]))

