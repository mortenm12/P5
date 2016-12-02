import time
import numpy as np
import numpy.ma as npm
import functools as ft
from DataAPI import *


class EvaluationAlgorithmPrefab:

    def __init__(self, name, function_generator, test_dependent):
        self.name = name
        self.function_generator = function_generator
        self.test_dependent = test_dependent


class EvaluationAlgorithm:
    AE = lambda a, b: abs(a - b)
    SE = lambda a, b: (a - b) ** 2

    # All our algorithms are prefabs with a functionGenerator, a boolean value indicating weather they are testdependant
    # or not and optional parameters.

    prefabs = {
        # Mean Absolute Error
        "MAE": EvaluationAlgorithmPrefab("MAE", lambda args: (EvaluationAlgorithm.AE, lambda arr: np.mean(arr)), False),

        # Root Mean Squared Error
        "RMSE": EvaluationAlgorithmPrefab("RMSE", lambda args: (EvaluationAlgorithm.SE, lambda arr: np.mean(arr) ** 0.5), False),

        # In the weighted measures, a weight array is multiplied with the error-array
        # The weight array is calculated as follows:
        # np.sign is used on testArray to make an array that contains a 1 if a rating exists and a 0 otherwise.
        # The sum across an axis in this array finds the amount of ratings of each user/movie which is used to make the initial weight array.
        # This is pre-processed using functools.partial, since this part of the calculation is independent of the error-array.
        # A copy of the error-array with entries replaced with 1s are then multiplied with the weight array.
        # This is needed to account for the invalid data, which makes some weights used more than others.
        # The average over this resulting array is then the average of the weights.
        # The initial weight array is then divided by this average resulting in the final weight array.

        # Partial allows us to pre-process part of the generated function, so that it happens only once and not every
        # evaluation.
        # Mean User-Ratings Weighted Absolute Error
        "MURWAE": EvaluationAlgorithmPrefab("MURWAE", lambda test_array, args: ft.partial(lambda weights: (
            EvaluationAlgorithm.AE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr))))),
            weights=np.atleast_2d(np.reciprocal(np.sum(np.sign(test_array), 0) + 1))), True),

        # Mean Movie-Ratings Weighted Absolute Error
        "MMRWAE": EvaluationAlgorithmPrefab("MMRWAE", lambda test_array, args: ft.partial(lambda weights: (
            EvaluationAlgorithm.AE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr))))),
            weights=np.atleast_2d(np.reciprocal(np.sum(np.sign(test_array), 1) + 1)).T), True),

        # Root Mean User-Ratings Weighted Square Error
        "RMURWSE": EvaluationAlgorithmPrefab("RMURWSE", lambda test_array, args: ft.partial(lambda weights: (
            EvaluationAlgorithm.SE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr)))) ** 0.5),
            weights=np.atleast_2d(np.reciprocal(np.sum(np.sign(test_array), 0) + 1))), True),

        # Root Mean Movie-Ratings Weighted Square Error
        "RMMRWSE": EvaluationAlgorithmPrefab("RMMRWSE", lambda test_array, args: ft.partial(lambda weights: (
            EvaluationAlgorithm.SE, lambda arr: npm.mean(arr * (weights / npm.mean(weights * np.ones_like(arr)))) ** 0.5),
            weights=np.atleast_2d(np.reciprocal(np.sum(np.sign(test_array), 1) + 1)).T), True),

        # In the sliced measures, a mask is applied to the error-array to ignore the ratings of users/movies with an amount
        # of ratings outside a given boundary.
        # This mask is calculated as follows:
        # np.sign is used on testArray to make an array that contains a 1 if a rating exists and a 0 otherwise.
        # The sum across an axis in this array finds the amount of ratings of each user/movie.
        # This array is then masked out where the amount of ratings is outside the given boundaries.
        # The mask of the array is pre-processed using functools.partial, since this part of the calculation is
        # independent of the error-array.
        # The mask is then changed in size and applied to the error-array.
        # Since the indexes of both arrays correlates with the same user/movie, applying this mask to the error-array
        # makes it ignore the ratings of these users/movies.

        # User-Ratings Sliced Mean Absolute Error
        "URSMAE": EvaluationAlgorithmPrefab("URSMAE", lambda test_array, args: ft.partial(lambda array_mask: (
            EvaluationAlgorithm.AE, lambda arr: np.mean(npm.masked_where(array_mask, arr))),
            array_mask=np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(test_array), 0), *args))),
                                      test_array.shape)), True),

        # Movie-Ratings Sliced Mean Absolute Error
        "MRSMAE": EvaluationAlgorithmPrefab("MRSMAE", lambda test_array, args: ft.partial(lambda array_mask: (
            EvaluationAlgorithm.AE, lambda arr: np.mean(npm.masked_where(array_mask, arr))),
            array_mask=np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(test_array), 1), *args))).T,
                                      test_array.shape)), True),

        # User-Ratings Sliced Root Mean Square Error
        "URSRMSE": EvaluationAlgorithmPrefab("URSRMSE", lambda test_array, args: ft.partial(lambda array_mask: (
            EvaluationAlgorithm.SE, lambda arr: np.mean(npm.masked_where(array_mask, arr)) ** 0.5),
            array_mask=np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(test_array), 0), *args))),
                                      test_array.shape)), True),

        # Movie-Ratings Sliced Root Mean Square Error
        "MRSRMSE": EvaluationAlgorithmPrefab("MRSRMSE", lambda test_array, args: ft.partial(lambda array_mask: (
            EvaluationAlgorithm.SE, lambda arr: np.mean(npm.masked_where(array_mask, arr)) ** 0.5),
            array_mask=np.broadcast_to(np.atleast_2d(npm.getmask(npm.masked_outside(np.sum(np.sign(test_array), 1), *args))).T,
                                      test_array.shape)), True)
    }

    # PARAMETERS:
    # mapping_function and folding_function:
    # Functions used to map and fold during evaluation. These are usually made from a prefab functionGenerator
    # name: Name of the algorithm
    def __init__(self, mapping_function, folding_function, name):
        self.mapping_function = mapping_function
        self.folding_function = folding_function
        self.name = name

    # Calling an EvaluationAlgorithm:
    # Evaluates a prediction- and a base-array into an error measure

    # INPUT:
    # prediction_array: The prediction array.
    # base_array: The base-array.

    # OUTPUT:
    # Returns the resulting error measure.
    def __call__(self, prediction_array, base_array):
        # Mask out all invalid ratings
        base_array = npm.masked_equal(base_array, 0)
        # Map into error-array
        result_array = self.mapping_function(prediction_array, base_array)
        # Fold error-array into the resulting measure
        return self.folding_function(result_array)


