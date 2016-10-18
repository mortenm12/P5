"""
Implementation of K-Nearest Neighbour, with normalization and meancenter.
Morten Meyer Rasmussen
Every page numbers is a refenece to the book: Recommender Systems Handbook
"""
import math

#a and b is a vector of the same dimensions
#the output is a number between 0 and 1 where 1 is an index of that the two vectors is parallel
def cos(a,b): #page 124
    if lenght_of_vector(a) * lenght_of_vector(b) == 0:
        return 0
    return dot(a,b) / (lenght_of_vector(a) * lenght_of_vector(b))

#a and b is a vector of the same dimensions
#the output is a scalar between a and b
def dot(a,b):
    sum1 = 0
    if len(a) == len(b):
        for x in range(len(a)):
            sum1 += a[x] * b[x]
        return sum1
    else:
        raise IndexError("a and b should be the same length.")

#a is vector
#the output is the lenght og vector a
def lenght_of_vector(a):
    sum1 = 0

    for x in a:
        sum1 += x ** 2

    return math.sqrt(sum1)

#The class user is for storing every users ratings, and recommended movies
class User():

    #u_id is every user identification number
    def __init__(self, u_id):
        self.u_id = u_id
        self.average_rating = 0
        self.rated_movies = {}
        self.recommended = []

    #m_id is the movies identifications number, and rat is the users rating of the movie
    #it stores the rating in the users rated-movies
    def add_rating(self, m_id, rat):
        self.rated_movies[int(m_id)] = rat

    #runs trough the users ratings and finds the average, and store it in the users overage_rating
    def calculate_average_rating(self):
        sum1 = 0
        if len(self.rated_movies) == 0:
            self.average_rating = 0
        else:
            for movie in self.rated_movies:
                sum1 += self.rated_movies[movie]
            self.average_rating = sum1 / len(self.rated_movies)

    #user2 is a user who is not the user self
    #returns an array of both the users ratings of movies the both have seen
    def find_both_rated_movies(self, user2):
        rated = [[],[]]
        for movie in self.rated_movies:
            if int(movie) in user2.rated_movies:
                rated[0].append(self.rated_movies[movie])
                rated[1].append(user2.rated_movies[movie])
        return rated

    #user2 is a user who is not the user self
    #returns the weight between self and user2
    def weight(self, user2): #page 124
        data = self.find_both_rated_movies(user2)
        return cos(data[0], data[1])

    #movie is a movie in the dictionary all_movies
    #Returns the average of the users ratings, and the average of what other rat the movie, compared to normal
    def mean_center(self, movie): #page 121
        sum1 = 0
        user_who_have_seen_this_movie = []

        #makes a list of all users who have seen the movie
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

    #k is the numbers of nearest nieghbour the algorithm should find, and movie is the movie ever nieghbour should have rated
    #returns a list of k numbers of users who have the heighest weight to the user self
    def find_k_nearest_neighbour(self, k, movie):
        users = []

        for user in list_of_users:
            if int(movie) in user.rated_movies:
                users.insert(user.u_id, [user, self.weight(user)])

        users.sort(key=lambda x: x[1])

        return users[:k]

    #movie is a movie in the dictionary all_movies
    #return a recommendation for the user self on movie
    def recommend(self, movie): #page 115
        users = self.find_k_nearest_neighbour(5, movie)
        sum1 = 0
        sum2 = 0
        for user in users:
            sum1 += user[1] * user[0].rated_movies[int(movie)]
            sum2 += user[1]
        if sum2 == 0:
            return self.mean_center(movie)
        else:
            return (sum1/sum2) + self.mean_center(movie)



#loader user data into the list_of_users
all_users_data = open("u.user", "r")

list_of_users = []

for line in all_users_data:
    lines = line.split("|")
    id = int(lines[0])

    new_user = User(id)
    list_of_users.insert(id, new_user)


if not all_users_data.closed:
    all_users_data.close()

all_ratings = open("u1.test", "r")

for line in all_ratings:
    lines = line.split()

    u_id = int(lines[0])
    m_id = int(lines[1])
    rat = int(lines[2])

    list_of_users[u_id-1].add_rating(m_id, rat)

if not all_ratings.closed:
    all_ratings.close()

#loader all the movies into all_movies
all_movies = {}

movie_file = open("u.item", "r", encoding= 'ISO-8859-1')
for line in movie_file:
    lines = line.split("|")

    id = lines[0]
    name = lines[1]

    all_movies[id] = name

if not movie_file.closed:
    movie_file.close()

#run throug all users and calculates their average rating
for user in list_of_users:
    user.calculate_average_rating()


#writer and calculates the ratings into an output file
i = 0

output = open("data.txt", "w")
output.write("ID, ")
for movie in all_movies:
    output.write(str(movie) + ", ")
output.writelines("\n")
for user in list_of_users:
    i += 1
    print(round((i / len(list_of_users)) * 100,1), "%")
    output.write(str(user.u_id) + ", ")
    for movie in all_movies:
        if movie not in user.rated_movies:
            output.write(str(round(user.recommend(movie),1)) + ", ")
        else:
            output.write(str(user.rated_movies[movie]) + ", ")
    output.writelines("\n")
if not output.closed:
    output.close()
