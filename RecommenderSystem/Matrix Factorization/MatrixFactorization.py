"""
Implementation of Matrix Factorization by Rasmus Jensen
"""
# Imports
from DataAPI import *
import time
import numpy


# Algorithm to write a matrix to a file
def write_numpy_matrix(m, file, test_set):
    result = open("Output/" + test_set + "/" + file, "w")
    result.write(" ID , " + ", ".join(str(x) for x in range(1, len(m[0]) + 1)) + "\n")
    for i in range(0, len(m)):
        result.write("{:>4d}, ".format(i + 1))
        result.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        result.write("\n")

    if not result.closed:
        result.close()


def write_factor_matrix(m, file, test_set):
    result = open("Output/" + test_set + "/" + file, "w")
    for i in range(0, len(m)):
        result.write("{:>4d}, ".format(i + 1))
        result.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        result.write("\n")

    if not result.closed:
        result.close()


# Method to calculate the recommendations from the P and Q matrices.
def calculate_recommendations(P, Q, R, test_set):
    recommendation_file = open("Output/" + test_set + "/UserRecommendations", "w")

    # For each user vector find the most similar item vector by calculating the dot products.
    a = 0
    most_accurate_product = 0
    for i in range(0, len(P)):
        for j in range(0, len(Q)):
            result = numpy.dot(P[i, :], Q[j, :])
            if result > most_accurate_product and R[i][j] == 0.0:
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
def matrix_factorization(P, Q, R, K, steps=5000, alpha=0.07, beta=0.02, debug=False):
    if debug:
        log_file = open("Log.txt", "a")
        log_file.write("For: K=" + str(K) + " steps=" + str(steps) + " alpha=" + str(alpha) + " beta=" + str(beta) + ":\n")
    # Transposes the Q matrix, so the dot product of P and Q can be taken.
    Q = Q.T

    prev_e = 0
    # The main algorithm.

    """
    nR = numpy.dot(P, Q)
    print("\n R:" + "".join(" " for x in range((7 * len(R[0])) - 4)) + "|" + "  P:" + "".join(
        " " for x in range((7 * len(P[0])) - 4)) + "|" + "  Q:" + "".join(
        " " for x in range((7 * len(Q)) - 4)))
    for t in range(len(nR) if len(nR) > len(nR[0]) else len(nR[0])):
        print(((", ".join(["{: 2.2f}".format(x) for x in nR[t, :]])) if t < len(nR) else (
            "  ".join(["     " for x in range(len(R))]))) + " | " + (
                  (", ".join(["{: 2.2f}".format(x) for x in P[t, :]])) if t < len(P) else (
                      "  ".join(["    " for x in range(len(P))]))) + " | " + (
                  (", ".join(["{: 2.2f}".format(x) for x in Q[:, t]])) if t < len(Q[0]) else ("  ").join(
                      ["    " for x in range(len(Q[0]))])))
    """

    for step in range(0, steps):

        # Printing progress.
        print("{:4d}".format(step), end=' ')
        print(time.ctime(time.time()), end='')

        # Iterates over the R matrix, only doing something if a rating has been given
        for i in range(len(R)):
            for j in range(len(R[i])):

                # If a rating has been given, calculate the error by getting the dot product of the user and item
                # vectors in the latent vector spaces corresponding to the rating
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])

                    """
                    if debug:
                        if numpy.isnan(eij):
                            print(str(R[i][j]) + " " + str(P[i, :]) + " " + str(Q[:, j]))
                            return P, Q.T
                    """

                    # Calculate the new entries in the latent factor spaces.
                    for k in range(0, K):
                        Pik = P[i][k]
                        Qkj = Q[k][j]
                        P[i][k] = Pik + (alpha * ((2 * eij * Qkj) - (beta * Pik)))
                        Q[k][j] = Qkj + (alpha * ((2 * eij * Pik) - (beta * Qkj)))

                        """
                        if debug:
                            if numpy.isinf(P[i][k]) or numpy.isinf(Q[k][j]):
                                print(str(Pik) + " " + str(Qkj) + " " + str(eij))
                                return P, Q.T
                            else:
                                print("P[{:d}][{:d}]: {:f} = {:f} + {:f} * (2 * {:f} * {:f} - {:f} * {:f}".format(i, k, P[i][k], Pik, alpha, eij, Qkj, beta, Pik))
                                print("Q[{:d}][{:d}]: {:f} = {:f} + {:f} * (2 * {:f} * {:f} - {:f} * {:f}".format(k, j, Q[k][j], Qkj, alpha, eij, Pik, beta, Qkj))
                        """
        nR = numpy.dot(P, Q)

        """
        print("\n R:" + "".join(" " for x in range((7 * len(R[0])) - 4)) + "|" + "  P:" + "".join(
            " " for x in range((7 * len(P[0])) - 4)) + "|" + "  Q:" + "".join(
            " " for x in range((7 * len(Q)) - 4)))
        for t in range(len(nR) if len(nR) > len(nR[0]) else len(nR[0])):
            print(((", ".join(["{: 2.2f}".format(x) for x in nR[t, :]])) if t < len(nR) else (
            "  ".join(["     " for x in range(len(R))]))) + " | " + (
                  (", ".join(["{: 2.2f}".format(x) for x in P[t, :]])) if t < len(P) else (
                  "  ".join(["    " for x in range(len(P))]))) + " | " + (
                  (", ".join(["{: 2.2f}".format(x) for x in Q[:, t]])) if t < len(Q[0]) else ("  ").join(
                      ["    " for x in range(len(Q[0]))])))
        """

        # Calculate the average error of PxQ from R.
        e = 0
        for i in range(0, len(R)):
            for j in range(0, len(R[i])):
                if R[i][j] > 0:
                    e += pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(0, K):
                        e += (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))

        # If the error is arbitrarily small, stop execution to avoid useless running time.
        if debug:
            log_file.write(str(step) + " Error = " + "{:.2f}".format(float(e)) + "\n")
            print(" Error = " + "{:.2f}".format(float(e)))
        else:
            print("")

        if prev_e != 0 and prev_e - e < 0.1:
            break

        prev_e = e

    if debug:
        log_file.write("\n")
        if not log_file.closed:
            log_file.close()

    return P, Q.T


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


