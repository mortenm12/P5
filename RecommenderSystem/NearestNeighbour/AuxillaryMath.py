import math


# a and b is a vector of the same dimensions
# the output is a number between 0 and 1 where 1 is an index of that the two vectors is parallel
def cos(a, b): # page 124
    if lenght_of_vector(a) * lenght_of_vector(b) == 0:
        return 0
    return dot(a,b) / (lenght_of_vector(a) * lenght_of_vector(b))


# a and b is a vector of the same dimensions
# the output is a scalar between a and b
def dot(a, b):
    sum1 = 0
    if len(a) == len(b):
        for x in range(len(a)):
            sum1 += a[x] * b[x]
        return sum1
    else:
        raise IndexError("a and b should be the same length.")


# a is vector
# the output is the lenght og vector a
def lenght_of_vector(a):
    sum1 = 0

    for x in a:
        sum1 += x ** 2

    return math.sqrt(sum1)