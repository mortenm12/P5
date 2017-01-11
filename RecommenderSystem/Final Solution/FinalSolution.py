from v21NearestNeighbour import KNN
import DataAPI
from ContentBased import calculate_recommendation_matrix
from PrecisionRecall import average_precision_recall
import Evaluation


# Algorithm to write a result matrix to a file.
def write_matrix(m, file_name, test_set):
    file = open("Output/" + test_set + "/" + file_name, "w")
    file.write(" ID  , " + ", ".join(str(x) for x in range(1, len(m[0]) + 1)) + "\n")
    for i in range(0, len(m)):
        file.write("{:>5d}, ".format(i + 1))
        file.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        file.write("\n")

    if not file.closed:
        file.close()


def log(evaluation_result, x):
    file = open("EvaluationLog.txt", "a")
    file.write(str(x) + ":" + str(evaluation_result) + "\n")

    if not file.closed:
        file.close()


def is_relevant(rating, User, Movie):
    if rating == 0:
        return None
    elif rating >= 4:
        return True
    else:
        return False


def get_head_and_tail(k, users, movies, ratings):
    head_movies = []
    tail_movies = []

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


def recommend(usernr, old_ratings, movies, new_ratings, k, head_movies, tail_movies):
    head_percent, tail_percent = division(usernr, head_movies, tail_movies, movies, old_ratings)

    head_tuple = []
    for movie in head_movies:
        if not old_ratings[usernr][movie] > 0:
            head_tuple.append([new_ratings[usernr][movie], movie])

    head_tuple.sort(key=lambda x: x[0], reverse=True)

    tail_tuple = []
    for movie in tail_movies:
        if not old_ratings[usernr][movie] > 0:
            tail_tuple.append([new_ratings[usernr][movie], movie])

    tail_tuple.sort(key=lambda x: x[0], reverse=True)

    return_array = []

    if k > len(tail_tuple) + len(head_tuple):
        k = len(tail_tuple) + len(head_tuple)

    limit = int(round(head_percent*k, 0))

    if len(head_tuple) == 0 and len(tail_tuple) == 0:
        pass
    elif len(head_tuple) == 0:
        for i in range(k):
            return_array.append(tail_tuple[i][1])
    elif len(tail_tuple) == 0:
        for i in range(k):
            return_array.append(head_tuple[i][1])
    else:
        j = 0
        for i in range(k):
            if i + 1 <= limit:
                return_array.append(head_tuple[i][1])
            elif i + 1 > limit:
                return_array.append(tail_tuple[j][1])
                j += 1
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


def do_hybrid_recommendation(test_set):
    users = DataAPI.read_users_as_id_list()
    movies = DataAPI.read_movies_as_id_list()
    ratings = DataAPI.read_ratings(test_set)

    # Do K-Nearest Neigbour
    #KNN(test_set)
    head_ratings = DataAPI.read_recommendation_matrix("v2.1NearestNeighbour", test_set)

    # Do Content Based
    #calculate_recommendation_matrix(test_set)
    tail_ratings = DataAPI.read_recommendation_matrix("Weighted Content Based", test_set)

    # Merge results
    head_movies, tail_movies = get_head_and_tail(41, users, movies, ratings)
    new_ratings = merge(head_movies, tail_movies, head_ratings, tail_ratings, users)

    write_matrix(new_ratings, "ratings.data", test_set)

    for i in [1, 5, 10, 20, 30, 40]:
        # Generate recommendations
        recommendations = []
        for user in range(0, len(users)):
            recommendations.insert(user, recommend(user, ratings, movies, new_ratings, i, head_movies, tail_movies))
            # print(user, ":", recommendations[user - 1])

        log("N = " + str(i), "")
        log(average_precision_recall(recommendations, is_relevant), test_set[-1])

#    return recommendations


# Running the Hybrid Recommender on the full Dataset
for i in range(1, 6):
    do_hybrid_recommendation("Test" + str(i))
#evaluation_algorithms = [
#    (Evaluation.EvaluationAlgorithm.prefabs["MAE"], None),
#    (Evaluation.EvaluationAlgorithm.prefabs["RMSE"], None),
#    (Evaluation.EvaluationAlgorithm.prefabs["MRSRMSE"], (0, 49)),
#    (Evaluation.EvaluationAlgorithm.prefabs["MRSRMSE"], (50, 100000))
#]
#evaluator = Evaluation.RatingEvaluator(["Final Solution"], [1, 2, 3, 4, 5], evaluation_algorithms)
#evaluator.evaluate_all_algorithms()
#evaluator.log_results("Final Solution")