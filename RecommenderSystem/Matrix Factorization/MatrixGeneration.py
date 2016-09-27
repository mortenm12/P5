from Classes import Movie, User
from CalculationOfAverages import *

movie_ids = []
movies = {}
user_ids = []
users = {}
matrix = []

item_file = open("u.item", "r")

for line in item_file:
    mov = line.split('|')
    id = int(mov[0])
    movie_ids.append(id)
    movies[id] = Movie(id)

item_file.close()

user_file = open("u.user", "r")

for line in user_file:
    user = line.split('|')
    id = int(user[0])
    user_ids.append(id)
    users[id] = User(id)

user_file.close()

for mid in movie_ids:
    matrix.insert(mid - 1, [])
    for uid in user_ids:
        matrix[mid - 1].insert(uid - 1, 0)

data_file = open("u.data", "r")

for line in data_file:
    data = line.split()
    matrix[int(data[1]) - 1][int(data[0]) - 1] = int(data[2])

data_file.close()

total_average_rating = calculate_averages(movies, matrix)

for key in movies:
    calculate_movie_bias(movies[key], total_average_rating)

for key in users:
    calculate_user_bias(users[key], movies, matrix)

for i in range(0, len(matrix)):
    for j in range(0, len(matrix[i])):
        if matrix[i][j] == 0:
            rating = total_average_rating + movies[i + 1].bias + users[j + 1].bias
            if rating <= 0:
                matrix[i][j] = 0
            else:
                matrix[i][j] = rating

result_file = open("result", "w")

for movie in matrix:
    for user in movie:
        result_file.write("%.2f " % user)
    result_file.write("\n")

result_file.close()