class RatingEvaluator:
    # All parameterless measures are evaluated as default
    default_algorithms = [
        (EvaluationAlgorithm.prefabs["MAE"], None),
        (EvaluationAlgorithm.prefabs["RMSE"], None),
        (EvaluationAlgorithm.prefabs["MURWAE"], None),
        (EvaluationAlgorithm.prefabs["MMRWAE"], None),
        (EvaluationAlgorithm.prefabs["RMURWSE"], None),
        (EvaluationAlgorithm.prefabs["RMMRWSE"], None)
    ]

    @staticmethod
    def format_name(name, args):
        if args is None:
            return name
        else:
            return name + str(args)

    # PARAMETERS:
    # predictionAlgorithms: List of names of predictionAlgorithms to evaluate
    # testIndexes: List of test-indexes for the tests used
    # evaluationAlgorithms (Optional): List of evaluation-algorithm prefabs to evaluate with.
    def __init__(self, prediction_algorithms, test_indexes, evaluation_algorithms=default_algorithms):
        self.test_indexes = test_indexes

        # Dictionary for storing arrays
        self.arrays = {}

        # Dictionary for storing results
        self.results = {}

        # Prepare base arrays
        self.read_base_arrays()

        # Prepare prediction arrays
        self.prediction_algorithm_names = prediction_algorithms
        for algorithm in prediction_algorithms:
            self.read_prediction_arrays(algorithm)

        # Test-dependent and test-independent evaluation-algorithms are prepared separately, since we only want to
        # prepare the same test-independent evaluation-algorithm once.

        # Prepare test-independent evaluation-algorithms
        self.evaluation_algorithms = {}

        # Only select the prefabs marked as test-independent
        for algorithm in filter(lambda algo: not algo[0].test_dependent, evaluation_algorithms):
            # Make an evaluation-algorithm from the prefab
            name = RatingEvaluator.format_name(algorithm[0].name, algorithm[1])
            mapping_function, folding_function = algorithm[0].function_generator(algorithm[1])
            self.evaluation_algorithms[name] = EvaluationAlgorithm(mapping_function, folding_function, name)

        # Prepare test-dependent evaluation-algorithms
        self.evaluation_algorithm_by_test = {}

        # Only select the prefabs marked as test-dependent
        for algorithm in filter(lambda algo: algo[0].test_dependent, evaluation_algorithms):
            name = RatingEvaluator.format_name(algorithm[0].name, algorithm[1])
            self.evaluation_algorithm_by_test[name] = {}

        for i in test_indexes:
            test_array = np.array(read_ratings("Test" + str(i)), np.float)

            # Again, only select the prefabs marked as test-dependent
            for algorithm in filter(lambda algo: algo[0].test_dependent, evaluation_algorithms):
                # Make an evaluation-algorithm from the prefab. The parameter-less call performs the pre-processing.
                mapping_function, folding_function = algorithm[0].function_generator(test_array, algorithm[1])()
                name = RatingEvaluator.format_name(algorithm[0].name, algorithm[1])
                self.evaluation_algorithm_by_test[name][i] = EvaluationAlgorithm(mapping_function, folding_function, name)

    def read_base_arrays(self):
        self.arrays["Base"] = {}
        for i in self.test_indexes:
            self.arrays["Base"][i] = np.array(read_base_ratings("Test" + str(i)), np.float)

    def read_prediction_arrays(self, algorithm_name):
        self.arrays[algorithm_name] = {}
        for i in self.test_indexes:
            self.arrays[algorithm_name][i] = np.array(read_recommendation_matrix(algorithm_name, "Test" + str(i)), np.float)

    def evaluate_algorithm(self, algorithm_name):
        self.results[algorithm_name] = {}
        for i in self.test_indexes:
            results = {}

            # Test-dependent and test-independent evaluation-algorithms are used separately, since we only want to
            # evaluate with the same test-independent evaluation-algorithm once.
            for evaluation_algorithm in self.evaluation_algorithms.values():
                # Call the evaluation-algortihm with the prediction- and the base-array, and store the result.
                results[evaluation_algorithm.name] = evaluation_algorithm(self.arrays[algorithm_name][i], self.arrays["Base"][i])

            for evaluation_algorithm in self.evaluation_algorithm_by_test.values():
                # Call the evaluation-algortihm with the prediction- and the base-array, and store the result.
                results[evaluation_algorithm[i].name] = evaluation_algorithm[i](self.arrays[algorithm_name][i], self.arrays["Base"][i])
            self.results[algorithm_name][i] = results

    def evaluate_all_algorithms(self):
        for algorithm in self.prediction_algorithm_names:
            self.evaluate_algorithm(algorithm)

    # Returns a formatted string of the results
    def format_results(self):
        output = ""
        for prediction_algorithm in self.prediction_algorithm_names:
            output += prediction_algorithm
            output += "\n---\n"
            for evaluation_algorithm in sorted(list(self.evaluation_algorithms.keys()) + list(self.evaluation_algorithm_by_test.keys())):
                output += evaluation_algorithm
                output += ":\n"
                for i in self.test_indexes:
                    output += str(i)
                    output += ". "
                    output += str(self.results[prediction_algorithm][i][evaluation_algorithm])
                    output += "\n"
            output += "---\n\n"
        return output

    # Appends the results in a formatted way to a logfile
    def log_results(self, description):
        output = ""
        output += time.ctime()
        output += "\nDescription: "
        output += description
        output += "\n\n"
        output += self.format_results()
        logfile = open("EvaluationLog.txt", "a")
        logfile.write(output)
        if not logfile.closed:
            logfile.close()

