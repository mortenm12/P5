from DataAPI import *
from DataAnalysis import *
import numpy


class UserProfile:
    def __init__(self, user):
        self.user = user
        self.vectors = {}
        for rating in self.user.rated_genres:
            metric = self.user.rated_genres[rating]
            highest = sorted(metric, reverse=True)[0]
            metric = [x/highest if highest > 0.0 else 0.0 for x in metric]
            self.vectors[rating] = [pow(x, 4) for x in metric]
        for key in self.vectors:
            self.vectors[key] = numpy.array(self.vectors[key])


class MovieProfile:
    def __init__(self, movie):
        self.movie = movie
        self.vector = [0.0 for x in range(19)]
        for genre in movie.genres:
            self.vector[genre] = 1.0
        self.vector = numpy.array(self.vector)


def get_data(test_set):
    R = read_ratings(test_set)
    M = read_movies_as_object_list()
    M = add_rating_metrics_to_movies(M, R)
    U = read_users_as_object_list()
    U = add_rating_metrics_to_users(M, U, R)

    return R, M, U


def profile_movies_and_users(test_set, steps=10):
    R, M, U = get_data(test_set)
    user_profiles = []
    for user in U:
        user_profiles.append(UserProfile(user))

    movie_profiles = []
    for movie in M:
        movie_profiles.append(MovieProfile(movie))

    for user_profile in user_profiles:
        print("Profiling user: " + str(user_profile.user.id))
        for i in range(steps):
            learn_user_profile(R, user_profile, movie_profiles)

    return movie_profiles, user_profiles


def learn_user_profile(ratings, user_profile, movie_profiles):
    u_id = user_profile.user.id
    predicted_ratings = []
    for j in range(len(ratings[0])):
        if ratings[u_id - 1][j] > 0:
            predicted_ratings.insert(j, predict_rating(user_profile, movie_profiles[j]))
        else:
            predicted_ratings.insert(j, 0)

    for j in range(len(ratings[0])):
        if ratings[u_id - 1][j] > 0:
            update_vectors(user_profile, movie_profiles[j], predicted_ratings, ratings)


def update_vectors(user_profile, movie_profile, predicted_ratings, ratings, alpha=0.03):
    error = sum([abs(predicted_ratings[i] - ratings[user_profile.user.id - 1][i]) for i in range(len(predicted_ratings))]) / len(predicted_ratings)
    rating = ratings[user_profile.user.id - 1][movie_profile.movie.id - 1]
    predicted_rating = predicted_ratings[movie_profile.movie.id - 1]
    for i in range(len(user_profile.vectors[rating])):
        user_profile.vectors[rating][i] += alpha * movie_profile.vector[i] * (rating - predicted_rating) * error
        user_profile.vectors[predicted_rating][i] += alpha * movie_profile.vector[i] * (predicted_rating - rating) * error


def predict_rating(user_profile, movie_profile):
    weights = calculate_weights(user_profile, movie_profile)
    weights.sort(key=lambda x: x[0], reverse=True)
    return weights[0][1]


def calculate_weights(user_profile, movie_profile):
    weights = []
    for key in user_profile.vectors:
        weights.insert(key, [similarity(user_profile.vectors[key], movie_profile.vector), key])
    return weights


def similarity(x, y):
    return numpy.dot(x, y)/(math.sqrt(sum([pow(xi, 2) for xi in x])) * math.sqrt(sum([pow(yi, 2) for yi in y])))