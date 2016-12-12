import PrecisionRecall
import random

number_of_users = 943
number_of_movies = 1682
number_of_recommendations = 10


def predicate(rating, user, movie):
    if rating == 0:
        return None
    elif rating >= 4:
        return True
    else:
        return False

recommendation_lists = []
for user in range(number_of_users):
    recommendation_lists.append(random.sample(range(number_of_movies), number_of_recommendations))

result = PrecisionRecall.average_precision_recall(recommendation_lists, predicate)
print(result)
