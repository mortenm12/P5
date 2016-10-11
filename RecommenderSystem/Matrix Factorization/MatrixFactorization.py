from MatrixGeneration import *
import time
import numpy


def write_numpy_matrix(m, file):
    result = open(file, "w")
    for i in range(0, len(m)):
        for j in range(0, len(m[i])):
            result.write("%.2f " % m[i][j])
        result.write('\n')

    if not result.closed:
        result.close()


def matrix_factorization(R, P, Q, K, steps=100, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in range(0, steps):
        print(step, end=' ')
        print(time.asctime(time.localtime(time.time())))
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
                    for k in range(0, K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P, Q)
        e = 0
        for i in range(0, len(R)):
            for j in range(0, len(R[i])):
                if R[i][j] > 0:
                    e += pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(0, K):
                        e += (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        if e < 0.001:
            break

    return P, Q.T


R = generate_matrix(read_users(), read_movies())
N = len(R)
M = len(R[0])
K = 42

P = numpy.random.rand(N, K)
Q = numpy.random.rand(M, K)

nP, nQ = matrix_factorization(R, P, Q, K)
nR = numpy.dot(nP, nQ.T)
write_numpy_matrix(R, "result")
write_numpy_matrix(nR, "R_matrix")
write_numpy_matrix(nP, "P_matrix")
write_numpy_matrix(nQ, "Q_matrix")

recommendation_file = open("Recommendations.data", "w")

a = 0
most_accurate_product = 0
for i in range(0, len(nP)):
    for j in range(0, len(nQ)):
        result = numpy.dot(nP[i, :], nQ[j, :])
        if result > most_accurate_product:
            most_accurate_product = result
            a = j
    recommendation_file.write("User: " + str(i) + ", Recommended movie: " + str(a) + "\n")
