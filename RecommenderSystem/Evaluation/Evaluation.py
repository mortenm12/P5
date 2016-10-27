import time
import numpy as np
import numpy.ma as npm
from DataAPI import *

class RatingEvaluator:

    evaluationAlgorithms = {}

    # Normalized Root Mean Square Error
    evaluationAlgorithms["NRMSE"] = (lambda a, b: (a - b) ** 2, lambda arr: np.mean(arr) ** 0.5)
    # Normalized Mean Absolute Error
    evaluationAlgorithms["NMAE"] = (lambda a, b: abs(a - b), lambda arr: np.mean(arr))
    # Per-User Normalized Mean Absolute Error
    evaluationAlgorithms["UNMAE"] = (lambda a, b: abs(a - b), lambda arr: np.mean(np.mean(arr, 0)))
    # Per-Movie Normalized Mean Absolute Error
    evaluationAlgorithms["MNMAE"] = (lambda a, b: abs(a - b), lambda arr: np.mean(np.mean(arr, 1)))

    def __init__(self, predAlgorithms, numTests):
        self.dictArrs = {}
        self.dictResults = {}
        self.numTests = numTests
        self.predictionAlgorithms = []
        self.ReadBaseArrays()
        for algo in predAlgorithms:
            self.ReadRecommendationArrays(algo)

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
    @staticmethod
    def rating_evaluation(arrTest, arrBase, func_map, func_fold):
        # Mask out invalid ratings
        arrBase = npm.masked_equal(arrBase, 0)
        # Map into combined array
        vec_map = np.vectorize(func_map)
        arrResult = vec_map(arrTest, arrBase)
        # Fold into the resulting value
        return func_fold(arrResult)

    def ReadBaseArrays(self):
        self.dictArrs["Base"] = []
        for i in range(1, self.numTests + 1):
            self.dictArrs["Base"].append(np.array(read_base_ratings("Test" + str(i)), np.float))

    def ReadRecommendationArrays(self, strAlgoname):
        self.dictArrs[strAlgoname] = []
        for i in range(1, self.numTests + 1):
            self.dictArrs[strAlgoname].append(np.array(read_recommendation_matrix(strAlgoname, "Test" + str(i)), np.float))
        self.predictionAlgorithms.append(strAlgoname)

    def EvaluateAlgorithm(self, strAlgoname):
        self.dictResults[strAlgoname] = []
        for i in range(self.numTests):
            results = {}
            for eAlgo in RatingEvaluator.evaluationAlgorithms.keys():
                results[eAlgo] = RatingEvaluator.rating_evaluation(self.dictArrs[strAlgoname][i], self.dictArrs["Base"][i],
                                               *RatingEvaluator.evaluationAlgorithms[eAlgo])
            self.dictResults[strAlgoname].append(results)

    def EvaluateAllAlgorithms(self):
        for algo in self.predictionAlgorithms:
            self.EvaluateAlgorithm(algo)

    def FormatResults(self):
        output = ""
        for rAlgo in self.dictResults.keys():
            output += rAlgo
            output += "\n---\n"
            for eAlgo in RatingEvaluator.evaluationAlgorithms.keys():
                output += eAlgo
                output += ":\n"
                for i in range(self.numTests):
                    output += str(i + 1)
                    output += ". "
                    output += str(self.dictResults[rAlgo][i][eAlgo])
                    output += "\n"
            output += "---\n\n"
        return output

    def LogResults(self, strDescription):
        output = ""
        output += time.ctime()
        output += "\nDescription: "
        output += strDescription
        output += "\n\n"
        output += self.FormatResults()
        logfile = open("EvaluationLog.txt", "a")
        logfile.write(output)
        if not logfile.closed:
            logfile.close()

evaluator = RatingEvaluator(["Matrix Factorization", "NearestNeighbour"], 1)
evaluator.EvaluateAllAlgorithms()
evaluator.LogResults(input("Evaluation Description:\n"))