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
for i in range(1,2):
    dictArrs["Base"].append(np.array(read_base_ratings("Test" + str(i))))

#Read in recommendation arrays
for algo in ratingAlgorithms:
    dictArrs[algo] = []
    for i in range(1,2):
        dictArrs[algo].append(np.array(read_recommendation_matrix(algo, "Test" + str(i))))

#Evaluate algorithms
dictResults = {}

for rAlgo in ratingAlgorithms:
    dictResults[rAlgo] = []
    for i in range(1):
        results = {}
        for eAlgo in evaluationAlgorithms.keys():
            results[eAlgo] = rating_evaluation(dictArrs[rAlgo][i], dictArrs["Base"][i], *evaluationAlgorithms[eAlgo])
        dictResults[rAlgo].append(results)

print(dictResults)