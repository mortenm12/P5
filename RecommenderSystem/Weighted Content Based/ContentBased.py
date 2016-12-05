from DataAPI import *
import numpy
import math
import Evaluation


class UserProfile:
    def __init__(self, user):
        self.user = user
        self.relevant_vector = [0 for x in range(19)]
        self.irrelevant_vector = [0 for x in range(19)]

    # Calculate the relevant and irrelevant genres for the user.
    def calculate_relevancy_vectors(self, ratings, movies):
        genre_totals = [0 for x in range(19)]
        genre_sums = [0 for x in range(19)]

        for j in range(len(ratings[0])):
            if ratings[self.user.id - 1][j] > 0:
                for genre in movies[j].genres:
                    genre_totals[genre] += ratings[self.user.id - 1][j]
                    genre_sums[genre] += 1

        genre_averages = [genre_totals[i]/genre_sums[i] if genre_sums[i] > 0 else None for i in range(19)]

        for i in range(len(genre_averages)):
            if genre_averages[i] is None:
                pass
            elif genre_averages[i] > 3:
                self.relevant_vector[i] = 1
            elif genre_averages[i] <= 3:
                self.irrelevant_vector[i] = 1

        self.relevant_vector = numpy.array(self.relevant_vector)
        self.irrelevant_vector = numpy.array(self.irrelevant_vector)


class MovieProfile:
    def __init__(self, movie):
        self.movie = movie
        self.vector = [0 for x in range(19)]

        for genre in self.movie.genres:
            self.vector[genre] = 1

        self.vector = numpy.array(self.vector)


# Calculate cosine similarity of vectors x and y
def similarity(x, y):
    len_x = length(x)
    len_y = length(y)

    if len_x == 0 or len_y == 0:
        return 0
    else:
        return numpy.dot(x, y)/(len_x * len_y)


# Calculate the length of vector x.
def length(x):
    return math.sqrt(sum([pow(xi, 2) for xi in x]))


# Calculate the expected rating for for a given movie for a given user.
def calculate_rating(user_profile, movie_profile):
    like_weight = similarity(user_profile.relevant_vector, movie_profile.vector)
    dislike_weight = similarity(user_profile.irrelevant_vector, movie_profile.vector)

    if like_weight > dislike_weight:
        return 3 + 2 * like_weight
    elif like_weight < dislike_weight:
        return 3 - 2 * dislike_weight
    else:
        return 3


# Write a matrix to a file.
def write_matrix(m, file, test_set):
    result = open("Output/" + test_set + "/" + file, "w")
    result.write(" ID , " + ", ".join(str(x) for x in range(1, len(m[0]) + 1)) + "\n")

    for i in range(0, len(m)):
        result.write("{:>4d}, ".format(i + 1))
        result.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        result.write("\n")

    if not result.closed:
        result.close()


def do_content_based(R, M, U, printing=True):
    result = [[0 for j in range(len(R[0]))] for i in range(len(R))]

    # Generate movie and user profiles.
    movie_profiles = [MovieProfile(movie) for movie in M]
    user_profiles = [UserProfile(user) for user in U]

    for profile in user_profiles:
        if(printing):
            print("Generating preferences for user: " + str(profile.user.id))
        profile.calculate_relevancy_vectors(R, M)

    # Calculate each rating for each user/item pair.
    for i in range(len(R)):
        if(printing):
            print("Calculating ratings for user: " + str(i + 1))

        for j in range(len(R[0])):
            result[i][j] = calculate_rating(user_profiles[i], movie_profiles[j])

    return result


# Calculate all recommended ratings and enter them into a matrix.
def calculate_recommendation_matrix(test_set):
    # Initialize variables.
    R = read_ratings(test_set)
    M = read_movies_as_object_list()
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)
    result = do_content_based(R, M, U)

    write_matrix(result, "ratings.data", test_set)

#calculate_recommendation_matrix("Test1")
#calculate_recommendation_matrix("Test2")
#calculate_recommendation_matrix("Test3")
#calculate_recommendation_matrix("Test4")
#calculate_recommendation_matrix("Test5")

#evaluationAlgorithms = [
 #       (Evaluation.EvaluationAlgorithm.prefabs["MAE"], None),
 #       (Evaluation.EvaluationAlgorithm.prefabs["RMSE"], None),
 #       (Evaluation.EvaluationAlgorithm.prefabs["MURWAE"], None),
 #       (Evaluation.EvaluationAlgorithm.prefabs["MMRWAE"], None),
 #       (Evaluation.EvaluationAlgorithm.prefabs["RMURWSE"], None),
 #       (Evaluation.EvaluationAlgorithm.prefabs["RMMRWSE"], None),
 #       (Evaluation.EvaluationAlgorithm.prefabs["MRSRMSE"], (0, 49)),
 #       (Evaluation.EvaluationAlgorithm.prefabs["MRSRMSE"], (50, 1000))
 #   ]

#evaluator = Evaluation.RatingEvaluator(["Weighted Content Based"], [1, 2, 3, 4, 5], evaluationAlgorithms)
#evaluator.evaluate_all_algorithms()
#evaluator.log_results("Weighted Content Based Test")