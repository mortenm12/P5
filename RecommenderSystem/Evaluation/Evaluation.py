import numpy as np

NRMSE = (lambda a, b: np.square(a - b), lambda i: sum(i) ** 0.5 / i.itersize)
NMAE = (lambda a, b: np.absolute(a - b), lambda i: sum(i) / i.itersize)

def ratingevaluation(arrA, arrB, func_map, func_fold):
	arrMapd = func_map(arrA, arrB)
	iterator = np.nditer(arrMapd)
	return func_fold(iterator)