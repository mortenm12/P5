import Evaluation

def SlicedError(predictionAlgo, lowest, highest):
    evaluator = Evaluation.RatingEvaluator([predictionAlgo], range(1,6), [(Evaluation.EvaluationAlgorithm.prefabs["MRSMAE"], (lowest, highest))])
    name = Evaluation.RatingEvaluator.formatName("MRSMAE", (lowest, highest))
    evaluator.EvaluateAlgorithm(name)
    results = list(map(lambda item: item[name], evaluator.results[predictionAlgo].values()))
    return sum(results) / len(results)

print(SlicedError("Matrix Factorization", 0, 10))