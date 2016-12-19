import DataAPI
import PrecisionRecall
import numpy


R = numpy.array(PrecisionRecall.AllRatings)
ratingsPerMovie = numpy.sum(numpy.sign(R), 0)


def in_tail(rating, user, movie):
    if ratingsPerMovie[movie] < 42:
        return True
    else:
        return False


def i_to_algo(i):
    if i == 0:
        return "KNN PC, K=40"
    elif i == 1:
        return "CB Imp"
    elif i == 2:
        return "CB"
    elif i == 3:
        return "MF no bias, K=20"
    else:
        return ""


def log(str):
    file.write(str + "\n")
    print(str)


def is_relevant(rating, User, Movie):
    if rating == 0:
        return None
    elif rating >= 4:
        return True
    else:
        return False


def recommend(user, old_ratings, movies, new_ratings, k):
    tuples = []
    for movie in movies:
        if not old_ratings[user-1][movie-1] > 0:
            tuples.append([new_ratings[user-1][movie-1], movie])

    tuples.sort(key=lambda x: x[0], reverse=True)

    return_array = []

    if k > len(tuples):
        k = len(tuples)

    for i in range(k):
        return_array.append(tuples[i][1])

    return return_array

users = DataAPI.read_users_as_id_list()
movies = DataAPI.read_movies_as_id_list()
old_ratings = []
KNN_PC_ratings = []
CB_imp_ratings = []
#CB_ratings = []
#MF_ratings = []
for i in range(5):
    set = "Test" + str(i+1)
    print("Reading ratings for Test set " + str(i+1))
    old_ratings.append(DataAPI.read_ratings(set))
    KNN_PC_ratings.append(DataAPI.read_recommendation_matrix("Results/KNN/PC/K=40", set))
    CB_imp_ratings.append(DataAPI.read_recommendation_matrix("Results/CB/Improved", set))
    #CB_ratings.append(DataAPI.read_recommendation_matrix("Results/CB/Weighted", set))
    #MF_ratings.append(DataAPI.read_recommendation_matrix("Results/MF/Non Bias/K=20", set))


for x in [1, 5, 10, 20, 30, 40]:
    file = open("PrecisionRecallLog.txt", "a")
    log("Precision and Recall in tail with N=" + str(x))
    recommendations = []
    for i in range(5):
        print("Calculating Recommendations for Test set " + str(i+1))
        KNN_PC_recommendations = []
        CB_imp_recommendations = []
        #CB_recommendations = []
        #MF_recommendations = []

        for user in users:
            KNN_PC_recommendations.insert(user - 1, recommend(user, old_ratings[i], movies, KNN_PC_ratings[i], x))
            CB_imp_recommendations.insert(user - 1, recommend(user, old_ratings[i], movies, CB_imp_ratings[i], x))
            #CB_recommendations.insert(user - 1, recommend(user, old_ratings[i], movies, CB_ratings[i], 1))
            #MF_recommendations.insert(user - 1, recommend(user, old_ratings[i], movies, MF_ratings[i], 1))

        recommendations.append([KNN_PC_recommendations, CB_imp_recommendations])

    for j in range(2):
        log(i_to_algo(j) + ":")
        for i in range(5):
            log("Test set " + str(i+1) + ":" + str(PrecisionRecall.average_precision_recall(recommendations[i][j], in_tail)))
        log("")

    if not file.closed:
        file.close()


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


def calculate_user_split(user, ratings, head, tail):

    head_ratings = []

    for movie in head:
        if ratings[user][movie] > 0.0:
            head_ratings.append(movie)

    tail_ratings = []

    for movie in tail:
        if ratings[user][movie] > 0.0:
            tail_ratings.append(movie)

    if head_ratings == 0:
        return 1

    if tail_ratings == 0:
        return 0

    return float(len(tail_ratings)) / float(len(tail_ratings) + len(head_ratings))


#users = DataAPI.read_users_as_id_list()
#movies = DataAPI.read_movies_as_id_list()
#ratings = DataAPI.read_ratings("FullData")
#head, tail = get_head_and_tail(50, users, movies, ratings)
#
#splits = 0
#for user in users:
#    splits += calculate_user_split(user - 1, ratings, head, tail)
#
#average = float(splits) / float(len(users))
#print(average)
