from Tests import Input
import unittest
import PrecisionRecall as PR

class Test(unittest.TestCase, Input):
    def test_precision_recall(self):
        PR.all_ratings = self.R
        expected = [
            (1, 1),
            (0.25, 1),
            (0, None),
            (1, 1),
            (0, None)
        ]

        def precision_recall_from_confusion_matrix(confusion_matrix):
            if confusion_matrix["TruePositive"] + confusion_matrix["FalsePositive"] > 0:
                precision = PR.calculate_precision(confusion_matrix)
            else:
                precision = None
            if confusion_matrix["TruePositive"] + confusion_matrix["FalseNegative"] > 0:
                recall = PR.calculate_recall(confusion_matrix)
            else:
                recall = None
            return precision, recall

        def predicate(rating, user, movie):
            if rating == 0:
                return None
            elif rating >= 4:
                return True
            else:
                return False

        result = []
        for test in range(0,5):
            result.append(precision_recall_from_confusion_matrix(PR.confusion_matrix_generator_from_predicate(predicate)(range(0, 5), test)))
            self.assertEqual(result[test], expected[test])