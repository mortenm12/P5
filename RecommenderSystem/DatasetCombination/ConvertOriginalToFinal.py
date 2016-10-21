def convert_genres():
    oldGenres = open("../FullDataSource/u.genre", "r", encoding="iso_8859_15")
    newGenres = open("../FullData/Genres.data", "w")

    for line in oldGenres:
        parts = line.split('|')
        parts[1] = parts[1][:-1]
        newGenres.write(parts[1] + '|' + parts[0] + '\n')

    if not oldGenres.closed:
        oldGenres.close()

    if not newGenres.closed:
        newGenres.close()


def convert_users():
    oldUsers = open("../FullDataSource/u.user", "r", encoding="iso_8859_15")
    newUsers = open("../FullData/Users.data", "w")

    for line in oldUsers:
        newUsers.write(line)

    if not oldUsers.closed:
        oldUsers.close()

    if not newUsers.closed:
        newUsers.close()


def convert_ratings(source_directory, target_directory, test_rating_file_name, base_rating_file_name=""):
    oldRatings = open("../" + source_directory + "/" + test_rating_file_name, "r", encoding="iso_8859_15")
    if test_rating_file_name == "u.data":
        newRatings = open("../" + target_directory + "/Ratings.data", "w")
    else:
        newRatings = open("../" + target_directory + "/TestRatings.data", "w")

    for line in oldRatings:
        parts = line.split()
        newRatings.write('|'.join(parts) + '\n')

    if not oldRatings.closed:
        oldRatings.close()

    if not newRatings.closed:
        newRatings.close()

    if base_rating_file_name != "":
        oldRatings = open("../" + source_directory + "/" + test_rating_file_name, "r", encoding="iso_8859_15")
        newRatings = open("../" + target_directory + "/BaseRatings.data", "w")

        for line in oldRatings:
            parts = line.split()
            newRatings.write('|'.join(parts) + '\n')

        if not oldRatings.closed:
            oldRatings.close()

        if not newRatings.closed:
            newRatings.close()


def convert_movies():
    oldMovies = open("../FullDataSource/u.item", "r", encoding="iso_8859_15")
    newMovies = open("../FullData/Movies.data", "w")

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


# Converts the original MovieLens data format to a format more suited for our algorithms
# Genres format: id|name
# Users format: id|age|sex|occupation|vatNumber
# Ratings format: uid|mid|rating|timestamp
# Movies format: id|name|date|genreIds|actorIds|directorIds
# Actors format: id|name
# Directors format: id|name
def convert_original_to_final():
    convert_genres()
    convert_users()
    convert_movies()
    convert_ratings("FullDataSource", "FullData", "u.data")
    convert_ratings("FullDataSource", "Test1", "u1.test", "u1.base")
    convert_ratings("FullDataSource", "Test2", "u2.test", "u2.base")
    convert_ratings("FullDataSource", "Test3", "u3.test", "u3.base")
    convert_ratings("FullDataSource", "Test4", "u4.test", "u4.base")
    convert_ratings("FullDataSource", "Test5", "u5.test", "u5.base")

