class Movie():
    def __init__(self, m_id):
        self.m_id = m_id
        self.rating_list = []
    def add_rating(self, rat):
        self.rating_list.append(rat)

list_of_movies = []

data = open("u1.test", "r")

line = data.readline()
while line != "":  # read until EOF
    info = line.split()  # split at TAB
    mid = int(info[1])  # MovieId
    rat = int(info[2])  # Rating

    try:
        list_of_movies[mid].add_rating(rat) # if the userId is in the list, add a rating

    except IndexError:  # if the user isn't in the list make a new user and add the rating
        new = Movie(mid)
        new.add_rating(rat)
        list_of_movies.insert(mid,new)

    line = data.readline()

data.close()
print("i'm done")

"""def compare_lenght_of_ratings(mov1, mov2):
    if mov1.rating_list.len() < mov2.rating_list.len():
        return 1
    elif mov1.rating_list.len() > mov2.rating_list.len():
        return -1
    else:
        return 0

list_of_movies.sort(compare_lenght_of_ratings)"""

sorted_list = sorted(list_of_movies, key = lambda movie: len(movie.rating_list))

for mov in sorted_list:
    print(mov.m_id, len(mov.rating_list))
