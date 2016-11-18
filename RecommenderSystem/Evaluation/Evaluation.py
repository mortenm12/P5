import time
import numpy as np
import numpy.ma as npm
import functools as ft
from DataAPI import *

class EvaluationAlgorithm:

    AE = lambda a, b: abs(a - b)
    SE = lambda a, b: (a - b) ** 2

    # All our algorithms are prefabs with a functionGenerator, a boolean value indicating weather they are testdependant or not and optional parameters.

    prefabs = {}

    prefabs["MAE"] = ("MAE", lambda args: (EvaluationAlgorithm.AE, lambda arr: np.mean(arr)), False, None)

    prefabs["RMSE"] = ("RMSE", lambda args: (EvaluationAlgorithm.SE, lambda arr: np.mean(arr) ** 0.5), False, None)

    #testArray gets preprocessed into user-/movieTests using partial. This makes the conversion happen only once and not every evaluation.
    prefabs["MUIWAE"] = ("MUIWAE", lambda testArray, args: ft.partial(lambda userRatings: (EvaluationAlgorithm.AE, lambda arr: npm.mean(arr * (userRatings / npm.mean(userRatings * np.ones_like(arr))))),
                                           userRatings = np.atleast_2d(np.reciprocal(np.sum(testArray, 0) + 1))), True, None)

    prefabs["MMIWAE"] = ("MMIWAE", lambda testArray, args: ft.partial(lambda movieRatings: (EvaluationAlgorithm.AE, lambda arr: npm.mean(arr * (movieRatings / npm.mean(movieRatings * np.ones_like(arr))))),
                                           movieRatings = np.atleast_2d(np.reciprocal(np.sum(testArray, 1) + 1)).T), True, None)

    prefabs["RMUIWSE"] = ("RMUIWSE", lambda testArray, args: ft.partial(lambda userRatings: (EvaluationAlgorithm.SE, lambda arr: npm.mean(arr * (userRatings / npm.mean(userRatings * np.ones_like(arr)))) ** 0.5),
                                           userRatings = np.atleast_2d(np.reciprocal(np.sum(testArray, 0) + 1))), True, None)

    prefabs["RMMIWSE"] = ("RMMIWSE", lambda testArray, args: ft.partial(lambda movieRatings: (EvaluationAlgorithm.SE, lambda arr: npm.mean(arr * (movieRatings / npm.mean(movieRatings * np.ones_like(arr)))) ** 0.5),
                                           movieRatings = np.atleast_2d(np.reciprocal(np.sum(testArray, 1) + 1)).T), True, None)

    prefabs["UISMAE"] = ("UISMAE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.AE, lambda arr: np.mean(npm.masked_where(arrayMask, arr))),
                                            arrayMask = np.resize(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(testArray, 0), *args))), testArray.shape)), True)

    prefabs["MISMAE"] = ("MISMAE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.AE, lambda arr: np.mean(npm.masked_where(arrayMask, arr))),
                                            arrayMask=np.resize(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(testArray, 1), *args))).T, testArray.shape)), True)

    prefabs["UISRMSE"] = ("UISRMSE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.SE, lambda arr: np.mean(npm.masked_where(arrayMask, arr)) ** 0.5),
                                            arrayMask = np.resize(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(testArray, 0), *args))), testArray.shape)), True)

    prefabs["MISRMSE"] = ("MISRMSE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.SE, lambda arr: np.mean(npm.masked_where(arrayMask, arr)) ** 0.5),
                                            arrayMask=np.resize(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(testArray, 1), *args))).T, testArray.shape)), True)

    def __init__(self, mappingFunction, foldingFunction, name):
        self.mappingFunction = mappingFunction
        self.foldingFunction = foldingFunction
        self.name = name

    def __call__(self, predictedArray, baseArray):
        # Mask out invalid ratings
        baseArray = npm.masked_equal(baseArray, 0)
        # Map into combined array
        resultArray = self.mappingFunction(predictedArray, baseArray)
        # Fold into the resulting value
        return self.foldingFunction(resultArray)

