'''
#################################################
@product: Gide Product Analysis
@filename: Quality Word Usage Analysis

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from initiateScore import dataBaseWordsLabelling
from initiateScore import dataBaseSelectScore
from initiateScore import dataBaseUpdateScore
from Database import data_config

import pandas as pd
import numpy as np
import scipy.stats as ss
import math

from nltk.tokenize import word_tokenize
from scipy.optimize import minimize_scalar
from collections import Counter
from score_config import quality_word_score

'''
@purpose: Database Configuration Values
'''

dbname = data_config.databaseHost()[0]
host = data_config.databaseHost()[1]
port = data_config.databaseHost()[2]
userID = data_config.databaseHost()[3]
pwd = data_config.databaseHost()[4]

wordsData = dataBaseWordsLabelling(dbname, host, port, userID, pwd)
authorScore = dataBaseSelectScore(dbname, host, port, userID, pwd)[0]

'''
@purpose: Table Configuration Values
'''

tableName = quality_word_score()[0]
scoreColumn = quality_word_score()[1]

def qualityWordUsageStart():
    
    '''
    @purpose: Starting quality word analysis 
    
    '''
    
    print("Starting Word Quality Analysis")
    wordQualityScore()
    print("Finished Word Quality Analysis")
    
def modelInitiate():
    
    '''
    @purpose: Extracting one author review information and all author information
    to build and construct a model analysis between one author and all authors
    and analyze the author's use of quality words
    
    Note: I won't be surprised if the algorithm analysis is not clear you below or 
    it is super confusing because it is confusing!
    
    '''
    
    CAP = product_characteristics()[0] ## One review for one author
    CARP = product_characteristics()[1] ## All reviews for one author
    CAAP = product_characteristics()[2] ## All reviews for all authors
    CGP = product_characteristics()[3] ## All reviews by increments for all author (change in the reviews)
    #CT = product_characteristics()[4] 
    
    CMA = confusionMatrixConst(CAP, CARP) ## Confusion matrix (relationship model matrix of authors and their reviews)
    CMG = confusionMatrixConst(CAAP, CGP) ## Confusion matrix (relationship model matrix of overall reviews)
    #CMT = confusionMatrixConst(CARP, CT)
    
    V_author = cramersStatsAlgo(CMA) ## Calculation Cramer's V to determine the relationship of the words and the reviews
    V_general = cramersStatsAlgo(CMG)
    return V_author, V_general

def confusionMatrixConst(data1, data2):
    
    '''
    @purpose: Confusion Matrix construction
    
    @inputs: data1 [list], data2 [list] (from modelInititate.py)
    @outputs: confusion_matrix [pandas array]
    '''
   
    cm_author = pd.Series(data1, name = 'Authors')
    cm_relative = pd.Series(data2, name = 'General')

    confusion_matrix = pd.crosstab(cm_author, cm_relative)
    
    return confusion_matrix
     
def cramersStatsAlgo(confusion_matrix):
    
    '''
    Cramer's V analysis algorithm using the confusion matrix inputs
    and calculate the relationships between the words used for each author and
    the word use for all the author; using a chi-squared distribution and cramer's V
    to determine the probability of the word's relationship - the cramer's V value is a measure 
    of the relationship
    
    @inputs: confusion_matrix [pandas array]
    @outputs: V [float]
    
    '''
    
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    
    with np.errstate(divide='ignore'):  
        phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
        rcorr = r - ((r-1)**2)/(n-1)
        kcorr = k - ((k-1)**2)/(n-1)
        try:
            V = np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))
        except:
            V = 0
    return V

def product_characteristics():
    
    '''
    @purpose:
    
    @outputs: CAP [list], CARP [list], CAAP [list], CGP [list], CT [list], authorIDInfo [list], 
    all_corpus [list]
    
    '''
    
    authorIDInfo = []
    countAllAuthorPercentage = [] ## All author reviews
    countAuthorPercentage = [] ## One review for one author
    countAuthorReviewsPercentage = [] ## All reviews for one author
    countGeneralPercentage = [] ## All reviews for all authors (reviews percentages (how much it changed) 
    all_corpus = []
    all_reviews = [] ## All reviews
    
    
    for authorID, author, corpus_words, review in wordsData:
        author
        
        all_author_corpus = [] ## All author corpus words
        all_author_reviews = [] ## All author reviews
        '''
        Word Tokenization
        '''
        word_tokens = word_tokenize(review)
        indiv_reviews = word_tokens
        
        '''
        One individual author comparision with corpus and review
        '''
        featureWordCount = float(len(corpus_words)) ## Individual Author Corpus count
        totalWordCount = float(len(indiv_reviews)) ## Individual Author Review Count
        
        '''
        One individual author percentage
        '''
        try:
            relative_percentage = float("{0:.3f}".format(featureWordCount/totalWordCount))
        except:
            relative_percentage = 0.0
        
        '''
        Change in the use of corpus and reviews in ONE individual author
        One individual author (incremental reviews) percentage
        '''
        
        all_author_corpus.extend(corpus_words)    
        all_author_reviews.extend(indiv_reviews)
        authorIncCount = float(len(all_author_corpus))
        totalAuthorIncCount = float(len(all_author_reviews))
        
        try:
            authorIncPercentage = float("{0:.3f}".format(authorIncCount/totalAuthorIncCount))
        except:
            authorIncPercentage = 0.0
            
            '''
            Two data correlation: Author versus Author's All reviews
            '''
        countAuthorPercentage.append(relative_percentage)
        countAuthorReviewsPercentage.append(authorIncPercentage)
        '''
        Change in the use of corpus and reviews in all individual authors
        '''
        
        all_corpus.extend(corpus_words)
        all_reviews.extend(indiv_reviews)
        incrementedCount = float(len(all_corpus)) 
        totalIncrementCount = float(len(all_reviews))
        
        try:
            incremented_percentage = float("{0:.3f}".format(incrementedCount/totalIncrementCount))
        except:
            incremented_percentage = 0.0
            
        '''
        Two data correlation: Authors versus All reviews
        '''
        countAllAuthorPercentage.append(relative_percentage)
        countGeneralPercentage.append(incremented_percentage)
        
        '''
        Two data correlation: Author versus All reviews
        '''
        countAuthorPercentage
        countGeneralPercentage
        
        authorIDInfo.append([authorID, relative_percentage])
        
    '''
    Total percentage
    '''   
    farc = float(len(all_corpus))
    arc = float(len(all_reviews))
    try:
        countTotal = float("{0:.4f}".format(farc/arc))
    except:
        countTotal = 0.0
    
    ''' Author versus Author's All reviews: CAP, CARP
        Authors versus All reviews: CAAP, CGP
        Authors versus Total reviews: CAAP, CT
    '''
    
    CAP = countAuthorPercentage
    CARP = countAuthorReviewsPercentage
    
    CAAP = countAllAuthorPercentage
    CGP = countGeneralPercentage
    
    CT = countTotal
    
    return CAP, CARP, CAAP, CGP, CT, authorIDInfo, all_corpus
    
def neg_zipf_likelihood(s):
    
    ''' The distribution of word frequencies is often characterized by Zipf's law, 
    which states that it has Pareto distribution p(k) ~ k^-s, so-called power law.
    This power law can be well seen as a straight line on the log-log plot of word counts:   

    If you are still not sure whether you need Zipf's distribution or any other distribution, 
    you can compare log likelihood of your data under different distribution, or choose one 
    using Kolmogorov-Smirnov test.

    '''

    all_corpus_words = product_characteristics()[6] 
    all_words = Counter(all_corpus_words)
    
    all_words_count = Counter(all_words.values())
    word_counts = np.array(list(all_words_count.keys()))
    freq_of_word_counts = np.array(list(all_words_count.values()))
    
    n = sum(freq_of_word_counts)
    # for each word count, find the probability that a random word has such word count
    try:
        probas = word_counts ** (-s) / np.sum(np.arange(1, n+1) **(-s))
        log_likelihood = sum(np.log(probas) * word_counts)
    except:
        log_likelihood = 0.0

    return -log_likelihood
    
def min_scalar():
    
    ''' The distribution of word frequencies is often characterized by Zipf's law, 
    which states that it has Pareto distribution p(k) ~ k^-s, so-called power law.
    This power law can be well seen as a straight line on the log-log plot of word counts:   

    If you are still not sure whether you need Zipf's distribution or any other distribution, 
    you can compare log likelihood of your data under different distribution, or choose one 
    using Kolmogorov-Smirnov test.
    
    @purpose: calculates the minimized best value from neg_zipf_likelihood analysis (best line of fit)

    '''
    
    s_best = minimize_scalar(neg_zipf_likelihood, [0.1, 3.0])
    return s_best.x

def wordQualityScore():
    
    '''
    Note:
    CMA: Confusion Matrix Author is a comparison between one author review and one author of all its reviews
    CMG: Confusion Matrix General is a comparison between author reviews and the general reviews (not all reviews)
    
    @purpose: Analyze the reviews, the words used, and output the score 
    
    @output: None (database update)
    '''
    
    authorIDInfo = product_characteristics()[5]
    countTotal = product_characteristics()[4]

    V = float(modelInitiate()[1])
    bestValue = float(abs(min_scalar()))

    for mainAuthorid, value in authorIDInfo:
        
        try:
            cramerValuePercent = value / (V + 0.000000001)
        except ZeroDivisionError:
            cramerValuePercent = 0.0

        ''' Words used in corpus versus the correlation of all the words used in all the reviews'''
        
        breaker = (cramerValuePercent * bestValue + countTotal) * bestValue
        breaker = breaker / 100
        
        try:
            score = float(breaker) / float(cramerValuePercent)
        except:
            score = breaker

        if math.isnan(score) or math.isinf(score):
            score = 1.0
            
        for authorid, nvalue in authorScore.items():
            
            if cramerValuePercent >= 0.5 and mainAuthorid == authorid:
                newvalue = nvalue * (1 + (score * 0.1))
                if math.isnan(newvalue) or math.isinf(newvalue):
                    newvalue = newvalue / (nvalue * score)
                authorScore[authorid] = newvalue
            if cramerValuePercent < 0.5 and mainAuthorid == authorid:  
                newvalue = nvalue * (1 - (1 - score) * 0.1)
                if math.isnan(newvalue) or math.isinf(newvalue):
                    newvalue = newvalue / (nvalue * score)
                authorScore[authorid] = newvalue

    dataBaseUpdateScore(authorScore, tableName, scoreColumn) 