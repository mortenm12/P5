from DataAPI import *
from DataAnalysis import *


class UserProfile:
    def __init__(self, user):
        self.user = user
        genres = []
        frequency = find_genre_frequency_for_user(user, M, R)
        for key in frequency:
            genres.insert(key, [key, frequency[key]])
        genres = sorted(genres, key=lambda x: x[1], reverse=True)
        vector = [0 for x in range(0, 19)]
        best_score = genres[0][1]
        if not best_score == 0:
            vector[genres[0][0]] = 1.0
            for genre in genres[1:]:
                vector[genre[0]] = genre[1] / best_score
        self.genre_vector = vector


def find_genre_frequency_for_user(user, movies, ratings):
    genre_frequency = {}
    genre_dict = read_genres_as_dict()
    for genre in genre_dict:
        genre_frequency[genre_dict[genre]] = 0

    for movie in movies:
        if ratings[user.id - 1][movie.id - 1] > 0:
            for genre in movie.genres:
                genre_frequency[genre_dict[genre]] += 1

    return genre_frequency

U, M, R = calculate_extra_data(read_movies_as_object_list(), read_users_as_object_list(), read_ratings("Test1"))

profiles = []
i = 0
length = len(U)
for user in U:
    print(str((i / length) * 100) + "%")
    profiles.append(UserProfile(user))
    i += 1

x = 0