import time
import numpy as np
import numpy.ma as npm
import functools as ft
from DataAPI import *

class EvaluationAlgorithmPrefab:

    def __init__(self, name, functionGenerator, testDependent):
        self.name = name
        self.functionGenerator = functionGenerator
        self.testDependent = testDependent

class EvaluationAlgorithm:

    AE = lambda a, b: abs(a - b)
    SE = lambda a, b: (a - b) ** 2

    # All our algorithms are prefabs with a functionGenerator, a boolean value indicating weather they are testdependant or not and optional parameters.

    prefabs = {}

    #Mean Absolute Error
    prefabs["MAE"] = EvaluationAlgorithmPrefab("MAE", lambda args: (EvaluationAlgorithm.AE, lambda arr: np.mean(arr)), False)

    #Root Mean Square Error
    prefabs["RMSE"] = EvaluationAlgorithmPrefab("RMSE", lambda args: (EvaluationAlgorithm.SE, lambda arr: np.mean(arr) ** 0.5), False)

    #Partial allows us to preprocess part of the generated function, so that it happens only once and not every evaluation.

    '''
    In the weighted measures, a weight array is multiplied with the error-array
    The weight array is calculated as follows:
    np.sign is used on testArray to make an array that contains a 1 if a rating exists and a 0 otherwise.
    The sum across an axis in this array finds the amount of ratings of each user/movie which is used to make the initial weight array.
    This is pre-processed using functools.partial, since this part of the calculation is independent of the error-array.
    A copy of the error-array with entries replaced with 1s are then multiplied with the weight array.
    This is needed to account for the invalid data, which makes some weights used more than others.
    The average over this resulting array is then the average of the weights.
    The initial weight array is then divided by this average resulting in the final weight array.
    '''

    #Mean User-Ratings Weighted Absolute Error
    prefabs["MURWAE"] = EvaluationAlgorithmPrefab("MUIWAE", lambda testArray, args: ft.partial(lambda weights: (EvaluationAlgorithm.AE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr))))),
                                                                      weights = np.atleast_2d(np.reciprocal(np.sum(np.sign(testArray), 0) + 1))), True)

    #Mean Movie-Ratings Weighted Absolute Error
    prefabs["MMRWAE"] = EvaluationAlgorithmPrefab("MMIWAE", lambda testArray, args: ft.partial(lambda weights: (EvaluationAlgorithm.AE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr))))),
                                                                      weights = np.atleast_2d(np.reciprocal(np.sum(np.sign(testArray), 1) + 1)).T), True)

    #Root Mean User-Ratings Weighted Square Error
    prefabs["RMURWSE"] = EvaluationAlgorithmPrefab("RMUIWSE", lambda testArray, args: ft.partial(lambda weights: (EvaluationAlgorithm.SE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr)))) ** 0.5),
                                                                        weights = np.atleast_2d(np.reciprocal(np.sum(np.sign(testArray), 0) + 1))), True)

    #Root Mean Movie-Ratings Weighted Square Error
    prefabs["RMMRWSE"] = EvaluationAlgorithmPrefab("RMMIWSE", lambda testArray, args: ft.partial(lambda weights: (EvaluationAlgorithm.SE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr)))) ** 0.5),
                                                                        weights = np.atleast_2d(np.reciprocal(np.sum(np.sign(testArray), 1) + 1)).T), True)

    '''
    In the sliced measures, a mask is applied to the error-array to ignore the ratings of users/movies with an amount
    of ratings outside a given boundary.
    This mask is calculated as follows:
    np.sign is used on testArray to make an array that contains a 1 if a rating exists and a 0 otherwise.
    The sum across an axis in this array finds the amount of ratings of each user/movie.
    This array is then masked out where the amount of ratings is outside the given boundaries.
    The mask of the array is pre-processed using functools.partial, since this part of the calculation is independent of the error-array.
    The mask is then changed in size and applied to the error-array.
    Since the indexes of both arrays correlates with the same user/movie, applying this mask to the error-array
    makes it ignore the ratings of these users/movies.
    '''

    #User-Ratings Sliced Mean Absolute Error
    prefabs["URSMAE"] = EvaluationAlgorithmPrefab("UISMAE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.AE, lambda arr: np.mean(npm.masked_where(arrayMask, arr))),
                                            arrayMask = np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(testArray), 0), *args))), testArray.shape)), True)

    #Movie-Ratings Sliced Mean Absolute Error
    prefabs["MRSMAE"] = EvaluationAlgorithmPrefab("MISMAE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.AE, lambda arr: np.mean(npm.masked_where(arrayMask, arr))),
                                            arrayMask = np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(testArray), 1), *args))).T, testArray.shape)), True)

    #User-Ratings Sliced Root Mean Square Error
    prefabs["URSRMSE"] = EvaluationAlgorithmPrefab("UISRMSE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.SE, lambda arr: np.mean(npm.masked_where(arrayMask, arr)) ** 0.5),
                                            arrayMask = np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(testArray), 0), *args))), testArray.shape)), True)

    #Movie-Ratings Sliced Root Mean Square Error
    prefabs["MRSRMSE"] = EvaluationAlgorithmPrefab("MISRMSE", lambda testArray, args: ft.partial(lambda arrayMask: (EvaluationAlgorithm.SE, lambda arr: np.mean(npm.masked_where(arrayMask, arr)) ** 0.5),
                                            arrayMask = np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(testArray), 1), *args))).T, testArray.shape)), True)

    '''
    PARAMETERS:
    mappingFunction and foldingFunction:
    Functions used to map and fold during evaluation. These are usually made from a prefab functionGenerator
    name: Name of the algorithm
    '''
    def __init__(self, mappingFunction, foldingFunction, name):
        self.mappingFunction = mappingFunction
        self.foldingFunction = foldingFunction
        self.name = name

    '''
    Calling an EvaluationAlgorithm:
    Evaluates a prediction- and a base-array into an error measure

    INPUT:
    predictionArray: The prediciton-array.
    baseArray: The base-array.

    OUTPUT:
    Returns the resulting error measure.
    '''
    def __call__(self, predictionArray, baseArray):
        # Mask out all invalid ratings
        baseArray = npm.masked_equal(baseArray, 0)
        # Map into error-array
        resultArray = self.mappingFunction(predictionArray, baseArray)
        # Fold error-array into the resulting measure
        return self.foldingFunction(resultArray)

