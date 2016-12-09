from Tests import Input
import unittest
import copy
import v21NearestNeighbour as NNPC
import math


class Test(unittest.TestCase, Input):
    def test_k_nearest_neighbour_pearson(self):
        Rout = copy.deepcopy(self.R)

        Rn = NNPC.do_K_nearest_neighbour(self.U_id, self.M_id, copy.deepcopy(self.R), K=4, bounding=False, printing=False)

        self.assertTrue(self.matrix_equals(Rn, Rout), msg="Output not equal to expected output.")
        print("K-Nearest Neighbour with Pearson Correlation works!")

    def test_all_average(self):
        expected = self.Global_average

        output = NNPC.calculate_all_average(self.U_id, self.M_id, self.R, printing=False)

        self.assertEqual(output, expected, msg="Output not equal to expected output.")
        print("Calculating global average works!")

    def test_cosine_function(self):
        x = [1, 2, 3, 4]
        y = [3, 4, 1, 2]
        expected = 22/(pow(math.sqrt(1 + 4 + 9 + 16), 2))

        output = NNPC.cos(x, y)

        self.assertEqual(output, expected, msg="Output not equal to expected output.")
        print("Cosine Vector works!")

    def test_length_function(self):
        x = [1, 2, 3, 4]
        expected = math.sqrt(1 + 4 + 9 + 16)

        output = NNPC.length(x)

        self.assertEqual(output, expected, msg="Output not equal to expected output.")
        print("Length of vector function works!")

    def test_weight_function(self):
        u1 = 1
        u2 = 2
        R = [[1, 2, 0, 3],
             [3, 0, 4, 2]]
        M_id = [1, 2, 3, 4]
        U_averages = [2, 3]
        Global_average = 2.5

        expected = 9/(math.sqrt(14.5)*math.sqrt(8.5))

        output = NNPC.weight(u1, u2, R, M_id, U_averages, Global_average)

        self.assertEqual(output, expected, msg="Output not equal to expected output.")
        print("Weight function works!")

    def test_k_nearest_neighbour(self):
        mov = 1
        user = 1
        k = 4
        weights = [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]

        expected = [[0, 0.25]]

        output = NNPC.k_nearest_neighbour(mov, user, k, self.R, self.U_id, weights, self.U_averages)

        self.assertListEqual(output, expected, msg="Output not equal to expected output.")
        print("Neighbour function works!")

    def test_rate(self):
        mov = 1
        user = 1
        k = 4
        weights = [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]

        expected = 0

        output = NNPC.rate(mov, user, self.U_id, self.R, weights, self.U_averages, k)

        self.assertEqual(output, expected, msg="Output not equal to expected output.")
        print("Rate function works!")

    def test_format_time(self):
        t = 7261

        expected = "02:01:01"

        output = NNPC.format_time(t)

        self.assertEqual(expected, output, msg="Output not equal to expected output.")
        print("Time function works!")

    def test_weight_matrix(self):
        expected = [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]

        output = NNPC.calculate_weight_matrix(self.M_id, self.R, self.U_id, 1, self.U_averages, self.Global_average, printing=False)

        self.assertListEqual(expected, output, msg="Output not equal to expected output.")
        print("Weight Matrix function works!")

    def test_user_average(self):
        expected = self.U_averages

        output = NNPC.calculate_user_average_rating(self.M_id, self.R, self.U_id, self.Global_average)

        self.assertListEqual(expected, output, msg="Output not equal to expected output.")
        print("User average function works!")

    def test_movie_average(self):
        expected = self.M_averages

        output = NNPC.calculate_movie_average_rating(self.M_id, self.R, self.U_id, self.Global_average)

        self.assertListEqual(expected, output, msg="Output not equal to expected output.")
        print("Movie average function works!")
