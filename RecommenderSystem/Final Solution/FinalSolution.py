from v21NearestNeighbour import KNN
import DataAPI
from ContentBased import calculate_recommendation_matrix
from PrecisionRecall import AveragePrecisionRecall


def log(evaluation_result):
    file = open("EvaluationLog.txt", "a")
    file.write(evaluation_result)

    if not file.closed:
        file.close()


def is_relevant(rating):
    if rating == 0:
        return None
    elif rating >= 4:
        return True
    else:
        return False


def get_head_and_tail(k, directory):
    head_movies = []
    tail_movies = []

    users = DataAPI.read_users_as_id_list()
    movies = DataAPI.read_movies_as_id_list()
    ratings = DataAPI.read_ratings(directory)

    for j in range(0, len(movies)):
        sum1 = 0
        for i in range(0, len(users)):
            if ratings[i][j] > 0.0:
                sum1 += 1

        if sum1 >= k:
            head_movies.append(j)
        else:
            tail_movies.append(j)

    return head_movies, tail_movies


def merge(head_movies, tail_movies, head_ratings, tail_ratings, users):
    ratings = []

    for i in range(0, len(users)):
        ratings.append([])
        for j in range(0, len(head_movies) + len(tail_movies)):
            ratings[i].append(0.0)

    for i in range(0, len(users)):
        for j in head_movies:
            ratings[i][j] = head_ratings[i][j]

        for j in tail_movies:
            ratings[i][j] = tail_ratings[i][j]

    return ratings


def recommend(usernr, old_ratings, movies, new_ratings, users, k, test_set):
    head_movies, tail_movies = get_head_and_tail(80, test_set)
    head_percent, tail_percent = division(usernr, head_movies, tail_movies, movies, old_ratings)

    for user in range(0, len(users)):
        for movie in range(0, len(movies)):
            if old_ratings[user][movie] > 0.0:
                new_ratings[user][movie] = 0.0

    head_tuple = []
    for movie in head_movies:
        head_tuple.append([new_ratings[usernr][movie], movie])

    head_tuple.sort(key=lambda x: x[0], reverse=True)

    tail_tuple = []
    for movie in tail_movies:
        tail_tuple.append([new_ratings[usernr][movie], movie])

    tail_tuple.sort(key=lambda x: x[0], reverse=False)

    return_array = []

    for i in range(0, int(round(head_percent * k, 0))):
        return_array.append(head_tuple[i][1])

    for i in range(0, int(round(tail_percent * k, 0))):
        return_array.append(tail_tuple[i][1])

    return return_array


def division(usernr, head_movies, tail_movies, movies, ratings):
    head = 0
    tail = 0
    sum1 = 0

    for movie in range(len(movies)):
        if ratings[usernr][movie] > 0.0:
            sum1 += 1
            if movie in head_movies:
                head += 1

            elif movie in tail_movies:
                tail += 1

            else:
                raise ValueError("well, fuck")

    if head + tail == sum1 and sum1 > 0:
        return head/sum1, tail/sum1

    else:
        return 0.5, 0.5


def do_hybrid_recommendation(test):
    test_set = "Test" + str(test)
    users = DataAPI.read_users_as_id_list()
    movies = DataAPI.read_movies_as_id_list()
    ratings = DataAPI.read_ratings(test_set)

    # Do K-Nearest Neigbour
    KNN(test)
    head_ratings = DataAPI.read_recommendation_matrix("v2.1NearestNeighbour", test_set)

    # Do Content Based
    calculate_recommendation_matrix(test_set)
    tail_ratings = DataAPI.read_recommendation_matrix("Weighted Content Based", test_set)

    # Merge results
    head_movies, tail_movies = get_head_and_tail(41, test_set)
    new_ratings = merge(head_movies, tail_movies, head_ratings, tail_ratings, users)

    # Generate recommendations
    recommendations = []
    for user in range(0, len(users)):
        recommendations.insert(user, recommend(user, ratings, movies, new_ratings, users, 10, test_set))
        print(user, ":", recommendations[user - 1])

    return recommendations

for i in [1, 2, 3, 4, 5]:
    recommendations = do_hybrid_recommendation(i)
    result = AveragePrecisionRecall(recommendations, is_relevant)
    print(result)
    log(result)
