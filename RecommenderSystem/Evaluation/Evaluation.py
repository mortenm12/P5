import numpy as np
import numpy.ma as npm
from DataAPI import *

#Normalized Root Mean Square Error
NRMSE = (lambda a, b: (a - b) ** 2, lambda i: sum(i) ** 0.5 / len(i))
#Normalized Mean Absolute Error
NMAE = (lambda a, b: abs(a - b), lambda i: sum(i) / len(i))

#Read in base arrays
arrsBase = []
for i in range(5):
    arrsBase.append(np.array(read_base_ratings("Test" + str(i + 1))))

'''
DISCRIPTION:
Evaluates a test- and a base-array into a single value

INPUT:
arrTest: The test-array.
arrBase: The base-array.
func_map(float, float, userid, movieid -> float): The function to evaluate each rating.
func_fold(list[float] -> float): The function to map all ratings into the resulting value.

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
    return func_fold(arrResult.compressed())