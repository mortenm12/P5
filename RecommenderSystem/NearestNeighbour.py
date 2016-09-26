class User:
    def __init__(self, u_id):
        self.u_id = u_id
        self.list_of_ratings = []

    def add_rating(self, m_id, rating):
        self.list_of_ratings.insert(m_id, rating)


ListOfUsers = []

data = open("u1.test", "r")

line = data.readline()
while line != "":  # read until EOF
    info = line.split()  # split at TAB
    uid = int(info[0])  # UserId
    mid = int(info[1])  # MovieId
    rat = int(info[2])  # Rating

    try:
        ListOfUsers[uid].addRating(mid, rat)  # if the userId is in the list, add a rating

    except IndexError:  # if the user isn't in the list make a new user and add the rating
        new = User(uid)
        new.add_rating(mid, rat)
        ListOfUsers.insert(uid, new)

    line = data.readline()

data.close()
print("i'm done")


def find_nearest_neighbor(u_id, list_of_users):
    best_user = User(10000)
    best_score = 0
    the_user = list_of_users[u_id]
    for user in list_of_users:  # for every user in the list
        if user != the_user:  # wich is not the user we are comparing against
            score = 0  # set the score to 0
            for movie in user.listOfRatings:  # for every movie in the rating list
                try:
                    if the_user.listOfRatings[movie]:  # if the movie is in the users rating list
                        if user.listOfRatings[movie] == the_user.listOfRatings[movie]:  # and the ratings are equal
                            score += 1  # add 1 to the score
                except IndexError:
                    score = score
            if score > best_score:  # if score is better than the best score
                best_user = user  # set the user to the bestuser

    return best_user


print(find_nearest_neighbor(100, ListOfUsers).UId)
