import math

def cos(a,b):
    if lenght_of_vector(a) * lenght_of_vector(b) == 0:
        return 0
    return dot(a,b) / (lenght_of_vector(a) * lenght_of_vector(b))

def dot(a,b):
    summer = 0
    if len(a) == len(b):
        for x in range(len(a)):
            summer += a[x] * b[x]
        return summer
    else:
        raise IndexError("a and b should be the same length.")

def lenght_of_vector(a):
    summer = 0

    for x in a:
        summer += x ** 2

    return math.sqrt(summer)

class User():
    def __init__(self, u_id, u_age, u_sex, u_prof, u_zip):
        self.u_id = u_id
        self.average_rating = 0
        self.rated_movies = {}
        self.u_age = u_age
        self.u_sex = u_sex
        self.u_prof = u_prof
        self.u_zip = u_zip
        self.recommended = []

    def add_rating(self, m_id, rat):
        self.rated_movies[m_id] = rat

    def calculate_average_rating(self):
        sum1 = 0
        for movie in self.rated_movies:
            sum1 += self.rated_movies[movie]
        self.average_rating = sum1 / len(self.rated_movies)

    def find_both_rated_movies(self, user2):
        rated = [[],[]]
        for movie in self.rated_movies:
            if int(movie) in user2.rated_movies:
                rated[0].append(self.rated_movies[movie])
                rated[1].append(user2.rated_movies[movie])
        return rated

    def weight(self, user2): #124
        data = self.find_both_rated_movies(user2)
        return cos(data[0], data[1])

    def mean_center(self, movie): #side 121
        sum1 = 0
        user_who_have_seen_this_movie = []

        for user in list_of_users:
            if movie in user.rated_movies:
                user_who_have_seen_this_movie.append(user)

        for user in user_who_have_seen_this_movie:
            sum1 += user.rated_movies[movie] - user.average_rating
        if len(self.rated_movies) == 0 and len (user_who_have_seen_this_movie) == 0:
            return self.average_rating + sum1
        elif len(self.rated_movies) == 0:
            return self.average_rating + (sum1 / len(user_who_have_seen_this_movie))
        elif len(user_who_have_seen_this_movie) == 0:
            return (self.average_rating / len(self.rated_movies)) + sum1
        else:
            return (self.average_rating / len(self.rated_movies)) + (sum1 / len(user_who_have_seen_this_movie))

    def find_k_nearest_neighbour(self, k, movie):
        users = []

        for user in list_of_users:
            #print(user.rated_movies)
            if int(movie) in user.rated_movies:
                #print(movie)
                users.insert(user.u_id, [user, self.weight(user)])

        users.sort(key=lambda x: x[1])

        result = []
        if len(users) <= k:
            return users

        for x in range(k):
            result.append(users[x])

        return result

    def recommend(self, movie):
        users = self.find_k_nearest_neighbour(5, movie)
        sum1 = 0
        for user in users:
            #print(user)
            sum1 += int(user[1])
        if len(users) == 0:
            return self.mean_center(movie)
        else:
            return (sum1/len(users)) + self.mean_center(movie)




all_users_data = open("u.user", "r")

list_of_users = []


for line in all_users_data:
    lines = line.split("|")
    id = int(lines[0])
    age = int(lines[1])
    sex = lines[2]
    prof = lines[3]
    zip = lines[4]

    new_user = User(id, age, sex, prof, zip)
    list_of_users.insert(id, new_user)


if not all_users_data.closed:
    all_users_data.close()

all_ratings = open("u.data", "r")

for line in all_ratings:
    lines = line.split()

    u_id = int(lines[0])
    m_id = int(lines[1])
    rat = int(lines[2])

    list_of_users[u_id-1].add_rating(m_id, rat)

if not all_ratings.closed:
    all_ratings.close()

all_movies = {}

movie_file = open("u.item", "r", encoding= 'ISO-8859-1')
for line in movie_file:
    lines = line.split("|")

    id = lines[0]
    name = lines[1]

    all_movies[id] = name

if not movie_file.closed:
    movie_file.close()

i = 0
for movie in all_movies:
    i += 1
    print(round((i / len(all_movies)) * 100,2), "%")
    for user in list_of_users:
        if movie not in user.rated_movies:
            user.recommended.insert(int(movie), float(user.recommend(movie)))

output = open("data.txt", "w")
for movie in all_movies:
    output.write(str(movie) + "\t")
output.writelines("\n")
for user in list_of_users:
    output.write(str(user.u_id) + "\t")
    for movie in all_movies:
        if movie in user.recommended:
            output.write(str(user.recommended[movie]) + " ")
        else:
            output.write("0 ")
    output.writelines("\n")
if not output.closed:
    output.close()