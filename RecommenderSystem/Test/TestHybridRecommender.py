from Tests import Input
import unittest
import FinalSolution as HR


class Test(unittest.TestCase, Input):
    def test_head_tail(self):
        head, tail = HR.get_head_and_tail(2, self.U_id, self.M_id, self.R)

        expected_head = [1, 3]
        expected_tail = [0, 2, 4]

        self.assertListEqual(expected_head, head)
        self.assertListEqual(expected_tail, tail)
        print("Head and Tail splitting works!")

    def test_is_relevant(self):
        r1 = 0
        r2 = 3
        r3 = 5

        o1 = HR.is_relevant(r1, None, None)
        o2 = HR.is_relevant(r2, None, None)
        o3 = HR.is_relevant(r3, None, None)

        self.assertIsNone(o1)
        self.assertFalse(o2)
        self.assertTrue(o3)
        print("is_relevant works!")

    def test_merge(self):
        R_head = [[1, 2, 3, 4, 5],
                  [2, 3, 4, 5, 1],
                  [3, 4, 5, 1, 2],
                  [4, 5, 1, 2, 3],
                  [5, 1, 2, 3, 4]]
        R_tail = [[5, 1, 2, 3, 4],
                  [1, 2, 3, 4, 5],
                  [2, 3, 4, 5, 1],
                  [3, 4, 5, 1, 2],
                  [4, 5, 1, 2, 3]]
        expected = [[5, 2, 2, 4, 4],
                    [1, 3, 3, 5, 5],
                    [2, 4, 4, 1, 1],
                    [3, 5, 5, 2, 2],
                    [4, 1, 1, 3, 3]]

        output = HR.merge(self.Head, self.Tail, R_head, R_tail, self.U_id)

        self.assertListEqual(expected, output)
        print("Merge works!")

    def test_division(self):
        user = 1
        expected_h, expected_t = 0.25, 0.75

        h, t = HR.division(user, self.Head, self.Tail, self.M_id, self.R)

        self.assertEqual(expected_h, h)
        self.assertEqual(expected_t, t)
        print("Division works!")

    def test_recommend(self):
        user = 1
        new_R = [[5, 2, 2, 4, 4],
                 [1, 3, 3, 5, 5],
                 [2, 4, 4, 1, 1],
                 [3, 5, 5, 2, 2],
                 [4, 1, 1, 3, 3]]
        expected = [3]

        output = HR.recommend(user, self.R, self.M_id, new_R, self.U_id, 4, self.Head, self.Tail)

        self.assertListEqual(expected, output)
        print("Recommend works!")