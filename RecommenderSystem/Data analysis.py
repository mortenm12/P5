class Movie:
    def __init__(self, mid, name):
        self.name = name
        self.id = mid
        self.number_of_ratings = 0


class User:
    def __init__(self, uid):
        self.id = uid
        self.ratings_in_head = 0
        self.ratings_in_tail = 0

    def percent_ratings_in_tail(self):
        if self.ratings_in_head > 0 and self.ratings_in_tail > 0:
            return float(self.ratings_in_tail) / float(self.ratings_in_head + self.ratings_in_tail)
        return 0.0

movies_file = open("FinalData/Movies.data", "r", encoding='iso_8859_15')
movies = []
for line in movies_file:
    parts = line.split('|')
    movies.append(Movie(int(parts[0]), parts[1]))
if not movies_file.closed:
    movies_file.close()

users_file = open("FinalData/Users.data", "r", encoding='iso_8859_15')
users = []
for line in users_file:
    parts = line.split('|')
    users.append(User(int(parts[0])))
if not users_file.closed:
    users_file.close()

ratings = []
for i in range(0, len(users)):
    ratings.append([])
    for j in range(0, len(movies)):
        ratings[i].append(0.0)

ratings_file = open("FinalData/Ratings.data", "r", encoding='iso_8859_15')
for line in ratings_file:
    parts = line.split('|')
    ratings[int(parts[0]) - 1][int(parts[1]) - 1] = float(parts[2])
if not ratings_file.closed:
    ratings_file.close()

for i in range(0, len(ratings)):
    for j in range(0, len(ratings[0])):
        if ratings[i][j] > 0.0:
            movies[j].number_of_ratings += 1

sorted_movies = movies.copy()
sorted_movies.sort(key=lambda x: x.number_of_ratings, reverse=True)
split = sorted_movies[80].number_of_ratings
head = [x for x in sorted_movies if x.number_of_ratings >= split]
tail = [x for x in sorted_movies if x.number_of_ratings < split]

for user in users:
    for movie in head:
        if ratings[user.id - 1][movie.id - 1] > 0.0:
            user.ratings_in_head += 1
    for movie in tail:
        if ratings[user.id - 1][movie.id - 1] > 0.0:
            user.ratings_in_tail += 1

sorted_users = users.copy()
sorted_users.sort(key=lambda x: x.percent_ratings_in_tail(), reverse=True)

result = open("FinalData/UserRatingDistribution.Data", "w", encoding='iso_8859_15')
for user in sorted_users:
    result.write("|".join([str(user.id), str(user.ratings_in_head), str(user.ratings_in_tail), "{}".format(user.percent_ratings_in_tail())]) + '\n')
if not result.closed:
    result.close()

head_file = open("FinalData/Head.Data", "w", encoding='iso_8859_15')
for movie in head:
    head_file.write("|".join([str(movie.id), str(movie.name), str(movie.number_of_ratings)]) + '\n')
if not head_file.closed:
    head_file.close()

tail_file = open("FinalData/Tail.Data", "w", encoding='iso_8859_15')
for movie in tail:
    tail_file.write("|".join([str(movie.id), str(movie.name), str(movie.number_of_ratings)]) + '\n')
if not tail_file.closed:
    tail_file.close()
