# PHSX815_Project1

This Project allows a user to simulate the effects of dice rolls of various magnitudes and fairnesses. The user can modify the simulation by setting values for several input parameters.

The main program file is python/DiceRoll.py, which can be run with these input parameters:

-seed:		(optional) the seed for the random number generator

-Nrolls:	(optional) the number of rolls to make (>=1, default 1)

-Nsides:	(optional) the number of sides of the dice (>=2, default 6)

-probs:		(optional) the probabilities of the sides ordered least to greatest ("[P(1), ..., P(N)]", default equal probabilities. If this array does not match the number of sides, or it does not sum to 1, it will default to a fair die.)

-output:	(optional) the name of the output file to print to. if not given, the program will just print the results to stdout

Random.py has been modified to sample numbers from a categorical distribution with given probabilities. Currently, there is no analysis code. Feel free to play around with this.

For best results, run the program from the top level directory as "python python/DiceRoll.py [params]"