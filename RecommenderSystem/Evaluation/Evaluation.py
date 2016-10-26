import time
import numpy as np
import numpy.ma as npm
from DataAPI import *

'''
DISCRIPTION:
Evaluates a test- and a base-array into a single value

INPUT:
arrTest: The test-array.
arrBase: The base-array.
func_map(float, float -> float): The function to evaluate each rating.
func_fold(list[(float)] -> float): The function to map all ratings into the resulting value.

OUTPUT:
Returns the resulting value.
'''

def rating_evaluation(arrTest, arrBase, func_map, func_fold):
    #Mask out invalid ratings
    arrBase = npm.masked_equal(arrBase, 0)
    #Map into combined array
    vec_map = np.vectorize(func_map)
    arrResult = vec_map(arrTest, arrBase)
    #Fold into the resulting value
    return func_fold(arrResult)

ratingAlgorithms = ["Matrix Factorization", "NearestNeighbour"]
numTests = 1

evaluationAlgorithms = {}

#Normalized Root Mean Square Error
evaluationAlgorithms["NRMSE"] = (lambda a, b: (a - b) ** 2, lambda arr: np.mean(arr) ** 0.5)
#Normalized Mean Absolute Error
evaluationAlgorithms["NMAE"] = (lambda a, b: abs(a - b), lambda arr: np.mean(arr))
#Per-User Normalized Mean Absolute Error
evaluationAlgorithms["UNMAE"] = (lambda a, b: abs(a - b), lambda arr: np.mean(np.mean(arr,0)))
#Per-Movie Normalized Mean Absolute Error
evaluationAlgorithms["MNMAE"] = (lambda a, b: abs(a - b), lambda arr: np.mean(np.mean(arr,1)))


dictArrs = {}

#Read in base arrays
dictArrs["Base"] = []
for i in range(1, numTests + 1):
    dictArrs["Base"].append(np.array(read_base_ratings("Test" + str(i)), np.float))

#Read in recommendation arrays
for algo in ratingAlgorithms:
    dictArrs[algo] = []
    for i in range(1, numTests + 1):
        dictArrs[algo].append(np.array(read_recommendation_matrix(algo, "Test" + str(i)), np.float))

#Evaluate algorithms
dictResults = {}

for rAlgo in ratingAlgorithms:
    dictResults[rAlgo] = []
    for i in range(numTests):
        results = {}
        for eAlgo in evaluationAlgorithms.keys():
            results[eAlgo] = rating_evaluation(dictArrs[rAlgo][i], dictArrs["Base"][i], *evaluationAlgorithms[eAlgo])
        dictResults[rAlgo].append(results)

def FormatResults(strDescription):
    output = ""
    output += time.ctime()
    output += "\nDescription: "
    output += strDescription
    output += "\n"
    for rAlgo in ratingAlgorithms:
        output += "\n"
        output += rAlgo
        output += "\n---\n"
        for eAlgo in evaluationAlgorithms.keys():
            output += eAlgo
            output += ":\n"
            for i in range(numTests):
                output += str(i + 1)
                output += ". "
                output += str(dictResults[rAlgo][i][eAlgo])
                output += "\n"
        output += "---\n"
    output += "\n"
    return output

def LogResults():
    logfile = open("EvaluationLog.txt", "a")
    logfile.write(FormatResults(input("Evaluation Description:\n")))
    if not logfile.closed:
        logfile.close()

LogResults()