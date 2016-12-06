from splitting import *
from v2NearestNeighbour import KNN
import DataAPI
from ContentBased import calculate_recommendation_matrix
from Division import recommend
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


def do_hybrid_recommendation(test):
    test_set = "Test" + str(test)
    users = DataAPI.read_users_as_id_list()
    movies = DataAPI.read_movies_as_id_list()
    ratings = DataAPI.read_ratings(test_set)

    # Do K-Nearest Neigbour
    KNN(test)
    head_ratings = DataAPI.read_recommendation_matrix("v2.0NearestNeighbour", test_set)

    # Do Content Based
    calculate_recommendation_matrix(test_set)
    tail_ratings = DataAPI.read_recommendation_matrix("Weighted Content Based", test_set)

    # Merge results
    head_movies, tail_movies = get_head_and_tail(41)
    new_ratings = merge(head_movies, tail_movies, head_ratings, tail_ratings, users)

    # Generate recommendations
    recommendations = []
    for user in range(0, len(users)):
        recommendations.insert(user, recommend(user, ratings, movies, new_ratings, users, 10))
        print(user, ":", recommendations[user - 1])

    return recommendations

for i in [1, 2, 3, 4, 5]:
    recommendations = do_hybrid_recommendation(i)
    result = AveragePrecisionRecall(recommendations, is_relevant)
    print(result)
    log(result)
