import DataAPI


def get_head_and_tail(k,test_set_number):

        directory = "Test" + str(test_set_number)

        users = DataAPI.read_users_as_id_list()
        movies = DataAPI.read_movies_as_id_list()
        ratings = DataAPI.read_ratings(directory)

        head_movies = []
        tail_movies = []
        rating_tuple = []

        for j in range(0, len(movies)):
            sum1 = 0
            for i in range(0, len(users)):
                if ratings[i][j] > 0.0:
                    sum1 += 1
            rating_tuple.append([sum1, j])
        rating_tuple.sort(key=lambda x: x[0], reverse=True)

        head_movies = rating_tuple[:k]
        tail_movies = rating_tuple[k:]

        for x in range(len(head_movies)):
            head_movies[x] = head_movies[x][1]

        for x in range(len(tail_movies)):
            tail_movies[x] = tail_movies[x][1]

        """for j in range(0, len(movies)):
            sum1 = 0
            for i in range(0, len(users)):
                if ratings[i][j] > 0.0:
                    sum1 += 1

            if sum1 >= k:
                head_movies.append(j)

            else:
                tail_movies.append(j)"""

        return head_movies, tail_movies
