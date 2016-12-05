import DataAPI


#test
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
