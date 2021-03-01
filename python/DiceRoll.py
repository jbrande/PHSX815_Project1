#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import re
import json


# import our Random class from python/Random.py file
sys.path.append(".")
from python.Random import Random

# main function for our coin toss Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number] [-Nrolls integer] [-Nsides integer] [-probs 'array of floats'] [-output string]" % sys.argv[0])
        print ("-seed:      (optional) the seed for the random number generator")
        print ("-Nrolls:    (optional) the number of rolls to make (>= 1, default 1)")
        print ("-Nsides:    (optional) the number of sides of the dice (>=2, default 6)")
        print ("-probs:     (optional) the probabilities of the sides ordered least to greatest ('[P(1), ..., P(N)]'. If this array does not match the number of sides, or it does not sum to 1, it will default to a fair die.)")
        print ("-output:    (optional) the name of the output file to print to. if not given, the program will just print the results to stdout")
        print
        sys.exit(1)

    # default seed
    seed = 66045 # KU zip code

    Nsides = 6

    # default equal probabilities for each side
    probs = None

    # default number of dice rolls
    Nrolls = 1

    # output file defaults
    doOutputFile = False

    # read the user-provided arguments from the command line (if there)
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]
    if '-probs' in sys.argv:
        p = sys.argv.index('-probs')
        probs = re.sub(r"\s+", "", sys.argv[p+1], flags=re.UNICODE) # get string of probabilities, remove all whitespace
    if '-Nrolls' in sys.argv:
        p = sys.argv.index('-Nrolls')
        Nrolls = int(sys.argv[p+1])
        if Nrolls < 1:
            print("Nrolls must be >= 1")
            sys.exit(1)
    if '-Nsides' in sys.argv:
        p = sys.argv.index('-Nsides')
        Nsides = int(sys.argv[p+1])
        if Nsides < 2:
            print("Nsides must be >= 2")
            sys.exit(1)
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True



    # unrelated: easiest way to get random probabilities that sum to 1
    # get nsides random numbers, divide them each by the sum of the numbers

    # check probabilities:
    # if no probabilities were given, make some
    if probs == None:
        probs = ((1.0/Nsides) * np.ones(Nsides)).tolist()
    else:
        # check probability string for cleanliness with regex
        # checks for square bracketed arrays of ints or floats
        pattern = r"\[(\d(\.\d*)?,)*(\d(\.\d*)?)\]"
        if re.match(pattern, probs) == None:
            print("Please ensure the probability array is formatted correctly.")
            sys.exit(1)
        else:
            # split string into individual numbers, make probability array of floats
            strprobs = probs.lstrip("[").rstrip("]").split(",")
            probs = []
            for s in strprobs:
                probs.append(float(s))

    # checks for numerical validity. if the sum of the array is significantly > or < 1, quit.
    ep = 1e-6
    if (np.abs(1 - np.sum(probs)) < ep):
        pass;
    else:
        print(np.sum(probs))
        print("Probabilities must sum to 1")
        sys.exit(1)
    
    # class instance of our Random class using seed
    random = Random(seed)

    # structure to hold results
    results = {
        "nsides": Nsides,
        "probs": probs,
        "nrolls": Nrolls,
        "rolls": "",
    }

    # do the rolls, add each roll to the string
    rolls = []
    for i in range(Nrolls):
        rolls.append(random.Categorical(probs))
    if (-1 in rolls):
        print("Something Broke")
        sys.exit(1)
    else:
        results["rolls"] = rolls


    # for later analysis, print the results as a JSON object to a file
    if doOutputFile:
        outfile = open(OutputFileName, 'w')
        outfile.write(json.dumps(results))
        outfile.close()
    else: # or, just print the results to the console
        print("Rolling a die:")
        print("Number of sides: {},\nSide probabilities {},\nNumber of rolls: {}".format(Nsides, probs, Nrolls))
        print("Results: {}".format(results["rolls"]))
   
