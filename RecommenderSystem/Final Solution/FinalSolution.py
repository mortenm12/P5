from splitting import *
from v2NearestNeighbour import KNN
import DataAPI
from ContentBased import calculate_recommendation_matrix
from Division import recommend
from PrecisionRecall import AveragePrecisionRecall
test = 1
test_set = "Test" + str(test)

#KNN(test)
head_ratings = DataAPI.read_recommendation_matrix("v2.0NearestNeighbour", test_set)

#calculate_recommendation_matrix(test_set)
tail_ratings = DataAPI.read_recommendation_matrix("Weighted Content Based", test_set)


directory = test_set
users = DataAPI.read_users_as_id_list()
movies = DataAPI.read_movies_as_id_list()
old_ratings = DataAPI.read_ratings(directory)

head_movies, tail_movies = get_head_and_tail(41)
new_ratings = merge(head_movies, tail_movies, head_ratings, tail_ratings, users)

recommendation = []

for user in range(0, len(users)):
    recommendation.insert(user, recommend(user, old_ratings, movies, new_ratings, users, 10))
    print(recommendation[user-1])
    for x in recommendation[user-1]:
        if x >= len(movies):
            print("HERE!!!!!\n\n\n\n\n")



def isRelevant(rating, user, movie):
    if rating == 0:
        return None
    elif rating >= 4:
        return True
    else:
        return False

print (AveragePrecisionRecall(recommendation, isRelevant))
#kør precision recall på recomendationen