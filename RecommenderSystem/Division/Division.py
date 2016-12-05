import splitting

def Division(usernr, head_movies, tail_movies, movies, ratings):
    head = 0
    tail = 0
    sum1 = 0

    for movie in range(len(movies)):
        if ratings[usernr][movie] > 0.0:
            sum1 += 1
            if movie in head_movies:
                head += 1

            elif movie in tail_movies:
                tail += 1

            else:
                raise ValueError("well, fuck")

    if head + tail == sum1:
        return head/sum1, tail/sum1

    else:
        raise ValueError("well, fuck")


def recommend(usernr, old_ratings, movies, new_ratings, k):
    head_movies, tail_movies = splitting.get_head_and_tail(80)
    head_percent, tail_percent = Division(usernr, head_movies, tail_movies, movies, old_ratings)

    head_tuple = []
    for movie in head_movies:
        head_tuple.append([new_ratings[usernr][movie], movie])

    head_tuple.sort(key=lambda x: x[0], reverse=True)

    tail_tuple = []
    for movie in tail_movies:
        tail_tuple.append([new_ratings[usernr][movie], movie])

    tail_tuple.sort(key=lambda x: x[0], reverse=True)

    return head_tuple[:head_percent * k][1] + tail_tuple[:tail_percent * k][1]



