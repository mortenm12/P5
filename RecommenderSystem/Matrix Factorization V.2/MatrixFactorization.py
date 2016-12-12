"""
Implementation of biased Matrix Factorization
"""
# Imports
from DataAPI import *
import time
import numpy
import Evaluation
import copy


# The factorization algorithm.
# The point of this algorithm is to stepwise approximate P and Q so that PxQ approximates R.
# Takes 4 parameters:
#   R, the N x M user/item rating matrix.
#   P, the N x K user latent factor space matrix, initially random.
#   Q, the M x K item latent factor space matrix, initially random.
#   K, the amount of latent factors.
#
# And has 3 other default parameters:
#   steps, the amount of iterations the algorithm will run for.
#   alpha, the approximation variable, defining how fast the algorithm converges.
#   beta, the normalization variable, defining how much to avoid overfitting.

def matrix_factorization(P, Q, R, K, steps=5000, alpha=0.07, beta=0.02, printing=True):
    # Transposes the Q matrix, so the dot product of P and Q can be taken.
    Q = Q.T

    prev_error = 0
    time_start = time.time()

    # The main algorithm.
    for step in range(0, steps):

        # Printing progress.
        if printing:
            print("{:4d}".format(step), end=' ')
            print(time.strftime("%H:%M:%S", time.localtime()), end='')

        # Iterates over the R matrix, only doing something if a rating has been given.
        for i in range(len(R)):
            for j in range(len(R[i])):

                # If a rating has been given, calculate the error by getting the dot product of the user and item
                # vectors in the latent vector spaces corresponding to the rating.
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])

                    # Calculate the new entries in the latent factor spaces.
                    for k in range(0, K):
                        Pik = P[i][k]
                        Qkj = Q[k][j]
                        P[i][k] = Pik + (alpha * ((2 * eij * Qkj) - (beta * Pik)))
                        Q[k][j] = Qkj + (alpha * ((2 * eij * Pik) - (beta * Qkj)))

        error = 0
        entries = 0

        # Calculate the average error of PxQ from R.
        for i in range(0, len(R)):
            for j in range(0, len(R[i])):
                if R[i][j] > 0:
                    error += pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    entries += 1
                    for k in range(0, K):
                        error += (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        average_error = error / entries
        if printing:
            print(" Error = " + "{:.2f}".format(float(error)) + " Average Error = " + "{:.2f}".format(float(average_error)))

        # If the change in error is arbitrarily small, stop execution to avoid useless running time.
        if prev_error != 0 and prev_error - error < 0.1:
            break

        prev_error = error

    if printing:
        print("Elapsed time: " + time.strftime("%H:%M:%S", time.localtime(time.time() - time_start)))

    return P, Q.T


# Calculates the biases of all users and movies, as well as the global average rating.
def calculate_biases(R):
    # Calculates the user biases.
    user_averages = []
    for i in range(len(R)):
        total = 0
        count = 0
        for j in range(len(R[0])):
            if R[i][j] > 0:
                total += R[i][j]
                count += 1

        if not count == 0:
            user_averages.insert(i, total / count)
        else:
            user_averages.insert(i, 0.0)

    # Calculate the movie biases.
    movie_averages = []
    for j in range(len(R[0])):
        total = 0
        count = 0
        for i in range(len(R)):
            if R[i][j] > 0:
                total += R[i][j]
                count += 1

        if not count == 0:
            movie_averages.insert(i, total / count)
        else:
            movie_averages.insert(i, 0.0)

    # Calculate the global average rating.
    total = 0
    count = 0
    for i in range(len(R)):
        for j in range(len(R[0])):
            if R[i][j] > 0:
                total += R[i][j]
                count += 1
    if not count == 0:
        global_average = total / count
    else:
        global_average = 0

    return global_average, movie_averages, user_averages


# Adjusts the input matrix based on user and movie biases.
def adjust_for_bias(R, global_average, movie_averages, user_averages):
    adjusted_R = copy.deepcopy(R)
    for i in range(len(R)):
        for j in range(len(R[0])):
            if adjusted_R[i][j] > 0:
                adjusted_R[i][j] = R[i][j] - user_averages[i] - movie_averages[j] + global_average

    return adjusted_R


# Reverses the adjustments made on the input matrix for the output matrix.
def readjust_for_bias(R, global_average, movie_averages, user_averages):
    readjusted_R = copy.deepcopy(R)
    for i in range(len(R)):
        for j in range(len(R[0])):
            readjusted_R[i][j] = R[i][j] + user_averages[i] + movie_averages[j] - global_average

    return readjusted_R


# Run the matrix factorization algorithm with all setup.
def do_biased_matrix_factorization(test_set, K=20, steps=1500, alpha=0.03, beta=0.02):
    # Initialize matrices and values.
    R = read_ratings(test_set)
    P = numpy.random.rand(len(R), K)
    Q = numpy.random.rand(len(R[0]), K)
    global_average, movie_averages, user_averages = calculate_biases(R)
    R = adjust_for_bias(R, global_average, movie_averages, user_averages)
    R = numpy.array(R)

    # Run algorithm on matrices.
    new_P, new_Q = matrix_factorization(P, Q, R, K=K, steps=steps, alpha=alpha, beta=beta)

    # Calculate recommendation matrix.
    recommendations = numpy.dot(P, Q.T)

    # Write all matrices to files for inspection and saving purposes.
    write_matrix(R, "R_original.data", test_set)
    write_matrix(readjust_for_bias(recommendations, global_average, movie_averages, user_averages), "ratings.data", test_set)
    write_matrix(recommendations, "unadjusted_ratings.data", test_set)
    write_feature_matrix(new_P, "P.data", test_set)
    write_feature_matrix(new_Q, "Q.data", test_set)


# Algorithm to write a result matrix to a file.
def write_matrix(m, file_name, test_set):
    file = open("Output/" + test_set + "/" + file_name, "w")
    file.write(" ID , " + ", ".join(str(x) for x in range(1, len(m[0]) + 1)) + "\n")
    for i in range(0, len(m)):
        file.write("{:>4d}, ".format(i + 1))
        file.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        file.write("\n")

    if not file.closed:
        file.close()


# Algorithm to write a feature matrix to a file.
def write_feature_matrix(m, file_name, test_set):
    file = open("Output/" + test_set + "/" + file_name, "w")
    for i in range(0, len(m)):
        file.write("{:>4d}, ".format(i + 1))
        file.write(", ".join(["{: .2f}".format(x) for x in m[i]]))
        file.write("\n")

    if not file.closed:
        file.close()


# Bound the result matrix so no value is above 5 or below 1.
def bound_results(R, test_set):
    bounded_R = copy.deepcopy(R)
    for i in range(len(bounded_R)):
        for j in range(len(bounded_R[0])):
            if bounded_R[i][j] > 5:
                bounded_R[i][j] = 5
            elif bounded_R[i][j] < 1:
                bounded_R[i][j] = 1

    write_matrix(bounded_R, "bounded_ratings.data", test_set)


# Calculate k recommendations for the user.
def calculate_k_recommendations(user, k, test_set):
    # Read matrices.
    R = read_ratings(test_set)
    P, Q = read_factor_matrices(test_set)
    P = numpy.array(P)
    Q = numpy.array(Q)

    # Calculate averages.
    global_average, movie_averages, user_averages = calculate_biases(R)

    # Calculate the ratings for all user/item pairs, and return the k highest ones.
    recommendations = []
    for i in range(len(Q)):
        if R[user - 1][i] == 0.0:
            recommendations.append([i + 1, numpy.dot(P[user - 1, :], Q[i, :]) - global_average + movie_averages[i] + user_averages[user - 1]])

    return sorted(recommendations, key=lambda x: x[1], reverse=True)[:k]

# Dialogue to determine what test sets will be run.
#print("Do you want to run for all test sets? (Y/N)")
#s = input()
#if s == 'Y':
#    tests_to_run = [1, 2, 3, 4, 5]
#elif s == 'N':
#    print("What test set will you run it for?")
#    s = input
#    tests_to_run = [int(s)]
#else:
#    tests_to_run = [1]
#
# Run the algorithms on all test sets.
#for i in tests_to_run:
#    do_biased_matrix_factorization("Test" + str(i), K=20, steps=1000, alpha=0.03, beta=0.02)

# Automatically run evaluation on the output of the algorithm.
#evaluator = Evaluation.RatingEvaluator(["Matrix Factorization V.2"], tests_to_run)
#evaluator.evaluate_all_algorithms()
#evaluator.log_results("Evaluation Description: ")

