oldGenres = open("OriginalData/u.genre", "r")
newGenres = open("FinalData/Genres", "w")

for line in oldGenres:
    parts = line.split('|')
    parts[1] = parts[1][:-1]
    newGenres.write(parts[1] + '|' + parts[0] + '\n')

if not oldGenres.closed:
    oldGenres.close()

if not newGenres.closed:
    newGenres.close()

oldUsers = open("OriginalData/u.user", "r")
newUsers = open("FinalData/Users", "w")

for line in oldUsers:
    newUsers.write(line)

if not oldUsers.closed:
    oldUsers.close()

if not newUsers.closed:
    newUsers.close()

oldRatings = open("OriginalData/u.data", "r")
newRatings = open("FinalData/Ratings", "w")

for line in oldRatings:
    parts = line.split()
    newRatings.write(parts[0] + '|' + parts[1] + '|' + parts[2] + '|' + parts[3] + '\n')

if not oldRatings.closed:
    oldRatings.close()

if not newRatings.closed:
    newRatings.close()

oldMovies = open("OriginalData/u.item", "r")
newMovies = open("FinalData/Movies", "w")

for line in oldMovies:
    parts = line.split('|')
    parts[23] = parts[23][:-1]
    newMovies.write(parts[0] + '|' + parts[1] + '|' + parts[2] + '|')
    genres = []
    for i in range(5, 24):
        if parts[i] == '1':
            genres.append(i - 5)

    for i in range(0, len(genres)):
        if i == len(genres) - 1:
            newMovies.write(str(genres[i]))
        else:
            newMovies.write(str(genres[i]) + ',')

    newMovies.write('||\n')

if not oldMovies.closed:
    oldMovies.close()

if not newMovies.closed:
    newMovies.close()

actors = open("FinalData/Actors", "w")
actors.close()

