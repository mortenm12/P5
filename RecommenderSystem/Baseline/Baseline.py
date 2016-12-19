import DataAPI
import math
import time

"return an array with all the users average ratings"
def calculate_user_average_rating(movies, ratings, users, all_average):
    user_average_array = []

    for user in range(len(users)):
        i = 0
        sum1 = 0
        for movie in range(len(movies)):
            if ratings[user][movie] != 0:
                sum1 += ratings[user][movie]
                i += 1
        if i != 0:
            user_average_array.insert(user, sum1 / i)

        else:
            user_average_array.insert(user, all_average)


    return user_average_array

#returns an array of all the movie average ratings
def calculate_movie_average_rating(movies, ratings, users, all_average):
    average_array = []

    for movie in range(len(movies)):
        i = 0
        sum1 = 0
        for user in range(len(users)):
            if ratings[user][movie] > 0:
                sum1 += ratings[user][movie]
                i += 1
        if i != 0:
            average_array.insert(movie, sum1 / i)
        else:
            average_array.insert(movie, all_average)

    return average_array

#returens the average of all the ratings
def calculate_all_average(users, movies, ratings):
    i = 0
    sum1 = 0
    for user in users:
        for movie in movies:
            if ratings[user - 1][movie - 1] > 0:
                i += 1
                sum1 += ratings[user - 1][movie - 1]
    print(sum1/i)
    return sum1 / i




#runs all the average function, the weight matrix and the ratings, and writing all the ratings to an output file
for x in range(1, 6):
    directory = "Test" + str(x)

    users = DataAPI.read_users_as_id_list()
    movies = DataAPI.read_movies_as_id_list()
    ratings = DataAPI.read_ratings(directory)

    i = 0
    rated = ratings
    all_average = calculate_all_average(users, movies, ratings)
    user_average_array = calculate_user_average_rating(movies, ratings, users, all_average)
    movie_average_array = calculate_movie_average_rating(movies, ratings, users, all_average)


    for user in users:
        i += 1


        for movie in movies:
            if ratings[user - 1][movie - 1] == 0.0:
                rated[user - 1][movie - 1] = user_average_array[user-1] + movie_average_array[movie - 1] - all_average

    for user in users:
        for movie in movies:
            if rated[user - 1][movie - 1] > 5:
                rated[user - 1][movie - 1] = 5
            elif rated[user - 1][movie - 1] < 1:
                rated[user - 1][movie - 1] = 1

    output = open("Output/Test" + str(x) + "/ratings.data", "w")
    output.write("   ID, ")
    for movie in movies:
        output.write("{:>5}".format(movie) + (", " if movie < len(movies) else ""))

    i = 0
    output.write("\n")

    for user in users:
        i += 1

        output.write("{:>5}".format(user) + ", ")
        for movie in movies:
            output.write("{: .2f}".format(rated[user - 1][movie - 1]) + (", " if movie < len(movies) else ""))

        output.write("\n")

    if not output.closed:
        output.close()