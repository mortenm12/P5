from DataAPI import read_movies_as_object_list, read_users_as_object_list, read_ratings


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
        movies[j].average_rating = float(float(movie_ratings[j]) / float(movies[j].number_of_ratings))
    return movies


def calculate_head_and_tail(movies):
    sorted_movies = movies.copy()
    sorted_movies.sort(key=lambda x: x.number_of_ratings, reverse=True)
    split = sorted_movies[80].number_of_ratings
    head = [x for x in sorted_movies if x.number_of_ratings >= split]
    tail = [x for x in sorted_movies if x.number_of_ratings < split]
    return head, tail


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
        user.average_rating = sum / user.total_ratings()

    sorted_users = users.copy()
    sorted_users.sort(key=lambda x: x.percent_ratings_in_tail(), reverse=True)
    return users, sorted_users


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


def calculate_average_rating(R):
    sum = 0
    amount = 0
    for i in range(len(R)):
        for j in range(len(R[0])):
            if R[i][j] > 0.0:
                sum += R[i][j]
                amount += 1

    return sum / float(amount)


def calculate_user_bias(U, average):
    for user in U:
        user.bias = user.average_rating - average
    return U


def calculate_movie_bias(M, average):
    for movie in M:
        movie.bias = movie.average_rating - average
    return M

U = read_users_as_object_list()
M = read_movies_as_object_list()
R = read_ratings("FullData")

M = calculate_rating_amount(M, R)
Head, Tail = calculate_head_and_tail(M)
U, Sort_U = calculate_users_rating_habits(U, R, Head, Tail)

average = calculate_average_rating(R)
U = calculate_user_bias(U, average)
M = calculate_movie_bias(M, average)

file = open("user_rating_habits.data", "w")

for user in U:
    file.write(",".join([str(user.id), str(average + user.bias), str(user.percent_ratings_in_tail())]) + "\n")

if not file.closed:
    file.close()
