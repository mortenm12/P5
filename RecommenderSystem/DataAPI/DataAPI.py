from AuxillaryMath import *


# Movie class with all content included
class Movie:
    def __init__(self, mid, name, genres=None, actors=None, directors=None, date=None):
        self.name = name
        self.id = mid
        self.date = date
        self.genres = genres
        self.actors = actors
        self.directors = directors
        self.number_of_ratings = 0


class User:
    # u_id is every user identification number
    def __init__(self, u_id):
        self.id = u_id
        self.average_rating = 0
        self.rated_movies = {}
        self.recommended = []
        self.ratings_in_head = 0
        self.ratings_in_tail = 0

    def percent_ratings_in_tail(self):
        if self.ratings_in_head > 0 and self.ratings_in_tail > 0:
            return float(self.ratings_in_tail) / float(self.ratings_in_head + self.ratings_in_tail)
        return 0.0

    # m_id is the movies identifications number, and rat is the users rating of the movie
    # it stores the rating in the users rated-movies
    def add_rating(self, m_id, rat):
        self.rated_movies[int(m_id)] = rat

    # runs trough the users ratings and finds the average, and store it in the users overage_rating
    def calculate_average_rating(self):
        sum1 = 0
        if len(self.rated_movies) == 0:
            self.average_rating = 0
        else:
            for movie in self.rated_movies:
                sum1 += self.rated_movies[movie]
            self.average_rating = sum1 / len(self.rated_movies)

    # user2 is a user who is not the user self
    # returns an array of both the users ratings of movies the both have seen
    def find_both_rated_movies(self, user2):
        rated = [[], []]
        for movie in self.rated_movies:
            if int(movie) in user2.rated_movies:
                rated[0].append(self.rated_movies[movie])
                rated[1].append(user2.rated_movies[movie])
        return rated

    # user2 is a user who is not the user self
    # returns the weight between self and user2
    def weight(self, user2):  # page 124
        data = self.find_both_rated_movies(user2)
        return cos(data[0], data[1])

    # movie is a movie in the dictionary all_movies
    # Returns the average of the users ratings, and the average of what other rat the movie, compared to normal
    def mean_center(self, movie, list_of_users):  # page 121
        sum1 = 0
        user_who_have_seen_this_movie = []

        # makes a list of all users who have seen the movie
        for user in list_of_users:
            if movie in user.rated_movies:
                user_who_have_seen_this_movie.append(user)

        for user in user_who_have_seen_this_movie:
            sum1 += user.rated_movies[movie] - user.average_rating

        if len(self.rated_movies) == 0 and len(user_who_have_seen_this_movie) == 0:
            return self.average_rating + sum1
        elif len(self.rated_movies) == 0:
            return self.average_rating + (sum1 / len(user_who_have_seen_this_movie))
        elif len(user_who_have_seen_this_movie) == 0:
            return (self.average_rating / len(self.rated_movies)) + sum1
        else:
            return (self.average_rating / len(self.rated_movies)) + (sum1 / len(user_who_have_seen_this_movie))

    # k is the numbers of neighbours the algorithm should find, and movie is the movie ever neighbour should have rated
    # returns a list of k numbers of users who have the highest weight to the user self
    def find_k_nearest_neighbour(self, k, movie, list_of_users):
        users = []

        for user in list_of_users:
            if int(movie) in user.rated_movies:
                users.insert(user.id, [user, self.weight(user)])

        users.sort(key=lambda x: x[1])

        return users[:k]

    # movie is a movie in the dictionary all_movies
    # return a recommendation for the user self on movie
    def recommend(self, movie, list_of_users):  # page 115
        users = self.find_k_nearest_neighbour(5, movie, list_of_users)
        sum1 = 0
        sum2 = 0
        for user in users:
            sum1 += user[1] * user[0].rated_movies[int(movie)]
            sum2 += user[1]
        if sum2 == 0:
            return self.mean_center(movie, list_of_users)
        else:
            return (sum1 / sum2) + self.mean_center(movie, list_of_users)


