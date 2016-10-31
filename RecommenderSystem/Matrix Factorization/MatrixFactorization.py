"""
Implementation of Matrix Factorization by Rasmus Jensen
"""
# Imports
from DataAPI import *
import time
import numpy


class MatrixFactorization:
    def __init__(self, test_set, K=20, steps=5000):
        self.test_set = test_set
        # Initialize matrices and values.
        self.R = read_ratings(self.test_set)
        self.R = numpy.array(self.R)

        self.K = K
        self.P = numpy.random.rand(len(self.R), self.K)
        self.Q = numpy.random.rand(len(self.R[0]), self.K)

        # Run algorithm on matrices.
        self.matrix_factorization(steps=steps)

        # Calculate recommendation and write it to recommendation file.
        # calculate_recommendations(nP, nQ, R, test_set)

        # Calculate and write all matrices to files for inspection and saving purposes.
        self.R_final = numpy.dot(self.P, self.Q.T)
        self.write_numpy_matrix(self.R, "R_original.data")
        self.write_numpy_matrix(self.R_final, "ratings.data")
        self.write_factor_matrix(self.P, "P.data")
        self.write_factor_matrix(self.Q, "Q.data")
        self.R_bounded = None
        self.bound_results()

    # Algorithm to write a matrix to a file
    def write_numpy_matrix(self, m, file):
        result = open("Output/" + self.test_set + "/" + file, "w")
        result.write(" ID , " + ", ".join(str(x) for x in range(1, len(m[0]) + 1)) + "\n")
        for i in range(0, len(m)):
            result.write("{:>4d}, ".format(i + 1))
            result.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
            result.write("\n")

        if not result.closed:
            result.close()

    def write_factor_matrix(self, m, file):
        result = open("Output/" + self.test_set + "/" + file, "w")
        for i in range(0, len(m)):
            result.write("{:>4d}, ".format(i + 1))
            result.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
            result.write("\n")

        if not result.closed:
            result.close()

    # Method to calculate the recommendations from the P and Q matrices.
    def calculate_recommendations(self):
        recommendation_file = open("Output/" + self.test_set + "/UserRecommendations", "w")

        # For each user vector find the most similar item vector by calculating the dot products.
        a = 0
        most_accurate_product = 0
        for i in range(0, len(self.P)):
            for j in range(0, len(self.Q)):
                result = numpy.dot(self.P[i, :], self.Q[j, :])
                if result > most_accurate_product and self.R[i][j] == 0.0:
                    most_accurate_product = result
                    a = j
            recommendation_file.write("User: " + str(i) + ", Recommended movie: " + str(a) + "Rating: " + str(most_accurate_product) + "\n")

        if not recommendation_file.closed:
            recommendation_file.close()


    # The factorization algorithm.
    # The point of this algorithm is to stepwise approximate P and Q so that PxQ approximates R.
    # Takes 4 parameters:
    #   R, the N x M user/item rating matrix.
    #   P, the N x K user latent factor space matrix, initially random.
    #   Q, the M x K item latent factor space matrix, initially random.
    #   K, the amount of latent factors.
    #
    # And has 3 other default parameters:
    #   steps, the amount of iteration the algorithm will run for.
    #   alpha, the approximation variable, defining how fast the algorithm converges.
    #   beta, the normalization variable, defining how much to avoid overfitting.
    def matrix_factorization(self, steps=5000, alpha=0.0002, beta=0.02):
        # Transposes the Q matrix, so the dot product of P and Q can be taken.
        self.Q = self.Q.T

        # The main algorithm.
        for step in range(0, steps):

            # Printing progress.
            print(step, end=' ')
            print(time.asctime(time.localtime(time.time())))

            # Iterates over the R matrix, only doing something if a rating has been given
            for i in range(len(self.R)):
                for j in range(len(self.R[i])):

                    # If a rating has been given, calculate the error by getting the dot product of the user and item
                    # vectors in the latent vector spaces corresponding to the rating
                    if self.R[i][j] > 0:
                        eij = self.R[i][j] - numpy.dot(self.P[i, :], self.Q[:, j])

                        # Calculate the new entries in the latent factor spaces.
                        for k in range(0, self.K):
                            self.P[i][k] = self.P[i][k] + alpha * (2 * eij * self.Q[k][j] - beta * self.P[i][k])
                            self.Q[k][j] = self.Q[k][j] + alpha * (2 * eij * self.P[i][k] - beta * self.Q[k][j])

            # Calculate the average error of PxQ from R.
            e = 0
            for i in range(0, len(self.R)):
                for j in range(0, len(self.R[i])):
                    if self.R[i][j] > 0:
                        e += pow(self.R[i][j] - numpy.dot(self.P[i, :], self.Q[:, j]), 2)
                        for k in range(0, self.K):
                            e += (beta / 2) * (pow(self.P[i][k], 2) + pow(self.Q[k][j], 2))

            # If the error is arbitrarily small, stop execution to avoid useless running time.
            if e < 0.001:
                break

        self.Q = self.Q.T

    @staticmethod
    def calculate_k_recommendations(user, k, test_set):
        R = read_ratings(test_set)
        P, Q = read_factor_matrices(test_set)
        P = numpy.array(P)
        Q = numpy.array(Q)

        ratings = []
        for i in range(len(Q)):
            if R[user - 1][i] == 0.0:
                ratings.append([i + 1, numpy.dot(P[user, :], Q[i, :])])

        return sorted(ratings, key=lambda x: x[1], reverse=True)[:k]

    def bound_results(self):
        self.R_bounded = self.R_final.copy()
        for i in range(len(self.R_bounded)):
            for j in range(len(self.R_bounded[0])):
                if self.R_bounded[i, j] > 5:
                    self.R_bounded[i, j] = 5
                elif self.R_bounded[i, j] < 1:
                    self.R_bounded[i, j] = 1

        self.write_numpy_matrix(self.R_bounded, "bounded_ratings.data")


#test_1 = MatrixFactorization("Test1")
test_2 = MatrixFactorization("Test2")
test_3 = MatrixFactorization("Test3")
test_4 = MatrixFactorization("Test4")
test_5 = MatrixFactorization("Test5")