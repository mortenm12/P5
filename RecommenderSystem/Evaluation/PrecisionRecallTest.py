import PrecisionRecall
import random

numberOfUsers = 943
numberOfMovies = 1682
numberOfRecommendations = 10

def Predicate(rating, user, movie):
    if rating == 0:
        return None
    elif rating >= 4:
        return True
    else:
        return False

recommendationLists = []
for user in range(numberOfUsers):
    recommendationLists.append(random.sample(range(numberOfMovies), numberOfRecommendations))

result = PrecisionRecall.AveragePrecisionRecall(recommendationLists, Predicate)
print(result)