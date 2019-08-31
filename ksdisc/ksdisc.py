from math import fabs
from random import random
import numpy as np


def _calcEcdf(samples, function_length):
	nr_of_points = sum(samples)
	assert nr_of_points >= 0

	ecdf = [0.0] * function_length
	nr_of_points = float(nr_of_points)
	running_sum = 0.0
	for i in range(function_length):
		running_sum += samples[i] / nr_of_points
		ecdf[i] = running_sum
	return ecdf


def ksDisc(samples, test_cdf, iters=10000):
	# TODO: Throw errors instead of asserts
	assert len(samples) == len(test_cdf)
	assert len(test_cdf) >= 2
	assert iters > 0

	function_length = len(test_cdf)

	for i in range(function_length-1):
		#assert cdf_x[i] < cdf_x[i+1]
		assert test_cdf[i] <= test_cdf[i+1]

	eps = 1.0e-8
	assert fabs(test_cdf[-1] - 1.0) < eps

	for s in samples:
		assert type(s) == type(1)
		assert s >= 0
	nr_of_points = sum(samples)

	ecdf = _calcEcdf(samples, function_length)
	epdf = [el / float(nr_of_points) for el in samples]
	assert fabs(ecdf[-1] - 1.0) < eps  # Remove, only for debugging.
	ecdf[-1] = 1.0

	diffs = [fabs(test_cdf[i]-ecdf[i]) for i in range(function_length)]
	base_ks = max(diffs)

	counter = 0
	arrs = np.arange(0, function_length)
	for itr in range(iters):
		new_samples = np.random.choice(arrs, (nr_of_points), p=epdf)
		#new_samples = _generateNewSample(test_cdf, nr_of_points)
		new_ecdf = _calcEcdf(new_samples, function_length)

		diffs = [fabs(test_cdf[i]-new_ecdf[i]) for i in range(function_length)]
		new_ks = max(diffs)

		if new_ks > base_ks:
			counter += 1

	return counter / float(iters)


if __name__ == '__main__':
	from random import randint
	#y = [250 + randint(0, 10) for _ in range(5)]
	y = [0]*5
	for _ in range(8):
		r = randint(0, 4)
		if random() < 0.00005:
			r = 1
		y[r] += 1

	_cdf = [i/5 for i in range(1, 6)]

	out = ksDisc(y, _cdf)
	print(out)
