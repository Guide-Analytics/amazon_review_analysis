'''
#################################################
@product: Gide Product Analysis
@filename: PMI Table - PMI Analysis

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from pyspark import SparkContext

import csv
from simple_tokenize import simple_tokenize
from fuzzywuzzy import fuzz

try:
    sc = SparkContext(appName="PMI", master="local[*]")
except:
    print("Spark is already running!")
    pass

# the log function for computing PMI
# for the sake of consistency across solutions, please use log base 10
from math import log

# this imports the Counter (subset of dict) tool from collections
from collections import Counter

# this imports permutations from itertools
from itertools import permutations

## Same code from Question 1 ##
distinctT = Counter()
distinctTP = Counter()



# total number of distinct token occurrences in each line of .txt
# (where each token may occur on each line at least once, but we count that as 1 occurrence)
sumDistinctT = float((sum(distinctT.values())))

# total number of distinct token pairs occurrences in each line of .txt
# (where each word pair may occur on each line at least once; count that as 1 occurrence)
sumDistinctTP = float((sum(distinctTP.values())))


## Spark Context
def sentimentTableExtraction():

    sentimentData = sc.textFile("product_info.csv")

    sentimentData = sentimentData.map(lambda x: x.encode('utf-8'))\
                                 .mapPartitions(lambda x: csv.reader(x))\
                                 .filter(lambda x: x != [])

    productInfo = sentimentData.take(2)

    title = productInfo[0]
    header = productInfo[1]

    sentimentData = sentimentData.filter(lambda x: x != title)\
                                 .filter(lambda x: x != header)\
                                 .map(lambda x: x[3])

    return sentimentData, productInfo

# Returns a list of samp_size tuples with the following format:
# (token, [ list_of_cooccurring_tokens ])
# where list_of_cooccurring_tokens is of the form
# [((token1, token2), pmi, cooc_count, token1_count, token2_count), ...]

def seq_try(arg):
    try:
        return arg
    except ZeroDivisionError:
        return 1

def PMI_one_token(threshold):

    sentimentData = sentimentTableExtraction()[0]
    # Create an empty RDD data for output
    output = sc.parallelize([])

    # Now, let's extract keywords for fan
    fanKeywords = sc.textFile('keywords_fan.txt')\
                    .map(lambda x: x.encode('utf-8'))\
                    .map(lambda x: x.split(",")).collect()[0]

    stopwords = sc.textFile('corpus_stopwords.txt') \
                  .map(lambda x: x.encode('utf-8')) \
                  .map(lambda x: x.split(",")).collect()[0]

    # apply map onto each element and use simple_tokenize func. for each line of the txt file
    # (mappedSet will become a list of lists RDD, with each list having a distinct number of
    # tokens)
    mappedSet = sentimentData.map(lambda line: set(simple_tokenize(line)))
    numLines = mappedSet.count()
    # apply flatMap onto each element of mappedSet and use permutations for finding pairs (2)
    # in each distinct token list. (will become a list RDD with distinct token pairs)
    occurrXY = mappedSet.flatMap(lambda pair: permutations(pair, 2))

    # apply flatMap on each line so we can map to become a KeyPair (token, 1) where this
    # behaves like a Counter. Then, we calculate the occurrences of each token using
    # reduceByKey by summing all the 1's together
    occurrs = mappedSet.flatMap(lambda x: x).map(lambda x: (x, 1))
    occurrs = occurrs.reduceByKey(lambda x, y: x + y).filter(lambda x: x[1] >= threshold)
    # if the threshold is big enough, this won't take up too much memory. Furthermore, the
    # number of token occurrences are always greater or equal to number of co-occurrences
    # token pairs
    occurrs = occurrs.collectAsMap()

    # obtain co-occurrences count (similar method to "occurrences"), but take the threshold that
    # filters all token pairs that co-occurr at least the threshold
    occurrXY = occurrXY.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
    occurrXY = occurrXY.filter(lambda x: x[1] >= threshold)

    # Iterate a certain N sample size of tokens
    for token in fanKeywords:

        # retrieve only the tokens that exist in the token pairs (we don't want other
        # unnecessary token pairs)
        tokenPMI = occurrXY.filter(lambda x: fuzz.ratio(token.lower(), x[0][0]) >= 85)

        # calculate (similar to Q5), except the token is in front of each calculation.
        # token becomes the key, the calculations become the values
        tokenPMI = tokenPMI.map(lambda x: (x[0][0], x[0][1], log(((x[1] + 1e-32)/ numLines) /
                                                                 (((occurrs[x[0][0]] + 1e-32) / numLines) *
                                                                  ((occurrs[x[0][1]] + 1e-32) / numLines)), 10),
                                           occurrs[x[0][0]], occurrs[x[0][1]]))

        # filter out stopwords
        tokenPMI = tokenPMI.filter(lambda x: x[1] not in stopwords)
        #tokenPMI = tokenPMI.filter(lambda )
        # perform a union for the result of tokenPMI; group the the results together by keys
        # (tokens). The union action is used for other tokens in samp_size
        output = output.union(tokenPMI)


    return output.sortBy(lambda x: x[2], False).collect()

## Output PMI Analysis Information to CSV
def pmiCSVTable():

    result = PMI_one_token(1)

    productinfo = sentimentTableExtraction()[1]

    ppath = 'pmi_product_table.csv'
    pname = "pmi_table"

    # try:
    with open(ppath, 'wb') as csvfile:
        sentwriter = csv.writer(csvfile)
        sentwriter.writerow(productinfo[0])
        sentwriter.writerow(['Keyword', 'Keyword Pair', 'PMI', 'Keyword Count', 'Keyword Pair Count'])
        sentwriter.writerows(result)

    print("PMI Completed. Please check: " + pname)

pmiCSVTable()