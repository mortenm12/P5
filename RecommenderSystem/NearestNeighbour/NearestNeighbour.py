"""
Implementation of K-Nearest Neighbour, with normalization and mean center.
Morten Meyer Rasmussen
Every page numbers is a reference to the book: Recommender Systems Handbook
"""
from DataAPI import *
from AuxillaryMath import *
import time


# user2 is a user who is not the user self
# returns an array of both the users ratings of movies the both have seen
def find_both_rated_movies(user1, user2):
    rated = [[], []]
    for movie in user1.rated_movies:
        if int(movie) in user2.rated_movies:
            rated[0].append(user1.rated_movies[movie])
            rated[1].append(user2.rated_movies[movie])
    return rated


# user2 is a user who is not the user self
# returns the weight between self and user2
def weight(user1, user2):  # page 124
    data = find_both_rated_movies(user1, user2)
    return cos(data[0], data[1])


# movie is a movie in the dictionary all_movies
# Returns the average of the users ratings, and the average of what other rat the movie, compared to normal
def mean_center(user1, movie, list_of_users):  # page 121
    sum1 = 0
    user_who_have_seen_this_movie = []

    # makes a list of all users who have seen the movie
    for user2 in list_of_users:
        if movie in user2.rated_movies:
            user_who_have_seen_this_movie.append(user2)

    for user2 in user_who_have_seen_this_movie:
        sum1 += user2.rated_movies[movie] - user2.average_rating

    if len(user1.rated_movies) == 0 and len(user_who_have_seen_this_movie) == 0:
        return user1.average_rating + sum1
    elif len(user1.rated_movies) == 0:
        return user1.average_rating + (sum1 / len(user_who_have_seen_this_movie))
    elif len(user_who_have_seen_this_movie) == 0:
        return (user1.average_rating / len(user1.rated_movies)) + sum1
    else:
        return (user1.average_rating / len(user1.rated_movies)) + (sum1 / len(user_who_have_seen_this_movie))


# k is the numbers of neighbours the algorithm should find, and movie is the movie ever neighbour should have rated
# returns a list of k numbers of users who have the highest weight to the user self
def find_k_nearest_neighbour(user1, k, movie, list_of_users):
    users = []

    for user2 in list_of_users:
        if int(movie) in user2.rated_movies:
            users.insert(user2.id, [user2, weight(user1, user2)])

    users.sort(key=lambda x: x[1])

    return users[:k]


# movie is a movie in the dictionary all_movies
# return a recommendation for the user self on movie
def recommend(user1, movie, list_of_users):  # page 115
    users = find_k_nearest_neighbour(user1, 5, movie, list_of_users)
    sum1 = 0
    sum2 = 0
    for user2 in users:
        sum1 += user2[1] * user2[0].rated_movies[int(movie)]
        sum2 += user2[1]
    if sum2 == 0:
        return mean_center(user1, movie, list_of_users)
    else:
        return (sum1 / sum2) + mean_center(user1, movie, list_of_users)

def format_time(t):
    if t < 1:
        return "00:00:00"
    else:
        t_int = int(t)
        h = t_int / 3600
        h_rest = t_int % 3600
        m = h_rest / 60
        s = h_rest % 60
        return "{:02d}".format(int(h)) + ":" + "{:02d}".format(int(m)) + ":" + "{:02d}".format(int(s))

# loader user data into the list_of_user
list_of_users = read_users_as_object_list()

ratings = read_ratings_as_list("Test1")

for rating in ratings:
    u_id = rating[0]
    m_id = rating[1]
    rat = rating[2]
    list_of_users[u_id-1].add_rating(m_id, rat)

# loads all the movies into all_movies
all_movies = read_movies_as_id_name_dict()

# run through all users and calculates their average rating
for user in list_of_users:
    user.calculate_average_rating()


rating_matrix = []
for i in range(0, len(list_of_users)):
    rating_matrix.append([])
    for j in range(0, len(all_movies)):
        rating_matrix[i].append(0.0)

i = 0
starting_time = time.time()
for user in list_of_users:
    i += 1

    current_time = time.time()
    elapsed_time = current_time - starting_time
    remaining_time = ((elapsed_time * len(list_of_users)) / i) - elapsed_time

    print(round((i / len(list_of_users)) * 100, 1), "% tid brugt: ", format_time(elapsed_time), " tid tilbage: ", format_time(remaining_time))
    for movie in all_movies:
        if movie not in user.rated_movies:
            rating_matrix[user.id-1][int(movie)-1] = recommend(user, movie, list_of_users)
        else:
            rating_matrix[user.id][int(movie)] = user.rated_movies[movie]

for i in range(0, len(list_of_users)):
    for j in range(0, len(all_movies)):
        if rating_matrix[i][j] > 5:
            rating_matrix[i][j] = 5
        elif rating_matrix[i][j] < 1:
            rating_matrix[i][j] = 1


# writes the ratings into an output file
i = 0
test_set = "Test1"
output = open("Output/" + test_set + "/ratings.data", "w")
output.write("   ID, ")
output.write(", ".join(["{:>5d}".format(movie) for movie in all_movies]))
output.writelines("\n")
for user in range(0, len(list_of_users)):
    i += 1
    print(round((i / len(list_of_users)) * 100, 1), "%")
    output.write("{:>5d}".format(list_of_users[user].id) + ", ")
    j = 1
    for movie in range(0, len(all_movies)):
        output.write("{: .2f}".format(rating_matrix[user][movie]) + (", " if j < len(all_movies) else ""))

        j += 1
    output.writelines("\n")
if not output.closed:
    output.close()
