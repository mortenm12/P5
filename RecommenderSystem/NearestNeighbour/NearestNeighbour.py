"""
Implementation of K-Nearest Neighbour, with normalization and meancenter.
Morten Meyer Rasmussen
Every page numbers is a refenece to the book: Recommender Systems Handbook
"""
from DataAPI import *

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


# writes and calculates the ratings into an output file
i = 0

output = open("Output/data.txt", "w")
output.write("ID, ")
for movie in all_movies:
    output.write(str(movie) + ", ")
output.writelines("\n")
for user in list_of_users:
    i += 1
    print(round((i / len(list_of_users)) * 100, 1), "%")
    output.write(str(user.id) + ", ")
    for movie in all_movies:
        if movie not in user.rated_movies:
            output.write(str(round(user.recommend(movie, list_of_users), 1)) + ", ")
        else:
            output.write(str(user.rated_movies[movie]) + ", ")
    output.writelines("\n")
if not output.closed:
    output.close()
