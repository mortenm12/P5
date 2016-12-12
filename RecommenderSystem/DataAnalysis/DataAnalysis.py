from DataAPI import read_movies_as_object_list, read_users_as_object_list, read_ratings


# Calculates the amount of ratings and the average rating for each movie.
def calculate_rating_amount(movies, ratings):
    movie_ratings = []
    for j in range(len(ratings[0])):
        movie_ratings.append(0)
    for i in range(0, len(ratings)):
        for j in range(0, len(ratings[0])):
            if ratings[i][j] > 0.0:
                movies[j].number_of_ratings += 1
                movie_ratings[j] += ratings[i][j]
    for j in range(len(ratings[0])):
        if not movie_ratings[j] == 0:
            movies[j].average_rating = float(float(movie_ratings[j]) / float(movies[j].number_of_ratings))
        else:
            movies[j].average_rating = 0.0
    return movies


# Splits the movies into head and tail. OUTDATED!
def calculate_head_and_tail(movies):
    sorted_movies = movies.copy()
    sorted_movies.sort(key=lambda x: x.number_of_ratings, reverse=True)
    split = sorted_movies[80].number_of_ratings
    head = [x for x in sorted_movies if x.number_of_ratings >= split]
    tail = [x for x in sorted_movies if x.number_of_ratings < split]
    return head, tail


# Calculates the average rating for a user as well as the mount of ratings in both head and tail.
def calculate_users_rating_habits(users, ratings, head, tail):
    for user in users:
        sum = 0
        for movie in head:
            if ratings[user.id - 1][movie.id - 1] > 0.0:
                user.ratings_in_head += 1
                sum += ratings[user.id-1][movie.id - 1]
        for movie in tail:
            if ratings[user.id - 1][movie.id - 1] > 0.0:
                user.ratings_in_tail += 1
                sum += ratings[user.id - 1][movie.id - 1]
        if not sum == 0:
            user.average_rating = sum / user.total_ratings()
        else:
            user.average_rating = 0.0

    sorted_users = users.copy()
    sorted_users.sort(key=lambda x: x.percent_ratings_in_tail(), reverse=True)
    return users, sorted_users


# Writes users rating habits, head and tail to files.
def write_results_to_files(users, head, tail):
    result = open("FinalData/UserRatingDistribution.Data", "w", encoding='iso_8859_15')
    for user in users:
        result.write("|".join([str(user.id), str(user.ratings_in_head), str(user.ratings_in_tail), "{}".format(user.percent_ratings_in_tail())]) + '\n')
    if not result.closed:
        result.close()

    head_file = open("FinalData/Head.Data", "w", encoding='iso_8859_15')
    for movie in head:
        head_file.write("|".join([str(movie.id), str(movie.name), str(movie.number_of_ratings)]) + '\n')
    if not head_file.closed:
        head_file.close()

    tail_file = open("FinalData/Tail.Data", "w", encoding='iso_8859_15')
    for movie in tail:
        tail_file.write("|".join([str(movie.id), str(movie.name), str(movie.number_of_ratings)]) + '\n')
    if not tail_file.closed:
        tail_file.close()


# Calculates the average rating of a rating matrix R.
def calculate_average_rating(R):
    sum = 0
    amount = 0
    for i in range(len(R)):
        for j in range(len(R[0])):
            if R[i][j] > 0.0:
                sum += R[i][j]
                amount += 1

    return sum / float(amount)


# Calculates the bias for all users in U given the global average.
def calculate_user_bias(U, average):
    for user in U:
        user.bias = user.average_rating - average
    return U


# Calculates the bias for all movies in M given the global average.
def calculate_movie_bias(M, average):
    for movie in M:
        movie.bias = movie.average_rating - average
    return M


# Calculates a bunch of stuff.
def calculate_extra_data(movies, users, ratings):
    movies = calculate_rating_amount(movies, ratings)
    head, tail = calculate_head_and_tail(movies)
    users, Sort_U = calculate_users_rating_habits(users, ratings, head, tail)
    average = calculate_average_rating(ratings)
    users = calculate_user_bias(users, average)
    movies = calculate_movie_bias(movies, average)
    return users, movies, ratings


# A main function to start calculating everything.
def __main__():
    R = read_ratings("FullData")
    U = read_users_as_object_list()
    M = read_movies_as_object_list()
    M = calculate_rating_amount(M, R)
    head, tail = calculate_head_and_tail(M)
    U, Sort_U = calculate_users_rating_habits(U, R, head, tail)
    average = calculate_average_rating(R)
    U = calculate_user_bias(U, average)
    calculate_movie_bias(M, average)

    file = open("user_rating_habits.data", "w")

    for user in U:
        file.write(",".join([str(user.id), str(average + user.bias), str(user.percent_ratings_in_tail())]) + "\n")

    if not file.closed:
        file.close()
