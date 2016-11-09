from DataAPI import *
from DataAnalysis import *


class UserProfile:
    def __init__(self, user):
        self.user = user
        genre_metric = [sum(x) for x in self.user.rated_genres]
        actor_metric = [sum(x) for x in self.user.rated_actors]
        director_metric = [sum(x) for x in self.user.rated_directors]
        highest_genre = sorted(genre_metric, reverse=True)[0]
        highest_actor = sorted(actor_metric, reverse=True)[0]
        highest_director = sorted(director_metric, reverse=True)[0]
        self.vector = [(x / highest_genre) * 5 if highest_genre > 0 else 0 for x in genre_metric]
        self.vector.extend([x / highest_actor if highest_actor > 0 else 0 for x in actor_metric])
        self.vector.extend([x / highest_director if highest_director > 0 else 0 for x in director_metric])


class MovieProfile:
    def __init__(self, movie):
        self.movie = movie
        self.vector = [0.0 for x in range(19)]
        for genre in movie.genres:
            self.vector[genre] = 5.0
        self.vector.extend([0.0 for x in range(director_count)])
        for director in self.movie.directors:
            self.vector[director + 18] = 1.0
        self.vector.extend([0.0 for x in range(actor_count)])
        for actor in self.movie.actors:
            self.vector[actor + director_count + 18] = 1.0


def profile_single_user(u_id):
    return UserProfile(U[u_id - 1])


def profile_movies():
    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))
    return movie_profiles


def profile_movies_and_users():
    user_profiles = []
    for user in U:
        user_profiles.append(UserProfile(user))

    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))

    return movie_profiles, user_profiles

actor_count = get_actor_count()
director_count = get_director_count()
R = read_ratings("Test1")
M = read_movies_as_object_list()
M = add_rating_metrics_to_movies(M, R)
U = read_users_as_object_list()
U = add_rating_metrics_to_users(M, U, R)