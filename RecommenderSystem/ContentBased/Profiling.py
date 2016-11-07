from DataAPI import *
from DataAnalysis import *


class UserProfile:
    def __init__(self, u_id, vector):
        self.id = u_id
        self.vector = vector

    def vector_to_string(self):
        return ",".join([str(x) for x in self.vector])


class MovieProfile:
    def __init__(self, m_id, vector):
        self.id = m_id
        self.vector = vector


def vector_to_string(vector):
    return ",".join([str(x) for x in vector])


def read_user_profiles(test_set):
    file = open(test_set + "UserProfiles.data", "r")

    users = []
    i = 0
    for line in file:
        users.append(UserProfile(i, [float(x) for x in line.split(",")]))
        i += 1

    if not file.closed:
        file.close()

    return users


def read_user_profile(test_set, n):
    file = open("../ContentBased/" + test_set + "UserProfiles.data", "r")

    user = None
    i = 0
    for line in file:
        if i == n:
            user = UserProfile(i, [float(x) for x in line.split(",")])
        i += 1

    if not file.closed:
        file.close()

    return user


def read_movie_profiles():
    file = open("../ContentBased/MovieProfiles.data", "r")

    movies = []
    i = 0
    for line in file:
        movies.append(MovieProfile(i, [float(x) for x in line.split(",")]))
        i += 1

    if not file.closed:
        file.close()

    return movies


def profile_users(test_set, U):
    file = open("../ContentBased/" + test_set + "UserProfiles.data", "w")
    for user in U:
        file.write(vector_to_string(generate_user_vector(user)) + "\n")
    if not file.closed:
        file.close()


def profile_movies(M):
    file = open("../ContentBased/MovieProfiles.data", "w")
    for movie in M:
        file.write(vector_to_string(generate_movie_vector(movie)) + "\n")
    if not file.closed:
        file.close()


def generate_user_vector(user):
    genre_metric = [sum(x) for x in user.rated_genres]
    actor_metric = [sum(x) for x in user.rated_actors]
    director_metric = [sum(x) for x in user.rated_directors]
    highest_genre = sorted(genre_metric, reverse=True)[0]
    highest_actor = sorted(actor_metric, reverse=True)[0]
    highest_director = sorted(director_metric, reverse=True)[0]
    vector = [(x / highest_genre) * 5 if highest_genre > 0 else 0 for x in genre_metric]
    vector.extend([x / highest_actor if highest_actor > 0 else 0 for x in actor_metric])
    vector.extend([x / highest_director if highest_director > 0 else 0 for x in director_metric])
    return vector


def generate_movie_vector(movie):
    actor_count = get_actor_count()
    director_count = get_director_count()
    vector = [0.0 for x in range(19)]
    for genre in movie.genres:
        vector[genre] = 5.0
    vector.extend([0.0 for x in range(director_count)])
    for director in movie.directors:
        vector[director + 18] = 1.0
    vector.extend([0.0 for x in range(actor_count)])
    for actor in movie.actors:
        vector[actor + director_count + 18] = 1.0
    return vector


def do_profiling(test_set):
    R = read_ratings("Test1")
    M = read_movies_as_object_list()
    M = add_rating_metrics_to_movies(M, R)
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)

    profile_movies(M)
    profile_users(test_set, U)
