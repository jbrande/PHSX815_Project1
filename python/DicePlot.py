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

# main function for our coin toss Python code
if __name__ == "__main__":
	# if no args passed (need at least the input file), dump the help message
	# if the user includes the flag -h or --help print the options
	if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
		print ("Usage: %s [-seed number] [-Nrolls integer] [-Nsides integer] [-probs 'array of floats'] [-output string]" % sys.argv[0])
		print ("-input:     (mandatory) the name of the file which holds the rolled dice data")
		print("-plot_comb: 	(optional)  given some number of dice (< num total rolls) plot the distribution of the sums of those rolls")
		print
		sys.exit(1)

	# read the user-provided arguments from the command line (if there)
	if '-input' in sys.argv:
		p = sys.argv.index('-input')
		try:
			inputfile = sys.argv[p+1]
			#print(inputfile)
		except IndexError as e:
			print("Must pass input filename")

	if '-plot_comb' in sys.argv:
		p = sys.argv.index('-plot_comb')
		comb = int(sys.argv[p+1])

	jsondata = ""
	with open(inputfile) as f:
		jsondata = json.load(f)
		f.close()


	nsides = jsondata["nsides"]
	nrolls = jsondata["nrolls"]
	probs = jsondata["probs"]
	rolls = jsondata["rolls"]


	# get split locations to calculate sums of dice combinations
	inds = np.arange(0, len(rolls), comb)[1:]

	# split rolls into subarrays, and sum them
	splits = np.split(rolls, inds)
	sums = []
	for s in splits:
		sums.append(np.sum(s))
	#print(sums)

	fig = plt.figure()
	plt.hist(rolls, nsides)
	plt.xlabel('Roll Values')
	plt.ylabel('Frequency')
	plt.title('Freq. of Dice Rolls')
	plt.show()
	fig.savefig("result_hist_uneven.jpg", dpi=180)

	fig = plt.figure()
	plt.hist(sums, 100)
	plt.xlabel('Sum')
	plt.ylabel('Frequency')
	plt.title('Sums of {} Dice'.format(comb))
	plt.show()
	fig.savefig("sum_hist_uneven.jpg", dpi=180)
