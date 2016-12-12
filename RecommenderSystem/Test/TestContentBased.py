from Tests import Input
import unittest
import ContentBased as CB
import copy
import math


class Test(unittest.TestCase, Input):
    def test_content_based(self):
        Rout = [[4.03279555899, 3.0, 3.0, 5.0, 3.63245553203],
                [1.45080666152, 1.73508893593, 5.0, 2.2, 1.73508893593],
                [3.0, 1.0, 3.0, 3.0, 3.0],
                [3.0, 5.0, 3.0, 3.0, 3.0],
                [1.96720444101, 3.0, 3.0, 1.0, 2.36754446797]]

        Rn = CB.do_content_based(copy.deepcopy(self.R), self.M_obj, self.U_obj, False)

        self.assertTrue(self.matrix_equals(Rn, Rout),
                        msg="Output not equal to expected output.\nExpected:\n{}\n\nGot:\n{}".format(
                            self.matrix_to_string(Rout), self.matrix_to_string(Rn)))
        print("Content Based works!")

    def test_user_profile_creation(self):
        user = self.U_obj[1]

        output = CB.UserProfile(user)

        self.assertEqual(output.user.id, 2, "User has wrong id.")
        self.assertListEqual(output.relevant_vector, [0 for x in range(19)], "Relevancy vector initialization error.")
        self.assertListEqual(output.irrelevant_vector, [0 for x in range(19)], "Relevancy vector initialization error.")
        print("UserProfile creation works!")

    def test_relevancy_vector_calculation(self):
        profile = CB.UserProfile(self.U_obj[1])

        expected_relevant = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_irrelevant = [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]

        profile.calculate_relevancy_vectors(self.R, self.M_obj)

        self.assertTrue(self.array_equals(expected_relevant, profile.relevant_vector), "Relevant vector calculated wrong.\nExpected: {}\nGot: {}".format(expected_relevant, profile.relevant_vector))
        self.assertTrue(self.array_equals(expected_irrelevant, profile.irrelevant_vector), "Irrelevant vector calculated wrong.\nExpected: {}\nGot: {}".format(expected_irrelevant, profile.irrelevant_vector))
        print("Relevancy vector calculation works!")

    def test_movie_profile_creation(self):
        expected = [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]

        output = CB.MovieProfile(self.M_obj[3])

        self.assertEqual(output.movie.id, 4, "Movie has wrong id.")
        self.assertTrue(self.array_equals(expected, output.vector), "Movie vecotr calculated wrong.\nExpected: {}\nGot: {}".format(expected, output.vector))
        print("MovieProfile creation works!")

    def test_similarity(self):
        x = [1, 2, 3, 4]
        y = [3, 4, 1, 2]
        expected = 22/(pow(math.sqrt(1 + 4 + 9 + 16), 2))

        output = CB.similarity(x, y)

        self.assertEqual(output, expected)
        print("Similarity works!")

    def test_length(self):
        x = [1, 2, 3, 4]
        expected = math.sqrt(1 + 4 + 9 + 16)

        output = CB.length(x)

        self.assertEqual(output, expected)
        print("Length works!")

    def test_rating_calculation(self):
        user = CB.UserProfile(self.U_obj[1])
        user.calculate_relevancy_vectors(self.R, self.M_obj)
        movie = CB.MovieProfile(self.M_obj[0])
        expected = 3 - 2 * (3/(math.sqrt(5)*math.sqrt(3)))

        output = CB.calculate_rating(user, movie)

        self.assertEqual(output, expected)
        print("Rating calculation works!")
