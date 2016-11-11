from DataAPI import *
from DataAnalysis import *


class UserProfile:
    def __init__(self, user):
        self.user = user
        self.vectors = {}
        for rating in self.user.rated_genres:
            metric = self.user.rated_genres[rating]
            highest_genre = sorted(metric, reverse=True)[0]
            if not highest_genre == 0.0:
                self.vectors[rating] = [x/highest_genre for x in metric]
            else:
                self.vectors[rating] = [0.0 for x in range(19)]


class MovieProfile:
    def __init__(self, movie):
        self.movie = movie
        self.vector = [0.0 for x in range(19)]
        for genre in movie.genres:
            self.vector[genre] = 1.0


def get_data(test_set):
    R = read_ratings(test_set)
    M = read_movies_as_object_list()
    M = add_rating_metrics_to_movies(M, R)
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)

    return R, M, U


def profile_single_user(u_id):
    R, M, U = get_data("Test1")
    return UserProfile(U[u_id - 1])


def profile_movies():
    R, M, U = get_data("Test1")
    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))
    return movie_profiles


def profile_movies_and_users(test_set):
    R, M, U = get_data(test_set)
    user_profiles = []
    for user in U:
        user_profiles.append(UserProfile(user))

    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))

    return movie_profiles, user_profiles