predictionAlgorithms = [
    "Weighted Content Based",
    "v2.0NearestNeighbour",
    "Matrix Factorization V.2"
]

splits = range(0,1000)

evaluationAlgorithms = []

for split in splits:
    evaluationAlgorithms.append((EvaluationAlgorithm.prefabs["MRSRMSE"], (0,  split)))
    evaluationAlgorithms.append((EvaluationAlgorithm.prefabs["MRSRMSE"], (split + 1,  1000)))

def print_splits(predictionAlgorithms, splits):
    evaluator = RatingEvaluator(predictionAlgorithms, range(1, 6), evaluationAlgorithms)
    evaluator.evaluate_all_algorithms()
    for split in splits:
        sums = {}
        for tailAlgo in predictionAlgorithms:
            for headAlgo in predictionAlgorithms:
                sums[(tailAlgo, headAlgo)] = 0
                for i in range(1,6):
                    sums[(tailAlgo, headAlgo)] += evaluator.results[tailAlgo][i][RatingEvaluator.format_name("MRSRMSE", (0, split))]
                    sums[(tailAlgo, headAlgo)] += evaluator.results[headAlgo][i][RatingEvaluator.format_name("MRSRMSE", (split + 1,  1000))]
        lowest = min(sums, key = lambda item: sums[item])
        print("Split:" + str(split) + " BestTailHead:" + str(lowest) + " AverageError:" + str(sums[lowest] / 10))