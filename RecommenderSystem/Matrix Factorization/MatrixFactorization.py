"""
Implementation of Matrix Factorization by Rasmus Jensen
"""
# Imports
from MatrixGeneration import *
import time
import numpy


# Algorithm to write a matrix to a file
def write_numpy_matrix(m, file):
    result = open(file, "w")
    for i in range(0, len(m)):
        for j in range(0, len(m[i])):
            result.write("%.2f " % m[i][j])
        result.write('\n')

    if not result.closed:
        result.close()


def calculate_recommendations(nP, nQ):
    recommendation_file = open("Recommendations.data", "w")

    # For each user vector find the most similar item vector by calculating the dot products.
    a = 0
    most_accurate_product = 0
    for i in range(0, len(nP)):
        for j in range(0, len(nQ)):
            result = numpy.dot(nP[i, :], nQ[j, :])
            if result > most_accurate_product:
                most_accurate_product = result
                a = j
        recommendation_file.write("User: " + str(i) + ", Recommended movie: " + str(a) + "\n")

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
def matrix_factorization(R, P, Q, K, steps=100, alpha=0.0002, beta=0.02):
    # Transposes the Q matrix, so the dot product of P and Q can be taken.
    Q = Q.T

    # The main algorithm.
    for step in range(0, steps):

        # Printing progress.
        print(step, end=' ')
        print(time.asctime(time.localtime(time.time())))

        # Iterates over the R matrix, only doing something if a rating has been given
        for i in range(len(R)):
            for j in range(len(R[i])):

                # If a rating has been given, calculate the error by getting the dot product of the user and item
                # vectors in the latent vector spaces corresponding to the rating
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])

                    # Calculate the new entries in the latent factor spaces.
                    for k in range(0, K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        # Calculate the average error of PxQ from R.
        e = 0
        for i in range(0, len(R)):
            for j in range(0, len(R[i])):
                if R[i][j] > 0:
                    e += pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(0, K):
                        e += (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))

        # If the error is arbitrarily small, stop execution to avoid useless running time.
        if e < 0.001:
            break

    return P, Q.T

# Initialize matrices and values.
R = generate_matrix(read_users(), read_movies())
K = 42
P = numpy.random.rand(len(R), K)
Q = numpy.random.rand(len(R[0]), K)

# Run algorithm on matrices.
nP, nQ = matrix_factorization(R, P, Q, K)

# Calculate recommendation and write it to recommendation file.
calculate_recommendations(nP, nQ)

# Calculate and write all matrices to files for inspection and saving purposes.
nR = numpy.dot(nP, nQ.T)
write_numpy_matrix(R, "result")
write_numpy_matrix(nR, "R_matrix")
write_numpy_matrix(nP, "P_matrix")
write_numpy_matrix(nQ, "Q_matrix")
