from DataAPI import read_movies_as_object_list, read_users_as_object_list, read_ratings


def calculate_rating_amount(movies, ratings):
    for i in range(0, len(ratings)):
        for j in range(0, len(ratings[0])):
            if ratings[i][j] > 0.0:
                movies[j].number_of_ratings += 1
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
        for movie in head:
            if ratings[user.id - 1][movie.id - 1] > 0.0:
                user.ratings_in_head += 1
        for movie in tail:
            if ratings[user.id - 1][movie.id - 1] > 0.0:
                user.ratings_in_tail += 1

    sorted_users = users.copy()
    sorted_users.sort(key=lambda x: x.percent_ratings_in_tail(), reverse=True)
    return sorted_users


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

movies = read_movies_as_object_list()
users = read_users_as_object_list()
ratings = read_ratings("FinalData")
movies = calculate_rating_amount(movies, ratings)
head, tail = calculate_head_and_tail(movies)
users = calculate_users_rating_habits(users, ratings, head, tail)
write_results_to_files(users, head, tail)
