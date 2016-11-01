from DataAPI import *
from DataAnalysis import *


class UserProfile:
    def __init__(self, user):
        self.user = user
        genre_metric = [sum(x) for x in user.rated_genres]
        highest = sorted(genre_metric, reverse=True)[0]
        self.genre_vector = [x / highest if highest > 0 else 0 for x in genre_metric]


class MovieProfile:
    def __init__(self, movie):
        self.movie = movie
        self.genre_vector = [0 for x in range(19)]
        for genre in movie.genres:
            self.genre_vector[genre] = 1


def profile_single_user(u_id):
    R = read_ratings("Test1")
    M = read_movies_as_object_list()
    M = add_rating_metrics_to_movies(M, R)
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)

    return UserProfile(U[u_id - 1])


def profile_movies():
    R = read_ratings("Test1")
    M = read_movies_as_object_list()
    M = add_rating_metrics_to_movies(M, R)
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)

    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))

    return movie_profiles


def profile_movies_and_users():
    R = read_ratings("Test1")
    M = read_movies_as_object_list()
    M = add_rating_metrics_to_movies(M, R)
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)

    user_profiles = []
    for user in U:
        user_profiles.append(UserProfile(user))

    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))

    return movie_profiles, user_profiles