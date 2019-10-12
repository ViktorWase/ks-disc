from math import fabs
from random import random, shuffle
from copy import copy
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


def _calc2sampleKS(samples1_inp, samples2_inp):
	samples1 = copy(samples1_inp)
	samples2 = copy(samples2_inp)
	samples1.sort()
	samples2.sort()

	counter1 = 0
	y1 = 0.0
	counter2 = 0
	y2 = 0.0

	max_diff = 0.0
	while counter1 < len(samples1) and counter2 < len(samples2):
		if samples1[counter1] < samples2[counter2]:
			y1 += 1.0/len(samples1)
			counter1 += 1
		elif samples2[counter2] < samples1[counter1]:
			y2 += 1.0/len(samples2)
			counter2 += 1
		else:
			y1 += 1.0/len(samples1)
			y2 += 1.0/len(samples2)
			counter1 += 1
			counter2 += 1

		diff = fabs(y1 - y2)
		if diff > max_diff:
			max_diff = diff

	return max_diff


def ksDisc2sample(samples1, samples2, iters=1000):
	assert len(samples1) > 0
	assert len(samples2) > 0
	assert iters > 0

	# Calculate the ks between the samples
	org_diff = _calc2sampleKS(samples1, samples2)

	long_samples = samples1 + samples2
	more_than_counter = 0
	for itr in range(iters):
		lables = [False]*len(samples1) + [True]*len(samples2)
		shuffle(lables)

		new_samples1 = [0.0] * len(samples1)
		new_samples2 = [0.0] * len(samples2)
		index1 = 0
		index2 = 0
		for i in range(len(long_samples)):
			if lables[i]:
				new_samples2[index2] = long_samples[i]
				index2 += 1
			else:
				new_samples1[index1] = long_samples[i]
				index1 += 1

		new_diff = _calc2sampleKS(new_samples1, new_samples2)

		if new_diff > org_diff:
			more_than_counter += 1

	return more_than_counter / float(iters)


def _calc1sampleKS(samples_in, cdf):
	y = 0.0
	max_diff = 0.0
	samples = copy(samples_in)
	samples.sort()

	for i in range(len(samples)):
		y += 1.0 / len(samples)

		if i == len(samples)-1 or samples[i] != samples[i+1]:
			cdf_val = cdf(samples[i])
			assert cdf_val >= 0.0
			assert cdf_val <= 1.0

			diff = fabs(cdf_val - y)

			if diff > max_diff:
				max_diff = diff
	return max_diff


def _generateSamplesFromCDF(cdf, nr_of_points):
	outs = [0]*nr_of_points
	cdf_0_val = cdf(0)
	for i in range(nr_of_points):
		r = random()
		if r > cdf_0_val:
			index = 0
			while cdf(index) < r:
				index += 1
			outs[i] = index
		elif r <= cdf_0_val:
			index = 0
			while cdf(index) >= r:
				index -= 1
			outs[i] = index + 1

	return outs


def ksDisc(samples, cdf, iters=1000):
	# TODO: Throw errors instead of asserts
	assert iters > 0

	for s in samples:
		assert type(s) == type(1)
	nr_of_points = len(samples)

	# Calc diff between samples and cdf
	orig_diff = _calc1sampleKS(samples, cdf)

	counter = 0
	for itr in range(iters):
		new_samples = _generateSamplesFromCDF(cdf, nr_of_points)
		new_diff = _calc1sampleKS(new_samples, cdf)

		if new_diff > orig_diff:
			counter += 1

	return counter / float(iters)


if __name__ == '__main__':
	from random import randint

	# 1-sample test
	y = [randint(1, 3) for _ in range(20)]  # Uniform in [1, 3]
	_cdf = lambda x: 0.0 if x < 0 else min(0.25*x, 1.0) # Uniform in [1, 4]

	out = ksDisc(y, _cdf)
	print(out)

	# 2-sample test
	samples1 = [randint(1, 15) for _ in range(1000)]
	samples2 = [randint(1, 15) if random()<0.95 else 3 for _ in range(1000)]
	out = ksDisc2sample(samples1, samples2, iters=1000)

	print(out)
