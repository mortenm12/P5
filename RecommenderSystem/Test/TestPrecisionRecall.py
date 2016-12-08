from Tests import Input
import unittest
import PrecisionRecall as PR

class Test(unittest.TestCase, Input):
    def test_precision_recall(self):
        expected = [
            (None, 0.0),
            (0.25, 1.0),
            (0.0, None),
            (1.0, 1.0),
            (None, None)
        ]

        def precision_recall_from_confusion_matrix(confusion_matrix):
            precision = PR.calculate_precision(confusion_matrix)
            recall = PR.calculate_recall(confusion_matrix)
            return precision, recall

        def predicate(rating, user, movie):
            if rating == 0:
                return None
            elif rating >= 4:
                return True
            else:
                return False

        result = {}
        for test in range(0,5):
            result[test] = (precision_recall_from_confusion_matrix(PR.confusion_matrix_generator_from_predicate(predicate, self.R)([0,1,2,4], test)))
            self.assertEqual(result[test], expected[test])