# Read movies as a list of Movie objects with all data included
def read_movies_as_object_list():
    genres_dict = {}
    genres_file = open("../FullData/Genres.Data", "r", encoding='iso_8859_15')
    for line in genres_file:
        parts = line.split('|')
        genres_dict[int(parts[0])] = parts[1]

    if not genres_file.closed:
        genres_file.close()

    movies_file = open("../FullData/Movies.data", "r", encoding='iso_8859_15')
    movies = []
    for line in movies_file:
        parts = line.split('|')
        genre_ids = [int(x) for x in parts[2].split(',')]
        genres = []
        for number in genre_ids:
            genres.append(genres_dict[number])
        actors = [int(x) for x in parts[3].split(',')]
        directors = [int(x) for x in parts[4].split(',')]
        movies.append(Movie(int(parts[0]), parts[1], genres, actors, directors))

    if not movies_file.closed:
        movies_file.close()

    return movies


# Read movies as a list of movie ids
def read_movies_as_id_list():
    movies_file = open("../FullData/Movies.data", "r", encoding='iso_8859_15')
    movies = []
    for line in movies_file:
        parts = line.split('|')
        movies.append(int(parts[0]))

    if not movies_file.closed:
        movies_file.close()

    return movies


# Read movies as a dictionary mapping ids to names
def read_movies_as_id_name_dict():
    movies_file = open("../FullData/Movies.data", "r", encoding='iso_8859_15')
    movies = {}
    for line in movies_file:
        parts = line.split('|')
        movies[int(parts[0])] = parts[1]

    if not movies_file.closed:
        movies_file.close()

    return movies


# Read users as a list of User objects with all data included
def read_users_as_object_list():
    users_file = open("../FullData/Users.data", "r", encoding='iso_8859_15')
    users = []
    for line in users_file:
        parts = line.split('|')
        users.insert(int(parts[0]), User(int(parts[0])))

    if not users_file.closed:
        users_file.close()

    return users


# Read users as a list of ids
def read_users_as_id_list():
    users_file = open("../FullData/Users.data", "r", encoding='iso_8859_15')
    users = []
    for line in users_file:
        parts = line.split('|')
        users.append(int(parts[0]))

    if not users_file.closed:
        users_file.close()

    return users


# Read ratings as a user/item rating matrix
# Also outputs dictionaries mapping user and movie ids to their indexes in the matrix
def read_ratings(directory):
    users = read_users_as_id_list()
    movies = read_movies_as_id_list()
    ratings = []
    for i in range(0, len(users)):
        ratings.append([])
        for j in range(0, len(movies)):
            ratings[i].append(0.0)

    if directory == "FullData":
        ratings_file = open("../" + directory + "/Ratings.data", "r", encoding='iso_8859_15')
    else:
        ratings_file = open("../" + directory + "/TestRatings.data", "r", encoding='iso_8859_15')

    for line in ratings_file:
        parts = line.split('|')
        ratings[int(parts[0])][int(parts[1])] = float(parts[2])

    if not ratings_file.closed:
        ratings_file.close()

    return ratings


# Read ratings as a user/item rating matrix
# Also outputs dictionaries mapping user and movie ids to their indexes in the matrix
def read_base_ratings(directory):
    users = read_users_as_id_list()
    movies = read_movies_as_id_list()
    ratings = []
    for i in range(0, len(users)):
        ratings.append([])
        for j in range(0, len(movies)):
            ratings[i].append(0.0)

    ratings_file = open("../" + directory + "/BaseRatings.data", "r", encoding='iso_8859_15')
    for line in ratings_file:
        parts = line.split('|')
        ratings[int(parts[0])][int(parts[1])] = float(parts[2])

    if not ratings_file.closed:
        ratings_file.close()

    return ratings


# Read ratings as list of ratings
def read_ratings_as_list(directory):
    if directory == "FullData":
        ratings_file = open("../" + directory + "/Ratings.data", "r", encoding='iso_8859_15')
    else:
        ratings_file = open("../" + directory + "/TestRatings.data", "r", encoding='iso_8859_15')

    ratings = []
    for line in ratings_file:
        parts = line.split('|')
        ratings.append([int(parts[0]), int(parts[1]), int(parts[2])])

    return ratings