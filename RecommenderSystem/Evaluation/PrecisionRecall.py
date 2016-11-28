from DataAPI import read_ratings

all_ratings = read_ratings("FullData")


class NoValidEntriesError(Exception):
    pass


def confusion_matrix_generator_from_predicate(predicate):
    true_count = 0
    false_count = 0
    correctness_matrix = []
    for user, user_ratings in enumerate(all_ratings):
        correctness_matrix.append([])
        for movie, rating in enumerate(user_ratings):
            is_correct = predicate(rating, user, movie)
            if is_correct:
                true_count += 1
            elif not is_correct:
                false_count += 1
            correctness_matrix[user].append(is_correct)

    def confusion_matrix_generator(recommendations, user):
        confusion_matrix = {
            "TruePositive": 0,
            "FalsePositive": 0,
            "TrueNegative": true_count,
            "FalseNegative": false_count
        }

        for movie in recommendations:
            if correctness_matrix[user][movie]:
                confusion_matrix["TruePositive"] += 1
            elif not correctness_matrix[user][movie]:
                confusion_matrix["FalsePositive"] += 1

        confusion_matrix["TrueNegative"] -= confusion_matrix["TruePositive"]
        confusion_matrix["FalseNegative"] -= confusion_matrix["FalsePositive"]

        return confusion_matrix

    return confusion_matrix_generator


def calculate_precision(confusion_matrix):
    return float(confusion_matrix["TruePositive"]) / (confusion_matrix["TruePositive"] + confusion_matrix["FalsePositive"])


def calculate_recall(confusion_matrix):
    return float(confusion_matrix["TruePositive"]) / (confusion_matrix["TruePositive"] + confusion_matrix["FalseNegative"])


def average_precision_recall(recommendation_lists, predicate):
    precision = 0.0
    recall = 0.0
    valid_entries = 0
    confusion_matrix_generator = confusion_matrix_generator_from_predicate(predicate)
    for user, recommendations in enumerate(recommendation_lists):
        confusion_matrix = confusion_matrix_generator(recommendations, user)
        if confusion_matrix["TruePositive"] + confusion_matrix["FalsePositive"] > 0:
            precision += calculate_precision(confusion_matrix)
            recall += calculate_recall(confusion_matrix)
            valid_entries += 1

    if valid_entries == 0:
        raise NoValidEntriesError
    return precision / valid_entries, recall / valid_entries
