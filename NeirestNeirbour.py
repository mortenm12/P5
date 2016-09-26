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
        ListOfUsers[uid].addRating(mid,rat)
        
    except IndexError:
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
    for x in listOfUsers:
        if x != theUser:
            score = 0
            for movie in x.listOfRatings:
                try:
                    if theUser.listOfRatings[movie]:
                        if x.listOfRatings[movie] == theUser.listOfRatings[movie]:
                            score += 1
                except IndexError:
                    score = score
            if score > bestScore:
                bestUser = x

    return bestUser

print FindNearestNeighbor(100, ListOfUsers).UId
                











            
    

