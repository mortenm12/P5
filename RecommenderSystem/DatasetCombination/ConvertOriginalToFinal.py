# Converts the original MovieLens data format to a format more suited for our algorithms
# Genres format: id|name
# Users format: id|age|sex|occupation|vatNumber
# Ratings format: uid|mid|rating|timestamp
# Movies format: id|name|date|genreIds|actorIds|directorIds
# Actors format: id|name
# Directors format: id|name
def convert_original_to_final(source_directory, target_directory):
    oldGenres = open("../" + source_directory + "/u.genre", "r", encoding="iso_8859_15")
    newGenres = open("../" + target_directory + "/Genres.data", "w")

    for line in oldGenres:
        parts = line.split('|')
        parts[1] = parts[1][:-1]
        newGenres.write(parts[1] + '|' + parts[0] + '\n')

    if not oldGenres.closed:
        oldGenres.close()

    if not newGenres.closed:
        newGenres.close()

    oldUsers = open("../" + source_directory + "/u.user", "r", encoding="iso_8859_15")
    newUsers = open("../" + target_directory + "/Users.data", "w")

    for line in oldUsers:
        newUsers.write(line)

    if not oldUsers.closed:
        oldUsers.close()

    if not newUsers.closed:
        newUsers.close()

    oldRatings = open("../" + source_directory + "/u.data", "r", encoding="iso_8859_15")
    newRatings = open("../" + target_directory + "/Ratings.data", "w")

    for line in oldRatings:
        parts = line.split()
        newRatings.write('|'.join(parts) + '\n')

    if not oldRatings.closed:
        oldRatings.close()

    if not newRatings.closed:
        newRatings.close()

    oldMovies = open("../" + source_directory + "/u.item", "r", encoding="iso_8859_15")
    newMovies = open("../" + target_directory + "/Movies.data", "w")

    for line in oldMovies:
        parts = line.split('|')
        parts[23] = parts[23][:-1]
        newMovies.write('|'.join([parts[0], parts[1], parts[2], '']))
        genres = []
        for i in range(5, 24):
            if parts[i] == '1':
                genres.append(str(i - 5))

        newMovies.write(','.join(genres) + '||\n')

    if not oldMovies.closed:
        oldMovies.close()

    if not newMovies.closed:
        newMovies.close()

    actors = open("../" + target_directory + "/Actors.data", "w")
    actors.close()

