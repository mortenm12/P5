from DataAnalysis import Movie, User, read_movies, read_users, read_ratings


def read_data():
    users = read_users()
    movies = read_movies()
    ratings = read_ratings(users, movies)
    return users, movies, ratings

users, movies, ratings = read_data()



