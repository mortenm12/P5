import unittest
import numpy
import MatrixFactorization as MF
import ContentBased as CB
import v20NearestNeighbour as NNCV
import v21NearestNeighbour as NNPC
import PrecisionRecall as PR
import DataAPI
import copy


class Test(unittest.TestCase):
    R = [[0, 0, 0, 4, 0],
         [3, 2, 4, 0, 2],
         [0, 3, 0, 0, 0],
         [0, 4, 0, 0, 0],
         [0, 0, 0, 2, 0]]
    R = numpy.array(R)
    P = [[2.0, 1.0],
         [1.0, 2.0],
         [2.0, 1.0],
         [1.0, 2.0],
         [2.0, 1.0]]
    P = numpy.array(P)
    Q = [[1.0, 2.0],
         [2.0, 1.0],
         [1.0, 2.0],
         [2.0, 1.0],
         [1.0, 2.0]]
    Q = numpy.array(Q)
    U_id = [1, 2, 3, 4, 5]
    M_id = [1, 2, 3, 4, 5]
    U_obj = [DataAPI.User(1), DataAPI.User(2), DataAPI.User(3), DataAPI.User(4), DataAPI.User(5)]
    M_obj = [DataAPI.Movie(1, None, [1, 2, 16]),
         DataAPI.Movie(2, None, [5, 14]),
         DataAPI.Movie(3, None, [8]),
         DataAPI.Movie(4, None, [1, 2, 4, 9, 15]),
         DataAPI.Movie(5, None, [1, 16])]
    U_obj = DataAPI.add_rating_metrics_to_users(M_obj, U_obj, R)

    def test_precision_recall(self):
        PR.all_ratings = Test.R
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
            return (precision, recall)

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

    def test_matrix_factorization(self):
        Pout = [[2.18829953982, 1.09414976991],
                [0.463989295055, 1.43526480365],
                [1.47961223593, 0.755377088731],
                [1.31925163182, 2.14741120978],
                [1.11549196971, 0.557745984857]]
        Pout = numpy.array(Pout)
        Qout = [[0.872357453835, 1.80551163715],
                [1.57276657582, 0.89592183339],
                [1.14111454636, 2.39590283972],
                [1.45476055549, 0.727380277744],
                [0.702312974788, 1.19545676409]]
        Pout = numpy.array(Pout)
        K = 2
        steps = 10
        alpha = 0.05
        beta = 0.002
        Pn, Qn = MF.matrix_factorization(self.P, self.Q, copy.deepcopy(self.R), K, steps, alpha, beta, False)
        self.assertTrue(matrix_equals(Qn, Qout))
        self.assertTrue(matrix_equals(Pn, Pout))
        print("Matrix Factorization works!")

    def test_content_based(self):
        Rout = [[4.03279555899, 3.0, 3.0, 5.0, 3.63245553203],
                [1.45080666152, 1.73508893593, 5.0, 2.2, 1.73508893593],
                [3.0, 1.0, 3.0, 3.0, 3.0],
                [3.0, 5.0, 3.0, 3.0, 3.0],
                [1.96720444101, 3.0, 3.0, 1.0, 2.36754446797]]

        Rn = CB.do_content_based(copy.deepcopy(self.R), self.M_obj, self.U_obj, False)

        self.assertTrue(matrix_equals(Rn, Rout))
        print("Content Based works!")

    def test_k_nearest_neighbour_cosine(self):
        Rout = copy.deepcopy(self.R)

        Rn = NNCV.do_nearest_neighbour(self.U_id, self.M_id, copy.deepcopy(self.R), printing=False, bounding=False)

        self.assertTrue(matrix_equals(Rn, Rout))
        print("K-Nearest Neighbour with Cosine Vector works!")

    def test_k_nearest_neighbour_pearson(self):
        Rout = copy.deepcopy(self.R)

        Rn = NNPC.do_nearest_neighbour(self.U_id, self.M_id, copy.deepcopy(self.R), printing=False, bounding=False)

        self.assertTrue(matrix_equals(Rn, Rout))
        print("K-Nearest Neighbour with Pearson Correlation works!")


def matrix_equals(x, y):
    for i in range(len(x)):
        for j in range(len(x[0])):
            if not float_equals(x[i][j], y[i][j]):
                return False
    return True


def float_equals(x, y):
    if x - y > 0.0000001:
        return False
    elif x - y < -0.0000001:
        return False
    else:
        return True