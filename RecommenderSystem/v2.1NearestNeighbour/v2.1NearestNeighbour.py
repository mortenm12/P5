import DataAPI
import math
import time




def cos(a, b):
    sum = 0

    if len(a) == len(b):
        for i in range(len(a)):
            sum += a[i] * b[i]
    else:
        raise Exception("a and b must be of the same length")

    if len(a) != 0 and len(b) != 0:
        return sum / (length(a) * length(b))
    else:
        return 0


def length(vector):
    sum = 0

    for i in range(len(vector)):
        sum += math.pow(vector[i], 2)

    return math.sqrt(sum)


def weight(user1, user2, ratings, movies, user_average_array):
    movie_ratings = [[],[]]

    for movie in movies:
        if ratings[user1 - 1][movie - 1] != 0.0 and ratings[user2 - 1][movie - 1] != 0.0:
            movie_ratings[0].append(ratings[user1 - 1][movie - 1] - (user_average_array[user1 - 1] - all_average))
            movie_ratings[1].append(ratings[user2 - 1][movie - 1] - (user_average_array[user2 - 1] - all_average))

    return cos(movie_ratings[0], movie_ratings[1])


def k_nearest_neighbour(movie, user1, k, ratings, users, weight_matrix, user_average_array):
    weight_rating_tuples = []
    for user2 in users:
        if user2 != user1 and ratings[user2 - 1][movie - 1] != 0.0:
            weight_rating_tuples.append([weight_matrix[user1 - 1][user2 - 1], ratings[user2 - 1][movie - 1] - user_average_array[user2 - 1]])

    sorted_array = sorted(weight_rating_tuples, key=lambda x: x[0])
    return sorted_array[-k:]


def rate(movie, user, users, ratings, weight_matrix, user_average_array, movie_average_array, all_average):
    k = 40
    weight_rating_tuples = k_nearest_neighbour(movie, user, k, ratings, users, weight_matrix, user_average_array)
    sum1 = 0
    sum2 = 0
    if len(weight_rating_tuples) == 0:

        return all_average + (user_average_array[user - 1] - all_average) + (movie_average_array[movie - 1] - all_average)

    for x in weight_rating_tuples:
        sum1 += x[0] * x[1]
        sum2 += x[0]
    if sum2 != 0:
        return (sum1/sum2) + user_average_array[user - 1]
    else:
        return sum1 + user_average_array[user - 1]


def format_time(t):
    if t < 1:
        return "00:00:00"
    else:
        t_int = int(t)
        h = t_int / 3600
        h_rest = t_int % 3600
        m = h_rest / 60
        s = h_rest % 60
        return "{:02d}".format(int(h)) + ":" + "{:02d}".format(int(m)) + ":" + "{:02d}".format(int(s))


def calculate_weight_matrix(movies, ratings, users, x, average_array):
    t_start = time.time()
    weight_matrix = []
    for i in range(len(movies)):
        weight_matrix.append([])
        for j in range(len(movies)):
            weight_matrix[i].append(0)

    for user1 in users:
        t_current = time.time()
        t_elapsed = t_current - t_start
        t_remaining = (t_elapsed * len(movies)) / user1 - t_elapsed
        print(x, " Calculating Weight", round((user1 / len(users)) * 100, 1), "% tid brugt: ", format_time(t_elapsed), " tid tilbage: ",
              format_time(t_remaining))
        for user2 in users:
            if user1 != user2:
                weight_matrix[user1 - 1][user2 - 1] = weight(user1, user2, ratings, movies, average_array)

    return weight_matrix


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
    weight_matrix = calculate_weight_matrix(movies, ratings, users, x, user_average_array)
    starting_time = time.time()
    for user in users:
        i += 1

        current_time = time.time()
        elapsed_time = current_time - starting_time
        remaining_time = ((elapsed_time * len(users)) / i) - elapsed_time

        print(x, " Rater", round((i / len(users)) * 100, 1), "% tid brugt: ", format_time(elapsed_time), " tid tilbage: ", format_time(remaining_time))

        for movie in movies:
            if ratings[user - 1][movie - 1] == 0.0:
                rated[user - 1][movie - 1] = (rate(movie, user, users, ratings, weight_matrix, user_average_array, movie_average_array, all_average))

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
        print("Writing", round((i / len(users)) * 100, 1), "%")
        output.write("{:>5}".format(user) + ", ")
        for movie in movies:
            output.write("{: .2f}".format(rated[user - 1][movie - 1]) + (", " if movie < len(movies) else ""))

        output.write("\n")

    if not output.closed:
        output.close()