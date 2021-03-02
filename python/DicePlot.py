# #! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import re
import json

import matplotlib.pyplot as plt

# import our Random class from python/Random.py file
sys.path.append(".")
from python.Random import Random
usecomb = False
# main function for our coin toss Python code
if __name__ == "__main__":
	# if no args passed (need at least the input file), dump the help message
	# if the user includes the flag -h or --help print the options
	if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
		print ("Usage: %s [-input0 string] [-input1 string] [-comb int]" % sys.argv[0])
		print ("-input0:     (mandatory) H0: the name of the file which holds the rolled dice data")
		print ("-input1:     (mandatory) H1: the name of the file which holds the rolled dice data")
		print ("-comb:	 	 (mandatory) given this number of dice (< num total rolls) plot the distribution of the sums of those rolls")
		print
		sys.exit(1)

	# read the user-provided arguments from the command line (if there)
	if '-input0' in sys.argv:
		p = sys.argv.index('-input0')
		try:
			input0 = sys.argv[p+1]
		except IndexError as e:
			print("Must pass input0 filename")
	else:
		print("Must pass input0 filename")

	if '-input1' in sys.argv:
		p = sys.argv.index('-input1')
		try:
			input1 = sys.argv[p+1]
		except IndexError as e:
			print("Must pass input1 filename")
	else:
		print("Must pass input1 filename")

	if '-comb' in sys.argv:
		p = sys.argv.index('-comb')
		try:
			comb = int(sys.argv[p+1])
			usecomb = True
		except IndexError as e:
			print("Must pass number of dice to group")
	else:
		print("Must pass number of dice to group")


	# load json data for both trials from files
	res0 = ""
	with open(input0) as f:
		res0 = json.load(f)
		f.close()

	res1 = ""
	with open(input1) as f:
		res1 = json.load(f)
		f.close()

	# get split locations to calculate sums of dice combinations
	inds0 = np.arange(0, len(res0["rolls"]), comb)[1:]

	# split rolls into subarrays, and sum them
	splits0 = np.split(res0["rolls"], inds0)
	sums0 = []
	for s in splits0:
		sums0.append(np.sum(s))
	#print(sums)

	inds1 = np.arange(0, len(res1["rolls"]), comb)[1:]

	# split rolls into subarrays, and sum them
	splits1 = np.split(res1["rolls"], inds1)
	sums1 = []
	for s in splits1:
		sums1.append(np.sum(s))
	#print(sums)

	# plot single roll histograms
	fig, ax = plt.subplots(1, 2, figsize=(15, 6))#, sharey=True)
	ax[0].hist(res0["rolls"], res0["nsides"], label="Die 0")
	ax[1].hist(res1["rolls"], res1["nsides"], label="Die 1")
	ax[0].set_xlabel('Roll Values')
	ax[1].set_xlabel('Roll Values')
	ax[0].set_ylabel('Frequency')
	ax[0].legend()
	ax[1].legend()
	plt.suptitle("Single Die Roll Face Frequencies")
	plt.show()
	fig.savefig("plots/fair_unfair_hist.jpg", dpi=180)


	if usecomb:
		# plot grouped roll histograms
		# for probability distributions, find freedman-diaconis bin width: https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data
		sums0 = np.array(sums0)
		q25, q75 = np.percentile(sums0,[.25,.75])
		bin_width0 = 2*(q75 - q25)*len(sums0)**(-1/3)
		bins0 = round((sums0.max() - sums0.min())/bin_width0)

		sums1 = np.array(sums1)
		q25, q75 = np.percentile(sums1,[.25,.75])
		bin_width1 = 2*(q75 - q25)*len(sums1)**(-1/3)
		bins1 = round((sums1.max() - sums1.min())/bin_width1)

		fig, ax = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
		ax[0].hist(sums0, bins0, density=True, stacked=True, label="Die 0")
		ax[1].hist(sums1, bins1, density=True, stacked=True, label="Die 1")
		ax[0].set_xlabel('Group Sum')
		ax[1].set_xlabel('Group Sum')
		ax[0].set_ylabel('Probability')
		ax[0].legend()
		ax[1].legend()
		plt.suptitle('Sums of {} Dice'.format(comb))
		plt.show()
		fig.savefig("plots/fair_unfair_sum_hist.jpg", dpi=180)


	# get log likelihood ratios
	llrs0 = []
	for sub in splits0:
		llr0 = 0
		for i in range(len(sub)):
			if sub[i] == 1:
				llr0 += np.log(res1["probs"][0] / res0["probs"][0])
			if sub[i] == 2:
				llr0 += np.log(res1["probs"][1] / res0["probs"][1])
			if sub[i] == 3:
				llr0 += np.log(res1["probs"][2] / res0["probs"][2])
			if sub[i] == 4:
				llr0 += np.log(res1["probs"][3] / res0["probs"][3])
			if sub[i] == 5:
				llr0 += np.log(res1["probs"][4] / res0["probs"][4])
			if sub[i] == 6:
				llr0 += np.log(res1["probs"][5] / res0["probs"][5])
		llrs0.append(llr0)


	llrs1 = []
	for sub in splits1:
		llr1 = 0
		for i in range(len(sub)):
			if sub[i] == 1:
				llr1 += np.log(res1["probs"][0] / res0["probs"][0])
			if sub[i] == 2:
				llr1 += np.log(res1["probs"][1] / res0["probs"][1])
			if sub[i] == 3:
				llr1 += np.log(res1["probs"][2] / res0["probs"][2])
			if sub[i] == 4:
				llr1 += np.log(res1["probs"][3] / res0["probs"][3])
			if sub[i] == 5:
				llr1 += np.log(res1["probs"][4] / res0["probs"][4])
			if sub[i] == 6:
				llr1 += np.log(res1["probs"][5] / res0["probs"][5])
		llrs1.append(llr1)

	llrs0 = np.sort(llrs0)
	llrs1 = np.sort(llrs1)

	# get boundary for 95% confidence interval
	alpha = 0.05
	alpha_index = int(len(llrs0) - len(llrs0)*alpha)
	#print(alpha_index)

	# plot the LLR plots
	fig = plt.figure()
	plt.hist(llrs0, 100, label="P(lambda|H0)", density=True, stacked=True)
	plt.axvline(llrs0[alpha_index], color="k", linestyle="--", label="alpha = 0.05")
	plt.hist(llrs1, 100, label="P(lambda|H1)", density=True, stacked=True)
	plt.xlabel("LLR")
	plt.ylabel("Probability")
	plt.title("Log-Likelihood Ratios")
	plt.legend()
	plt.show()
	fig.savefig("plots/LLRs_unfair.jpg", dpi=180)