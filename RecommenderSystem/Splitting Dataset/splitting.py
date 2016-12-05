import DataAPI


def get_head_and_tail(k):

    for x in range(1,6):
        directory = "Test" + str(x)

        users = DataAPI.read_users_as_id_list()
        movies = DataAPI.read_movies_as_id_list()
        ratings = DataAPI.read_ratings(directory)

        head_movies = []
        tail_movies = []


        for j in range(0, len(movies)):
            sum1 = 0
            for i in range(0,len(users)):
                if ratings[i][j] > 0.0:
                    sum1 += 1

            if sum1 >= k:
                head_movies.append(j)

            else:
                tail_movies.append(j)

    return head_movies, tail_movies


def merge(head_movies, tail_movies, head_ratings, tail_ratings):
    users = len(head_ratings)
    ratings = []

    for i in range(0, users):
        ratings[i].append([])

    for i in range(0, users):
        for j in head_movies:
            ratings[i][j] = head_ratings[i][j]

        for j in tail_movies:
            ratings[i][j] = tail_ratings[i][j]

    return ratings
