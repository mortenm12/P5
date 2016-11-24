import DataAPI

def get_head_and_tail(k):

    for x in range(1,6):
        directory = "Test" + str(x)

        users = DataAPI.read_users_as_id_list()
        movies = DataAPI.read_movies_as_id_list()
        ratings = DataAPI.read_ratings(directory)

        head = []
        tail = []

        for i in range(0, len(users)):
            head.append([])
            tail.append([])
            for j in range(0, len(movies)):
                head[i].append(0.0)
                tail[i].append(0.0)

        for i in range(0, len(users)):
            sum1 = 0
            for j in range(0,len(movies)):
                if ratings[i][j] > 0.0:
                    sum1 += 1

            if sum1 >= k:
                for j in range(0, len(movies)):
                    head[i][j] = ratings[i][j]

            else:
                for j in range(0, len(movies)):
                    tail[i][j] = ratings[i][j]

    return head, tail