def bound_results(R_final, test_set):
    R_bounded = R_final.copy()
    for i in range(len(R_bounded)):
        for j in range(len(R_bounded[0])):
            if R_bounded[i, j] > 5:
                R_bounded[i, j] = 5
            elif R_bounded[i, j] < 1:
                R_bounded[i, j] = 1

    write_numpy_matrix(R_bounded, "bounded_ratings.data", test_set)


def do_factorization(test_set, K=20, steps=5000, alpha=0.0002, beta=0.02, debug=False):
    # Initialize matrices and values.
    R = read_ratings(test_set)
    #R = [[5, 4, 0, 0, 1],
    #     [4, 2, 1, 0, 3],
    #     [0, 3, 2, 4, 2],
    #     [4, 0, 2, 4, 0],
    #     [4, 3, 0, 0, 0]]

    R = numpy.array(R)

    P = numpy.random.rand(len(R), K)
    Q = numpy.random.rand(len(R[0]), K)

    # Run algorithm on matrices.
    nP, nQ = matrix_factorization(P, Q, R, K=K, steps=steps, alpha=alpha, beta=beta, debug=debug)

    # Calculate recommendation and write it to recommendation file.
    # calculate_recommendations(nP, nQ, R, test_set)

    # Calculate and write all matrices to files for inspection and saving purposes.
    """
    if not debug:
        R_final = numpy.dot(P, Q.T)
        write_numpy_matrix(R, "R_original.data", test_set)
        write_numpy_matrix(R_final, "ratings.data", test_set)
        write_factor_matrix(nP, "P.data", test_set)
        write_factor_matrix(nQ, "Q.data", test_set)
        bound_results(R_final, test_set)
    """


file = open("Log.txt", "w").close()
do_factorization("Test1", K=2, steps=5000, alpha=0.03, beta=0.02, debug=True)
#do_factorization("Test2")
#do_factorization("Test3")
#do_factorization("Test4")
#do_factorization("Test5")