class RatingEvaluator:

    #All parameterless measures are evaluated as default
    defaultAlgorithms = [
        (EvaluationAlgorithm.prefabs["MAE"], None),
        (EvaluationAlgorithm.prefabs["RMSE"], None),
        (EvaluationAlgorithm.prefabs["MURWAE"], None),
        (EvaluationAlgorithm.prefabs["MMRWAE"], None),
        (EvaluationAlgorithm.prefabs["RMURWSE"], None),
        (EvaluationAlgorithm.prefabs["RMMRWSE"], None)
    ]

    @staticmethod
    def formatName(name, args):
        if args == None:
            return name
        else:
            return name + str(args)

    '''
    PARAMETERS:
    predictionAlgorithms: List of names of predictionAlgorithms to evaluate
    testIndexes: List of test-indexes for the tests used
    evaluationAlgorithms (Optional): List of evaluation-algorithm prefabs to evaluate with.
    '''
    def __init__(self, predictionAlgorithms, testIndexes, evaluationAlgorithms = defaultAlgorithms):
        self.testIndexes = testIndexes

        #Dictionary for storing arrays
        self.arrays = {}
        #Dictionary for storing results
        self.results = {}

        #Prepare base arrays
        self.ReadBaseArrays()

        #Prepare prediction arrays
        self.predictionAlgorithmNames = predictionAlgorithms
        for algo in predictionAlgorithms:
            self.ReadPredictionArrays(algo)
        '''
        Test-dependent and test-independent evaluation-algorithms are prepared separately, since we only want to
        prepare the same test-independent evaluation-algorithm once.
        '''
        #Prepare test-independent evaluation-algorithms
        self.evaluationAlgorithms = {}
        #Only select the prefabs marked as test-independent
        for algo in filter(lambda algo: algo[0].testDependent == False, evaluationAlgorithms):
            #Make an evaluation-algorithm from the prefab
            name = RatingEvaluator.formatName(algo[0].name, algo[1])
            mappingFunction, foldingFunction = algo[0].functionGenerator(algo[1])
            self.evaluationAlgorithms[name] = EvaluationAlgorithm(mappingFunction, foldingFunction, name)

        #Prepare test-dependent evaluation-algorithms
        self.evaluationAlgorithmByTest = {}
        #Only select the prefabs marked as test-dependent
        for algo in filter(lambda algo: algo[0].testDependent == True, evaluationAlgorithms):
            name = RatingEvaluator.formatName(algo[0].name, algo[1])
            self.evaluationAlgorithmByTest[name] = {}
        for i in testIndexes:
            testArray = np.array(read_ratings("Test" + str(i)), np.float)
            #Again, only select the prefabs marked as test-dependent
            for algo in filter(lambda algo: algo[0].testDependent == True, evaluationAlgorithms):
                # Make an evaluation-algorithm from the prefab. The parameterless call performs the pre-processing.
                mappingFunction, foldingFunction = algo[0].functionGenerator(testArray, algo[1])()
                name = RatingEvaluator.formatName(algo[0].name, algo[1])
                self.evaluationAlgorithmByTest[name][i] = EvaluationAlgorithm(mappingFunction, foldingFunction, name)

    def ReadBaseArrays(self):
        self.arrays["Base"] = {}
        for i in self.testIndexes:
            self.arrays["Base"][i] = np.array(read_base_ratings("Test" + str(i)), np.float)

    def ReadPredictionArrays(self, algorithmName):
        self.arrays[algorithmName] = {}
        for i in self.testIndexes:
            self.arrays[algorithmName][i] = np.array(read_recommendation_matrix(algorithmName, "Test" + str(i)), np.float)

    def EvaluateAlgorithm(self, algorithmName):
        self.results[algorithmName] = {}
        for i in self.testIndexes:
            results = {}
            '''
            Test-dependent and test-independent evaluation-algorithms are used separately, since we only want to
            evaluate with the same test-independent evaluation-algorithm once.
            '''
            for eAlgo in self.evaluationAlgorithms.values():
                #Call the evaluation-algortihm with the prediction- and the base-array, and store the result.
                results[eAlgo.name] = eAlgo(self.arrays[algorithmName][i], self.arrays["Base"][i])

            for eAlgo in self.evaluationAlgorithmByTest.values():
                #Call the evaluation-algortihm with the prediction- and the base-array, and store the result.
                results[eAlgo[i].name] = eAlgo[i](self.arrays[algorithmName][i], self.arrays["Base"][i])
            self.results[algorithmName][i] = results

    def EvaluateAllAlgorithms(self):
        for algo in self.predictionAlgorithmNames:
            self.EvaluateAlgorithm(algo)

    #Returns a formatted string of the results
    def FormatResults(self):
        output = ""
        for rAlgo in self.predictionAlgorithmNames:
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

    #Appends the results in a formatted way to a logfile
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

#evaluator = RatingEvaluator(["Matrix Factorization"], [1])
#evaluator.EvaluateAllAlgorithms()
#evaluator.LogResults(input("Evaluation Description:\n"))