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


# User class with all content included
class User:
    def __init__(self, uid):
        self.id = uid
        self.ratings_in_head = 0
        self.ratings_in_tail = 0

    def percent_ratings_in_tail(self):
        if self.ratings_in_head > 0 and self.ratings_in_tail > 0:
            return float(self.ratings_in_tail) / float(self.ratings_in_head + self.ratings_in_tail)
        return 0.0


# Read movies as a list of Movie objects with all data included
def read_movies_as_object_list(directory):
    genres_dict = {}
    genres_file = open("../" + directory + "/Genres.Data", "r", encoding='iso_8859_15')
    for line in genres_file:
        parts = line.split('|')
        genres_dict[int(parts[0])] = parts[1]

    if not genres_file.closed:
        genres_file.close()

    movies_file = open("../" + directory + "/Movies.data", "r", encoding='iso_8859_15')
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
def read_movies_as_id_list(directory):
    movies_file = open("../" + directory + "/Movies.data", "r", encoding='iso_8859_15')
    movies = []
    for line in movies_file:
        parts = line.split('|')
        movies.append(int(parts[0]))

    if not movies_file.closed:
        movies_file.close()

    return movies


# Read movies as a dictionary mapping ids to names
def read_movies_as_id_name_dict(directory):
    movies_file = open("../" + directory + "/Movies.data", "r", encoding='iso_8859_15')
    movies = {}
    for line in movies_file:
        parts = line.split('|')
        movies[int(parts[0])] = parts[1]

    if not movies_file.closed:
        movies_file.close()

    return movies


# Read users as a list of User objects with all data included
def read_users_as_object_list(directory):
    users_file = open("../" + directory + "/Users.data", "r", encoding='iso_8859_15')
    users = []
    for line in users_file:
        parts = line.split('|')
        users.append(User(int(parts[0])))

    if not users_file.closed:
        users_file.close()

    return users


# Read users as a list of ids
def read_users_as_id_list(directory):
    users_file = open("../" + directory + "/Users.data", "r", encoding='iso_8859_15')
    users = []
    for line in users_file:
        parts = line.split('|')
        users.append(int(parts[0]))

    if not users_file.closed:
        users_file.close()

    return users


# Read ratings as a user/item rating matrix
# Also outputs dictionaries mapping user and movie ids to their indexes in the matrix
def read_test_ratings(users, movies, directory):
    ratings = []
    for i in range(0, len(users)):
        ratings.append([])
        for j in range(0, len(movies)):
            ratings[i].append(0.0)

    ratings_file = open("../" + directory + "/TestRatings.data", "r", encoding='iso_8859_15')
    for line in ratings_file:
        parts = line.split('|')
        ratings[int(parts[0])][int(parts[1])] = float(parts[2])

    if not ratings_file.closed:
        ratings_file.close()

    return ratings


# Read ratings as a user/item rating matrix
# Also outputs dictionaries mapping user and movie ids to their indexes in the matrix
def read_base_ratings(users, movies, directory):
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
