'''
#################################################
@product: Gide Product Analysis
@filename: Word Extraction/Analysis 

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import review_input
from itertools import product


def wordAnalysis(reviewData): 
    
    '''
    @purpose: Word Analysis for each review according to the characteristics text file
    of keywords. The output of the words will be in a list of words found in a particular review.
    The review text will also be in a list according to the word found. 
    
    @inputs: reviewData [list of review information from inputReview]
    @outputs: word_features [list of review information that will contain a list of words
    for each review]
    '''
    
    rev_dict = review_input.inputRev(reviewData)
    features = review_input.charact()
            
    word_features = []
    
    for value in rev_dict:
        
        lstoffeat = []
        lstofsentences = []
        author = value[0]
        prodt = value[2]
        url = value[3]
        authorid = value[4]
        
        for feat, bodyreview in product(features, value[1]):
            
            sentence = "".join(bodyreview).encode('utf-8')
            sentence = sentence.replace("\n", " ")
            if feat in sentence.lower() and feat not in lstoffeat:
                lstoffeat.append(feat)
                lstofsentences.append(sentence)
                
        word_features.append([prodt, url, authorid, author, lstoffeat, lstofsentences])

    return word_features
