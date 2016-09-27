def calculate_averages(movs, m):
    for key in movs:
        amount = 0
        total = 0
        for rate in m[movs[key].id - 1]:
            if rate != 0:
                total += rate
                amount += 1

        if amount == 0:
            movs[key].set_average_rating(0)
        else:
            movs[key].set_average_rating(total / amount)

    amount = 0
    total = 0
    for key in movs:
        if movs[key].rating != 0:
            total += movs[key].rating
            amount += 1

    return total / amount


def calculate_user_bias(user, movies, matrix):
    total = 0
    amount = 0
    for movie in matrix:
        if movie[user.id - 1] != 0:
            total += movie[user.id - 1] - movies[matrix.index(movie) + 1].rating
            amount += 1

    if amount != 0:
        user.set_bias(total / amount)


def calculate_movie_bias(movie, total_average):
    if movie.rating != 0:
        movie.set_bias(movie.rating - total_average)
