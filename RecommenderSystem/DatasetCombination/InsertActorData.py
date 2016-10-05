import time

class Movie:
    def __init__(self, name, date, genres):
        self.name = name
        self.date = date
        self.genres = genres
        self.actors = []
        self.directors = []


def read_movie_file():
    movie_file = open("FinalData/Movies", "r", encoding="iso_8859_15")
    movies = []

    for line in movie_file:
        parts = line.split('|')
        movies.append(Movie(parts[0], parts[1], parts[2]))

    if not movie_file.closed:
        movie_file.close()

    return movies


def remake_movies_file(movies):
    movies_file = open("FinalData\Movies", "w")

    for movie in movies:
        movies_file.write('|'.join([movie.name, movie.date, movie.genres, ', '.join(movie.actors), '']))

    if not movies_file.closed:
        movies_file.close()


def extract_movie_title(movie_parts):
    j = 0
    for i in range(0, len(movie_parts)):
        if movie_parts[i].endswith('\n'):
            movie_parts[i] = movie_parts[i][:-1]
        if movie_parts[i].startswith('(') and movie_parts[i].endswith(')'):
            j = i + 1
            break

    movie_parts = movie_parts[0:j]
    return ' '.join(movie_parts)


def insert_actors(movies, file):
    l = 0
    actors_file = open("OriginalData/" + file, "r", encoding="iso_8859_15")

    line = actors_file.readline()
    l += 1
    if file == 'actors.list':
        string = 'THE ACTORS LIST\n'
    elif file == 'actresses.list':
        string = 'THE ACTRESSES LIST\n'
    else:
        string = ''

    while line != string:
        line = actors_file.readline()
        l += 1

    for i in range(0, 4):
        actors_file.readline()
        l += 1

    line = actors_file.readline()
    l += 1
    while not line.startswith('----'):
        parts = line.split('\t')
        parts = [x for x in parts if x]
        actor = parts[0]
        movie_parts = parts[1].split()
        movie = extract_movie_title(movie_parts)
        actor_movies = [movie]

        line = actors_file.readline()
        l += 1
        while line != '\n':
            parts = line.split()
            parts = [x for x in parts if x]
            movie = extract_movie_title(parts)
            if movie not in actor_movies:
                actor_movies.append(movie)

            line = actors_file.readline()
            l += 1

        for mov in movies:
            if mov.name in actor_movies:
                mov.actors.append(actor)

        print(str(l))
        line = actors_file.readline()
        l += 1

    if not actors_file.closed:
        actors_file.close()

    return movies

movs = read_movie_file()
time_at_start = time.clock()
movs = insert_actors(movs, 'actors.list')
movs = insert_actors(movs, 'actresses.list')
time_at_end = time.clock()
time_elapsed = time_at_end - time_at_start
print("Time elapsed: " + str(int(time_elapsed/60)) + ':' + str(int(time_elapsed) % 60))
remake_movies_file(movs)
