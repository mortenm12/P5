import DataAPI
import math
import time

directory = "Test1Target"

users = DataAPI.read_users_as_id_list(directory)
movies = DataAPI.read_movies_as_id_list(directory)
ratings = DataAPI.read_ratings(directory)


def cos(a, b):
    sum = 0

    if len(a) == len(b):
        for i in range(len(a)):
            sum += a[i] * b[i]
    else:
        raise Exception("a and b must be of the same length")

    if len(a) != 0:
        return sum / (length(a) * length(b))
    else:
        return 0


def length(vector):
    sum = 0

    for i in range(len(vector)):
        sum += vector[i] ** 2

    return math.sqrt(sum)


def weight(movie1, movie2, ratings, users):
    user_ratings = [[],[]]

    for user in users:
        if ratings[user - 1][movie1 - 1] != 0.0 and ratings[user - 1][movie2 - 1] != 0.0:
            user_ratings[0].append(ratings[user - 1][movie1 - 1])
            user_ratings[1].append(ratings[user - 1][movie2 - 1])

    return cos(user_ratings[0], user_ratings[1])


def k_nearest_neighbour(movie1, user, k, ratings, movies, users):
    weight_rating_tuples = []
    for movie2 in movies:
        if movie2 != movie1 and ratings[user - 1][movie2 - 1] != 0.0:
            weight_rating_tuples.append([weight(movie1, movie2, ratings, users), ratings[user - 1][movie2 - 1]])

    sorted_array = sorted(weight_rating_tuples, key=lambda x: x[0])
    return sorted_array[-k:]


def rate(movie, user, users, movies, ratings):
    weight_rating_tuples = k_nearest_neighbour(movie, user, 5, ratings, movies, users)
    sum1 = 0
    sum2 = 0
    for x in weight_rating_tuples:
        sum1 += x[0] * x[1]
        sum2 += x[0]
    if sum2 != 0:
        return sum1/sum2
    else:
        return sum1


def format_time(time):
    if time < 1:
        return "0:0:0"
    else:
        h = round(time / 3600)
        m = round((time - (h * 3600)) / 60)
        s = round(time % 60)
        return str(h) + ":" + str(m) + ":" + str(s)


starting_time = time.time()

i = 0
rated = ratings
for user in users:
    i += 1

    current_time = time.time()
    elapsed_time = current_time - starting_time
    remaining_time = ((elapsed_time * len(users)) / i) - elapsed_time

    print(round((i / len(users)) * 100, 1), "% tid brugt: ", format_time(elapsed_time), " tid tilbage: ", format_time(remaining_time))

    for movie in movies:
        if ratings[user - 1][movie - 1] == 0.0:
            rated[user - 1][movie - 1] = (rate(movie, user, users, movies, ratings))


output = open("output.data", "w")
output.write("   ID, ")
for movie in movies:
    output.write("{:>5}".format(movie) + ", ")

i = 0
output.write("\n")

for user in users:
    i += 1
    print(round((i / len(users)) * 100, 1), "%")
    output.write("{:>5}".format(user) + ", ")
    for movie in movies:
        output.write("{: .2f}".format(rated[user - 1][movie - 1]) + ", ")

    output.write("\n")

if not output.closed:
    output.close()
