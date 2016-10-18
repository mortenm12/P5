import numpy as np
from DataAPI import DataAPI

NRMSE = (lambda a, b: (a - b) ** 2, lambda i: sum(i) ** 0.5 / len(i))
NMAE = (lambda a, b: abs(a - b), lambda i: sum(i) / len(i))

basearrays = []
basearrays.append(np.array(DataAPI.read_ratings("Test1Target")))

def rating_evaluation(arrTest, arrBase, func_map, func_fold):
    arrKnown = np.sign(arrBase)
    iterAll = zip(np.nditer(arrTest), np.nditer(arrBase), np.nditer(arrKnown))
    iterKnown = filter(lambda item: item[2] == 1, iterAll)
    iterMapd = map(lambda item: func_map(item[0], item[1]), iterKnown)
    return func_fold(list(iterMapd))

print(rating_evaluation(basearrays[0], basearrays[0], *NMAE))