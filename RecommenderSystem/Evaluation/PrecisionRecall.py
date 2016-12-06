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
def ConfusionMatrixGeneratorFromPredicate(predicate):
    relevantCount = 0
    irrelevantCount = 0
    relevanceMatrix = []

    #Count how many ratings does/doesn't satisfy the predicate.
    #Also record the results in correctnessMatrix in case of a slow predicate.
    for user, userRatings in enumerate(AllRatings):
        relevanceMatrix.append([])
        for movie, rating in enumerate(userRatings):
            isRelevant = predicate(rating, user, movie)
            if isRelevant == True:
                relevantCount += 1
            elif isRelevant == False:
                irrelevantCount += 1
            relevanceMatrix[user].append(isRelevant)

    # ConfusionMatrixGenerator(recommendations, user):
    # Makes a confusion-matrix.
    #
    # recommendations - List of movieids recommended.
    # user - id of user recommended to.
    # return - A confusion-matrix implemented as a dictionary.
    #
    def ConfusionMatrixGenerator(recommendations, user):
        confusionMatrix = {}
        confusionMatrix["TruePositive"] = 0
        confusionMatrix["FalsePositive"] = 0

        # Count how many recommendations does/doesn't satisfy the predicate.
        for movie in recommendations:
            if relevanceMatrix[user][movie] == True:
                confusionMatrix["TruePositive"] += 1
            elif relevanceMatrix[user][movie] == False:
                confusionMatrix["FalsePositive"] += 1

        # Subtract count of recommended from total count to find count of unrecommended.
        confusionMatrix["FalseNegative"] = relevantCount - confusionMatrix["TruePositive"]
        confusionMatrix["TrueNegative"] = irrelevantCount -  confusionMatrix["FalsePositive"]

        return confusionMatrix

    return ConfusionMatrixGenerator

def CalculatePrecision(confusionMatrix):
    return float(confusionMatrix["TruePositive"]) / (confusionMatrix["TruePositive"] + confusionMatrix["FalsePositive"])

def CalculateRecall(confusionMatrix):
    return float(confusionMatrix["TruePositive"]) / (confusionMatrix["TruePositive"] + confusionMatrix["FalseNegative"])

# AveragePrecisionRecall(recommendationLists, predicate):
# Calculates an average precision recall.
# Due to the sparsity of our ratings, only lists with atleast
#     one recommendation having a decidable predicate will be considered.
#
# recommendationLists - A complete list of recommendationlists.
#                       The list is indexed by userid and each list contains the movieids of the recommendations.
# predicate - A predicate function of the form: rating, userid, movieid -> bool or None.
#             Returns weather a recommendation should be recommended. If that's undecidable, returns None.
# return - The average precision and the average recall.
def AveragePrecisionRecall(recommendationLists, predicate):
    precision = 0.0
    recall = 0.0
    validEntries = 0
    #Make the confusion matrix generator for the predicate
    confusionMatrixGenerator = ConfusionMatrixGeneratorFromPredicate(predicate)
    for user, recommendations in enumerate(recommendationLists):
        #Make a confusion matrix for the current recommendationlist
        confusionMatrix = confusionMatrixGenerator(recommendations, user)
        #If the recommendationlist is to be considered
        if confusionMatrix["TruePositive"] + confusionMatrix["FalsePositive"] > 0:
            #Add the results
            precision += CalculatePrecision(confusionMatrix)
            recall += CalculateRecall(confusionMatrix)
            #Increment the valid entries count
            validEntries += 1

    #Prevent taking an average over no entries.
    if validEntries == 0:
        raise NoValidEntriesError
    #Return the averages
    return precision / validEntries, recall / validEntries