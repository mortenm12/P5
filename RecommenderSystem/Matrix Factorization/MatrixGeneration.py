import numpy


# Read the movies from the item file. OBS: Outdated.
def read_movies():
    D = []
    item_file = open("u.item", 'r', encoding='iso-8859-1')

    for line in item_file:
        mov = line.split('|')
        mid = int(mov[0])
        D.append(mid)

    if not item_file.closed:
        item_file.close()

    return numpy.array(D)


# Read the users from the user file. OBS: Outdated.
def read_users():
    U = []
    user_file = open("u.user", "r")

    for line in user_file:
        user = line.split('|')
        uid = int(user[0])
        U.append(uid)

    if not user_file.closed:
        user_file.close()

    return numpy.array(U)


# Generate a rating matrix based on the user/movie lists from the read_users and read_movies methods. OBS: Outdated.
def generate_matrix(U, D):
    # Generate a 0 initialized matrix.
    R = []
    for uid in U:
        R.insert(uid - 1, [])
        for mid in D:
            R[uid - 1].insert(mid - 1, 0)

    data_file = open("u.data", "r")

    # Insert ratings into the matrix where applicable.
    for line in data_file:
        data = line.split()
        R[int(data[0]) - 1][int(data[1]) - 1] = int(data[2])

    if not data_file.closed:
        data_file.close()

    return numpy.array(R)


