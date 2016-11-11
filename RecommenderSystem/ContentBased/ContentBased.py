from Profiling import *
import numpy


def write_matrix(m, file, test_set):
    result = open("Output/" + test_set + "/" + file, "w")
    result.write(" ID , " + ", ".join(str(x) for x in range(1, len(m[0]) + 1)) + "\n")
    for i in range(0, len(m)):
        result.write("{:>4d}, ".format(i + 1))
        result.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        result.write("\n")

    if not result.closed:
        result.close()


def calculate_recommendation_matrix(test_set):
    movie_profiles, user_profiles = profile_movies_and_users(test_set)

    R = [[0.0 for x in range(len(movie_profiles))] for x in range(len(user_profiles))]

    for user in user_profiles:
        u_vectors = {}
        for vector in user.vectors:
            u_vectors[vector] = numpy.array(user.vectors[vector].copy())

        for movie in movie_profiles:
            m_vector = numpy.array(movie.vector.copy())
            weights = [[x, similarity(u_vectors[x], m_vector)] for x in u_vectors]
            weights.sort(key=lambda x: x[1], reverse=True)
            R[user.user.id - 1][movie.movie.id - 1] = weights[0][0]

    write_matrix(R, "ratings.data", test_set)


def calculate_n_recommendations(user_id, n):
    movie_profiles = profile_movies()
    user_profile = profile_single_user(user_id)

    u_vectors = {}
    for vector in user_profile.vectors:
        u_vectors[vector] = numpy.array(user_profile.vectors[vector].copy())

    ratings = []
    for movie_profile in movie_profiles:
        m_vector = numpy.array(movie_profile.vector.copy())
        weights = [[x, similarity(u_vectors[x], m_vector)] for x in u_vectors]
        weights.sort(key=lambda x: x[1], reverse=True)
        ratings.append([movie_profile.movie.id, weights[0][0], weights[0][1]])

    ratings = sorted(ratings, key=lambda x: x[1] + x[2], reverse=True)

    return ratings[:n]


def do_content_based_recommendations():
    print("What user do you want recommendations for?")
    s = input()
    i = int(s)
    print("How many recommendations do you want?")
    s = input()
    n = int(s)
    recommendations = calculate_n_recommendations(i, n)
    print("For user " + str(i) + ":")
    for recommendation in recommendations:
        print("Movie " + "{:4d}".format(recommendation[0]) + " rated " + "{:1.2f}".format(recommendation[1]) + " with weight " + "{:1.2f}".format(recommendation[2]))


def similarity(x, y):
    return numpy.dot(x, y)/(math.sqrt(sum([pow(xi, 2) for xi in x])) * math.sqrt(sum([pow(yi, 2) for yi in y])))

calculate_recommendation_matrix("Test1")
calculate_recommendation_matrix("Test2")
calculate_recommendation_matrix("Test3")
calculate_recommendation_matrix("Test4")
calculate_recommendation_matrix("Test5")
