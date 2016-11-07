from Profiling import *
import numpy


def calculate_n_recommendations(test_set, user_id, n):
    movie_profiles = read_movie_profiles()
    user_profile = read_user_profile(test_set, user_id)

    u_vector = numpy.array(user_profile.vector.copy())
    weights = []
    for movie_profile in movie_profiles:
        m_vector = numpy.array(movie_profile.vector.copy())
        weights.append([movie_profile.id, similarity(u_vector, m_vector)])

    weights = sorted(weights, key=lambda x: x[1], reverse=True)

    return weights[:n]


def do_content_based_recommendations(test_set, i, n):
    recommendations = calculate_n_recommendations(test_set, i, n)
    print("For user " + str(i) + ":")
    for recommendation in recommendations:
        print("Movie " + "{:4d}".format(recommendation[0]) + " with weight " + "{:1.2f}".format(recommendation[1]))


def similarity(x, y):
    return numpy.dot(x, y)/(math.sqrt(sum([pow(xi, 2) for xi in x])) * math.sqrt(sum([pow(yi, 2) for yi in y])))
