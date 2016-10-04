import numpy

def read_movies():
    D = []
    item_file = open("u.item", "r")

    for line in item_file:
        mov = line.split('|')
        mid = int(mov[0])
        D.append(mid)

    if not item_file.closed:
        item_file.close()

    return numpy.array(D)


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


def generate_matrix(U, D):
    R = []
    for uid in U:
        R.insert(uid - 1, [])
        for mid in D:
            R[uid - 1].insert(mid - 1, 0)

    data_file = open("u.data", "r")

    for line in data_file:
        data = line.split()
        R[int(data[0]) - 1][int(data[1]) - 1] = int(data[2])

    if not data_file.closed:
        data_file.close()

    return numpy.array(R)


def initialize_latent_factor_matrix(n, K):
    m = []
    for i in range(0, n):
        m.insert(i, [])
        for j in range(0, K):
            m[i].insert(j, 2)

    return numpy.array(m)


