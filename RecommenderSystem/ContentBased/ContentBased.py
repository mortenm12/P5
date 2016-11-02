from Profiling import *
import numpy


def calculate_n_recommendations(user_id, n):
    movie_profiles = profile_movies()
    user_profile = profile_single_user(user_id)

    u_vector = numpy.array(user_profile.vector.copy())
    weights = []
    for movie_profile in movie_profiles:
        m_vector = numpy.array(movie_profile.vector.copy())
        weights.append([movie_profile.movie.id, similarity(u_vector, m_vector)])

    weights = sorted(weights, key=lambda x: x[1], reverse=True)

    return weights[:n]


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
        print("Movie " + "{:4d}".format(recommendation[0]) + " with weight " + "{:1.2f}".format(recommendation[1]))


def similarity(x, y):
    return numpy.dot(x, y)/(math.sqrt(sum([pow(xi, 2) for xi in x])) * math.sqrt(sum([pow(yi, 2) for yi in y])))

do_content_based_recommendations()
