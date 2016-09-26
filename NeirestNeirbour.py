class user():
    def __init__(self, UId):
        self.UId = UId
        self.listOfRatings = []
        
    def addRating(self, MId, Rat):
        self.listOfRatings.insert(MId, Rat)


ListOfUsers = []

data = open("u1.test", "r")

line = data.readline()
while line != "":           #read until EOF
    info = line.split()     #split at TAB
    uid = int(info[0])      #UserId
    mid = int(info[1])      #MovieId
    rat = int(info[2])      #Rating
    
    try:
        ListOfUsers[uid].addRating(mid,rat) #if the userId is in the list, add a rating
        
    except IndexError:                      #if the user isn't in the list make a new user and add the rating
        new = user(uid)
        new.addRating(mid,rat)
        ListOfUsers.insert(uid, new)

    line = data.readline()

data.close()
print "i'm done"

def FindNearestNeighbor(uid, listOfUsers):
    bestUser = user(10000)                  
    bestScore = 0
    theUser = listOfUsers[uid]
    for User in listOfUsers:               #for every user in the list
        if User != theUser:                #wich is not the user we are comparing against
            score = 0                    # set the score to 0
            for movie in User.listOfRatings:   #for every movie in the rating list
                try:
                    if theUser.listOfRatings[movie]: #if the movie is in the users rating list
                        if User.listOfRatings[movie] == theUser.listOfRatings[movie]: #and the ratings are equal
                            score += 1          #add 1 to the score
                except IndexError:
                    score = score
            if score > bestScore:   #if score is better than the best score
                bestUser = User        #set the user to the bestuser

    return bestUser

print FindNearestNeighbor(100, ListOfUsers).UId
                











            
    

