from MatrixFactorization import calculate_result_matrix
import numpy

R_file = open("ratings", "r")
R = []
i = 0
for line in R_file:
    R.append([])
    vals = line.split()
    for val in vals:
        R[i].append(float(val))
    i += 1
if not R_file.closed:
    R_file.close()
R = numpy.array(R)

P_file = open("P_matrix", "r")
P = []
i = 0
for line in P_file:
    P.append([])
    vals = line.split()
    for val in vals:
        P[i].append(float(val))
    i += 1
if not P_file.closed:
    P_file.close()
P = numpy.array(P)

Q_file = open("Q_matrix", "r")
Q = []
i = 0
for line in Q_file:
    Q.append([])
    vals = line.split()
    for val in vals:
        Q[i].append(float(val))
    i += 1
if not Q_file.closed:
    Q_file.close()
Q = numpy.array(Q)

calculate_result_matrix(P, Q, R)
