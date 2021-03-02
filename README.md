# PHSX815_Project1

Needed dependencies: numpy, matplotlib

This Project allows a user to simulate the effects of dice rolls of various magnitudes and fairnesses. The user can modify the simulation by setting values for several input parameters.

The main program file is python/DiceRoll.py, which can be run with these input parameters:

-seed:		(optional) the seed for the random number generator

-Nrolls:	(optional) the number of rolls to make (>=1, default 1)

-Nsides:	(optional) the number of sides of the dice (>=2, default 6)

-probs:		(optional) the probabilities of the sides ordered least to greatest ("[P(1), ..., P(N)]", default equal probabilities. If this array does not match the number of sides, or it does not sum to 1, it will default to a fair die.)

-output:	(optional) the name of the output file to print to. if not given, the program will just print the results to stdout

Random.py has been modified to sample numbers from a categorical distribution with given probabilities.


After the dice are rolled, and the output saved to a file, the user can then plot the results of the simulations with python/DicePlot.py. This takes three input parameters:

-input0:     (mandatory) H0: the name of the file which holds the rolled dice data")

-input1:     (mandatory) H1: the name of the file which holds the rolled dice data")

-comb:	 	 (mandatory) given this number of dice (< num total rolls) plot the distribution of the sums of those rolls")

This will read in the JSON results from input0 and input1, and calculate the needed quantities and plot the various histograms: a histogram of the frequencies of the faces found from many single die rolls, the probabilities of the sums of grouped dice rolls, and the log-likelihood ratios for H0 and H1. 

For best results, run the programs from the top level directory as "python python/program_name.py -params"