class RatingEvaluator:

    defaultAlgorithms = [
        EvaluationAlgorithm.prefabs["MAE"],
        EvaluationAlgorithm.prefabs["RMSE"],
        EvaluationAlgorithm.prefabs["MUIWAE"],
        EvaluationAlgorithm.prefabs["MMIWAE"],
        EvaluationAlgorithm.prefabs["RMUIWSE"],
        EvaluationAlgorithm.prefabs["RMMIWSE"]
    ]

    def __init__(self, predictionAlgorithms, testIndexes, evaluationAlgorithms = defaultAlgorithms):
        self.arrays = {}
        self.results = {}
        self.evaluationAlgorithms = {}
        self.evaluationAlgorithmByTest = {}
        self.testIndexes = testIndexes
        self.predictionAlgorithms = []
        self.ReadBaseArrays()
        for algo in predictionAlgorithms:
            self.ReadRecommendationArrays(algo)
        for algo in filter(lambda algo: algo[2] == False, evaluationAlgorithms):
            self.evaluationAlgorithms[algo[0]] = EvaluationAlgorithm(*algo[1](algo[3]), algo[0])
        for algo in filter(lambda algo: algo[2] == True, evaluationAlgorithms):
            self.evaluationAlgorithmByTest[algo[0]] = {}
        for i in testIndexes:
            testArray = np.sign(np.array(read_ratings("Test" + str(i)), np.float))
            for algo in filter(lambda item: item[2] == True, evaluationAlgorithms):
                self.evaluationAlgorithmByTest[algo[0]][i] = EvaluationAlgorithm(*algo[1](testArray, algo[3])(), algo[0])

    '''
    rating_evaluation:
    Evaluates a test- and a base-array into a single value

    INPUT:
    arrTest: The test-array.
    arrBase: The base-array.
    func_map(float, float -> float): The function to evaluate each rating.
    func_fold(arr(float)] -> float): The function to map all ratings into the resulting value.

    OUTPUT:
    Returns the resulting value.
    '''

    def ReadBaseArrays(self):
        self.arrays["Base"] = {}
        for i in self.testIndexes:
            self.arrays["Base"][i] = np.array(read_base_ratings("Test" + str(i)), np.float)

    def ReadRecommendationArrays(self, algorithmName):
        self.arrays[algorithmName] = {}
        for i in self.testIndexes:
            self.arrays[algorithmName][i] = np.array(read_recommendation_matrix(algorithmName, "Test" + str(i)), np.float)
        self.predictionAlgorithms.append(algorithmName)

    def EvaluateAlgorithm(self, algorithmName):
        self.results[algorithmName] = {}
        for i in self.testIndexes:
            results = {}
            for eAlgo in self.evaluationAlgorithms.values():
                results[eAlgo.name] = eAlgo(self.arrays[algorithmName][i], self.arrays["Base"][i])

            for eAlgo in self.evaluationAlgorithmByTest.values():
                results[eAlgo[i].name] = eAlgo[i](self.arrays[algorithmName][i], self.arrays["Base"][i])
            self.results[algorithmName][i] = results

    def EvaluateAllAlgorithms(self):
        for algo in self.predictionAlgorithms:
            self.EvaluateAlgorithm(algo)

    def FormatResults(self):
        output = ""
        for rAlgo in sorted(self.results.keys()):
            output += rAlgo
            output += "\n---\n"
            for eAlgo in sorted(list(self.evaluationAlgorithms.keys()) + list(self.evaluationAlgorithmByTest.keys())):
                output += eAlgo
                output += ":\n"
                for i in self.testIndexes:
                    output += str(i)
                    output += ". "
                    output += str(self.results[rAlgo][i][eAlgo])
                    output += "\n"
            output += "---\n\n"
        return output

    def LogResults(self, description):
        output = ""
        output += time.ctime()
        output += "\nDescription: "
        output += description
        output += "\n\n"
        output += self.FormatResults()
        logfile = open("EvaluationLog.txt", "a")
        logfile.write(output)
        if not logfile.closed:
            logfile.close()

evaluator = RatingEvaluator(["Matrix Factorization"], [1])
evaluator.EvaluateAllAlgorithms()
evaluator.LogResults(input("Evaluation Description:\n"))