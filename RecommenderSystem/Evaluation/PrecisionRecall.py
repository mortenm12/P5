from DataAPI import read_ratings

AllRatings = read_ratings("FullData")


class NoValidEntriesError(Exception):
    pass


# ConfusionMatrixGeneratorFromPredicate(predicate):
# Makes a confusion matrix generator from a predicate.
# This allows the algorithm to only read through all ratings once per predicate.
#
# predicate - A predicate function of the form: rating, userid, movieid -> bool or None.
#             Returns weather a recommendation should be recommended. If that's undecidable, returns None.
# return - A confusion-matrix generator. (Defined inside function)
#
def confusion_matrix_generator_from_predicate(predicate):
    relevant_count = []
    irrelevant_count = []
    relevance_matrix = []

    # Count how many ratings does/doesn't satisfy the predicate.
    # Also record the results in correctnessMatrix in case of a slow predicate.
    for user, userRatings in enumerate(AllRatings):
        relevance_matrix.append([])
        relevant_count.append(0)
        irrelevant_count.append(0)
        for movie, rating in enumerate(userRatings):
            is_relevant = predicate(rating, user, movie)
            if is_relevant:
                relevant_count[user] += 1
            elif not is_relevant:
                irrelevant_count[user] += 1
            relevance_matrix[user].append(is_relevant)

    # confusion_matrix_generator(recommendations, user):
    # Makes a confusion-matrix.
    #
    # recommendations - List of movieids recommended.
    # user - id of user recommended to.
    # return - A confusion-matrix implemented as a dictionary.
    #
    def confusion_matrix_generator(recommendations, user):
        confusion_matrix = {}
        confusion_matrix["TruePositive"] = 0
        confusion_matrix["FalsePositive"] = 0

        # Count how many recommendations does/doesn't satisfy the predicate.
        for movie in recommendations:
            if relevance_matrix[user][movie]:
                confusion_matrix["TruePositive"] += 1
            elif not relevance_matrix[user][movie]:
                confusion_matrix["FalsePositive"] += 1

        # Subtract count of recommended from total count to find count of unrecommended.
        confusion_matrix["FalseNegative"] = relevant_count[user] - confusion_matrix["TruePositive"]
        confusion_matrix["TrueNegative"] = irrelevant_count[user] - confusion_matrix["FalsePositive"]

        return confusion_matrix

    return confusion_matrix_generator


def calculate_precision(confusion_matrix):
    return float(confusion_matrix["TruePositive"]) / (confusion_matrix["TruePositive"] + confusion_matrix["FalsePositive"])


def calculate_recall(confusion_matrix):
    return float(confusion_matrix["TruePositive"]) / (confusion_matrix["TruePositive"] + confusion_matrix["FalseNegative"])


# average_precision_recall(recommendationLists, predicate):
# Calculates an average precision recall.
# Due to the sparsity of our ratings, only lists with atleast
#     one recommendation having a decidable predicate will be considered.
#
# recommendation_lists - A complete list of recommendationlists.
#                       The list is indexed by userid and each list contains the movieids of the recommendations.
# predicate - A predicate function of the form: rating, userid, movieid -> bool or None.
#             Returns weather a recommendation should be recommended. If that's undecidable, returns None.
# return - The average precision and the average recall.
def average_precision_recall(recommendation_lists, predicate):
    precision = 0.0
    recall = 0.0
    valid_entries = 0

    # Make the confusion matrix generator for the predicate
    confusion_matrix_generator = confusion_matrix_generator_from_predicate(predicate)
    for user, recommendations in enumerate(recommendation_lists):
        # Make a confusion matrix for the current recommendationlist
        confusion_matrix = confusion_matrix_generator(recommendations, user)
        # If the recommendationlist is to be considered
        if confusion_matrix["TruePositive"] + confusion_matrix["FalsePositive"] > 0:
            # Add the results
            precision += calculate_precision(confusion_matrix)
            recall += calculate_recall(confusion_matrix)
            # Increment the valid entries count
            valid_entries += 1

    # Prevent taking an average over no entries.
    if valid_entries == 0:
        raise NoValidEntriesError
    # Return the averages
    return precision / valid_entries, recall / valid_entries
