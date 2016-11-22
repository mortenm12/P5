from DataAPI import read_ratings

AllRatings = read_ratings("FullData")

class NoValidEntriesError(Exception):
    pass

def ConfusionMatrixGeneratorFromPredicate(predicate):
    trueCount = 0
    falseCount = 0
    correctnessMatrix = []
    for user, userRatings in enumerate(AllRatings):
        correctnessMatrix.append([])
        for movie, rating in enumerate(userRatings):
            isCorrect = predicate(rating, user, movie)
            if isCorrect == True:
                trueCount += 1
            elif isCorrect == False:
                falseCount += 1
            correctnessMatrix[user].append(isCorrect)

    def ConfusionMatrixGenerator(recommendations, user):
        confusionMatrix = {}
        confusionMatrix["TruePositive"] = 0
        confusionMatrix["FalsePositive"] = 0
        confusionMatrix["TrueNegative"] = trueCount
        confusionMatrix["FalseNegative"] = falseCount

        for movie in recommendations:
            if correctnessMatrix[user][movie] == True:
                confusionMatrix["TruePositive"] += 1
            elif correctnessMatrix[user][movie] == False:
                confusionMatrix["FalsePositive"] += 1

        confusionMatrix["TrueNegative"] -= confusionMatrix["TruePositive"]
        confusionMatrix["FalseNegative"] -= confusionMatrix["FalsePositive"]

        return confusionMatrix

    return ConfusionMatrixGenerator

def CalculatePrecision(confusionMatrix):
    return float(confusionMatrix["TruePositive"]) / (confusionMatrix["TruePositive"] + confusionMatrix["FalsePositive"])

def CalculateRecall(confusionMatrix):
    return float(confusionMatrix["TruePositive"]) / (confusionMatrix["TruePositive"] + confusionMatrix["FalseNegative"])

def AveragePrecisionRecall(recommendationLists, predicate):
    precision = 0.0
    recall = 0.0
    validEntries = 0
    confusionMatrixGenerator = ConfusionMatrixGeneratorFromPredicate(predicate)
    for user, recommendations in enumerate(recommendationLists):
        confusionMatrix = confusionMatrixGenerator(recommendations, user)
        if confusionMatrix["TruePositive"] + confusionMatrix["FalsePositive"] > 0:
            precision += CalculatePrecision(confusionMatrix)
            recall += CalculateRecall(confusionMatrix)
            validEntries += 1

    if validEntries == 0:
        raise NoValidEntriesError
    return precision / validEntries, recall / validEntries