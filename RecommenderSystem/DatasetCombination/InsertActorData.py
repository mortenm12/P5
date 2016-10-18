import time
from ConvertOriginalToFinal import convert_original_to_final
from DataAPI import Movie


# Reads the movie file without actors and directors
def read_movie_file(source_directory):
    movie_file = open("../" + source_directory + "/Movies.data", "r", encoding="iso_8859_15")
    movies = []

    for line in movie_file:
        parts = line.split('|')
        movies.append(Movie(parts[0], parts[1], date=parts[2], genres=parts[3]))

    if not movie_file.closed:
        movie_file.close()

    return movies


# Remakes the movie file with the new actors and directors
def remake_movies_file(movies, target_directory):
    movies_file = open("../" + target_directory + "/Movies.data", "w")

    for movie in movies:
        movies_file.write(
            '|'.join([movie.id, movie.name, movie.date, movie.genres, ','.join(movie.actors), ','.join(movie.directors)])+'\n')

    if not movies_file.closed:
        movies_file.close()


# Extracts the title of a movie from the raw string given by the IMDb data
def extract_movie_title(movie_parts):
    j = 0
    for i in range(0, len(movie_parts)):
        if movie_parts[i].endswith('\n'):
            movie_parts[i] = movie_parts[i][:-1]
        if len(movie_parts[i]) == 6 and movie_parts[i].startswith('(') \
                and movie_parts[i].endswith(')') and len(movie_parts[i][1:-1]) == 4:
            j = i + 1
            break

    movie_parts = movie_parts[0:j]
    return ' '.join(movie_parts)


# Writes the actor file
def write_actors_file(actors, target_directory):
    actors_file = open("../" + target_directory + "/Actors.data", "w")

    for i in range(0, len(actors)):
        actors_file.write(str(i) + "|" + actors[i] + "\n")

    if not actors_file.closed:
        actors_file.close()


# Writes the director file
def write_directors_file(directors, target_directory):
    directors_file = open("../" + target_directory + "/Directors.data", "w")

    for i in range(0, len(directors)):
        directors_file.write(str(i) + "|" + directors[i] + "\n")

    if not directors_file.closed:
        directors_file.close()


# Reads and inserts the directors into the movie objects
def insert_directors(movies, source_directory):
    directors = []
    a = 0
    l = 0
    directors_file = open("../" + source_directory + "/directors.list", "r", encoding="iso_8859_15")

    line = directors_file.readline()
    l += 1

    while line != 'THE DIRECTORS LIST\n':
        line = directors_file.readline()
        l += 1

    for i in range(0, 4):
        directors_file.readline()
        l += 1

    line = directors_file.readline()
    l += 1
    while not line.startswith('----'):
        parts = line.split('\t')
        parts = [x for x in parts if x]
        director = parts[0]
        movie_parts = parts[1].split()
        movie = extract_movie_title(movie_parts)
        director_movies = [movie]
        director_key = a

        line = directors_file.readline()
        l += 1
        while line != '\n':
            parts = line.split()
            parts = [x for x in parts if x]
            movie = extract_movie_title(parts)
            if movie not in director_movies:
                director_movies.append(movie)

            line = directors_file.readline()
            l += 1

        for mov in movies:
            if mov.name in director_movies:
                if str(director_key) not in mov.directors:
                    mov.directors.append(str(director_key))

                if director not in directors:
                    directors.insert(director_key, director)
                    a += 1

        print(str(l))
        line = directors_file.readline()
        l += 1

    if not directors_file.closed:
        directors_file.close()

    return movies, directors


# Reads and inserts the actors into the movie objects
def insert_actors(movies, file, actors, a, source_directory):
    l = 0
    actors_file = open("../" + source_directory + "/" + file, "r", encoding="iso_8859_15")

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
        actor_key = a

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
                if str(actor_key) not in mov.actors:
                    mov.actors.append(str(actor_key))

                if actor not in actors:
                    actors.insert(actor_key, actor)
                    a += 1

        print(str(l))
        line = actors_file.readline()
        l += 1

    if not actors_file.closed:
        actors_file.close()

    return movies, actors, a

convert_original_to_final("Test1Source", "Test1Target", "u1.test")
#movs = read_movie_file("FinalData")
#time_at_start = time.clock()
#actors = []
#movs, directors = insert_directors(movs, "OriginalData")
#movs, actors, a = insert_actors(movs, 'actors.list', actors, 0, "OriginalData")
#movs, actors, a = insert_actors(movs, 'actresses.list', actors, a, "OriginalData")
#write_actors_file(actors, "FinalData")
#write_directors_file(directors, "FinalData")
#time_at_end = time.clock()
#time_elapsed = time_at_end - time_at_start
#print("Time elapsed: " + str(int(time_elapsed/60)) + ':' + str(int(time_elapsed) % 60))
#remake_movies_file(movs, "FinalData")
