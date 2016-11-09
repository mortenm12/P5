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
    # Normalized X Information Weighted Mean Absolute Error
    def generate_XIW(self, arrTests):
        return (lambda a, b: abs(a - b), lambda arr: npm.mean(arr * (arrTests / npm.mean(arrTests * np.ones_like(arr)))))
    # Normalized Root X Information Weighted Mean Square Error
    def generate_XIWRS(self, arrTests):
        return (lambda a, b: (a - b) ** 2, lambda arr: npm.mean(arr * (arrTests / npm.mean(arrTests * np.ones_like(arr)))) ** 0.5)
    # X = User or Movie
    testDependantEvalAlgorithms = ["UIW", "MIW", "UIWRS", "MIWRS"]

    def __init__(self, predAlgorithms, numTests):
        self.arrsEvalAlgorithmsByTest = []
        self.dictArrs = {}
        self.dictResults = {}
        self.numTests = numTests
        self.predictionAlgorithms = []
        self.ReadBaseArrays()
        for algo in predAlgorithms:
            self.ReadRecommendationArrays(algo)
        for i in range(1, numTests + 1):
            arrTests = np.sign(np.array(read_ratings("Test" + str(i)), np.float))
            arrUTests = np.atleast_2d(np.reciprocal(np.sum(arrTests, 0) + 1))
            arrMTests = np.atleast_2d(np.reciprocal(np.sum(arrTests, 1) + 1)).T
            perXFunc = {}
            perXFunc["UIW"] = self.generate_XIW(arrUTests)
            perXFunc["MIW"] = self.generate_XIW(arrMTests)
            perXFunc["UIWRS"] = self.generate_XIWRS(arrUTests)
            perXFunc["MIWRS"] = self.generate_XIWRS(arrMTests)
            self.arrsEvalAlgorithmsByTest.append(perXFunc)

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
            for eAlgo in self.testDependantEvalAlgorithms:
                results[eAlgo] = RatingEvaluator.rating_evaluation(self.dictArrs[strAlgoname][i], self.dictArrs["Base"][i],
                                                                    *self.arrsEvalAlgorithmsByTest[i][eAlgo])
            self.dictResults[strAlgoname].append(results)

    def EvaluateAllAlgorithms(self):
        for algo in self.predictionAlgorithms:
            self.EvaluateAlgorithm(algo)

    def FormatResults(self):
        output = ""
        for rAlgo in sorted(self.dictResults.keys()):
            output += rAlgo
            output += "\n---\n"
            for eAlgo in sorted(RatingEvaluator.evaluationAlgorithms.keys()) + self.testDependantEvalAlgorithms:
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


evaluator = RatingEvaluator(["NearestNeighbour", "Matrix Factorization"], 1)
evaluator.EvaluateAllAlgorithms()
evaluator.LogResults(input("Evaluation Description:\n"))