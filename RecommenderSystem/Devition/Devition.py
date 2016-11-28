def Devition(usernr, head_movies, tail_movies, movies, ratings):
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
                #well, fuck

    if head + tail == sum1:
        return head/sum1, tail/sum1

    else:
        #well, fuck

