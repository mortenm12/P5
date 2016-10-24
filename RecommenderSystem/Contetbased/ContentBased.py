import DataAPI
import math
import time

directory = "Test1Target"

userDict = {}
movieDict = {}
ratings = []

ratings, userDict, movieDict = DataAPI.read_ratings(directory)


def cos(a, b):
    sum1 = 0

    if len(a) == len(b):
        for i in range(len(a)):
            sum1 += a[i] * b[i]
    else:
        raise Exception("a and b must be of the same lenght")

    if len(a) != 0:
        return sum1 / (length(a) * length(b))
    else:
        return 0


def length(v):
    sum1 = 0

    for i in range(len(v)):
        sum1 += v[i] ** 2

    return math.sqrt(sum1)


def weight(mId1, mId2, ratings, userdict):
    userratings = [[],[]]

    for uId in range(len(userdict)):
        if ratings[uId][mId1] != 0.0 and ratings[uId][mId2] != 0.0:
            userratings[0].append(ratings[uId][mId1])
            userratings[1].append(ratings[uId][mId2])

    return cos(userratings[0], userratings[1])


def knn(mid1, uid, k, userdict, moviedict, ratings):
    weightandrating = []
    for mid2 in range(len(moviedict)):
        if mid2 != mid1 and ratings[uid][mid2] != 0.0:
            weightandrating.append([weight(mid1, mid2, ratings, userdict), ratings[uid][mid2]])

    sortedarray = sorted(weightandrating, key=lambda x: x[0])
    return sortedarray[-k:]


def rate(mid, uid, userdict, moviedict, ratings):
    knearesteneighour = knn(mid, uid, 5, userdict, moviedict, ratings)
    sum1 = 0
    sum2 = 0
    for x in knearesteneighour:
        sum1 += x[0] * x[1]
        sum2 += x[0]
    if sum2 != 0:
        return sum1/sum2
    else:
        return sum1


def totime(time):
    if time < 1:
        return "0:0:0"
    else:
        h = round(time / 3600)
        m = round((time - (h * 3600)) / 60)
        s = round(time % 60)
        return str(h) + ":" + str(m) + ":" + str(s)


tidstart = time.time()

i = 0
rated = ratings
for user in range(len(userDict)):
    i += 1

    tidnu = time.time()
    tidbrugt = tidnu - tidstart
    tidtilbage = ((tidbrugt * len(userDict)) / i) - tidbrugt

    print(round((i / len(userDict)) * 100, 1), "% tid brugt: ", totime(tidbrugt), " tid tilbage: ", totime(tidtilbage) )

    for movie in range(len(movieDict)):
        if ratings[user][movie] == 0.0:
            rated[user][movie] = (rate(movie, user, userDict, movieDict, ratings))


output = open("output.data", "w")
output.write("   ID, ")
for movie in range(len(movieDict)):
    output.write("{:>5}".format(movie) + ", ")

i = 0
output.write("\n")

for user in range(len(userDict)):
    i += 1
    print(round((i / len(userDict)) * 100, 1), "%")
    output.write("{:>5}".format(user) + ", ")
    for movie in range(len(movieDict)):
        output.write("{: .2f}".format(rated[user][movie]) + ", ")

    output.write("\n")

if not output.closed:
    output.close()
