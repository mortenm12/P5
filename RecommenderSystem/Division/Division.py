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

    if head + tail == sum1 and sum1 > 0:
        return head/sum1, tail/sum1

    else:
        return 0.5, 0.5


def recommend(usernr, old_ratings, movies, new_ratings, users, k):
    head_movies, tail_movies = splitting.get_head_and_tail(80)
    head_percent, tail_percent = Division(usernr, head_movies, tail_movies, movies, old_ratings)

    for user in range(0, len(users)):
        for movie in range(0, len(movies)):
            if old_ratings[user][movie] > 0.0:
                new_ratings[user][movie] = 0.0

    head_tuple = []
    for movie in head_movies:
        head_tuple.append([new_ratings[usernr][movie], movie])

    head_tuple.sort(key=lambda x: x[0], reverse=True)

    tail_tuple = []
    for movie in tail_movies:
        tail_tuple.append([new_ratings[usernr][movie], movie])

    tail_tuple.sort(key=lambda x: x[0], reverse=False)

    return_array = []

    for i in range(0, int(round(head_percent * k, 0))):
        return_array.append(head_tuple[i][1])

    for i in range(0, int(round(tail_percent * k, 0))):
        return_array.append(tail_tuple[i][1])

    return return_array




