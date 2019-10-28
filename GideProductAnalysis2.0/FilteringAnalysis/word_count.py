'''
#################################################
@product: Gide Product Analysis
@filename: Word Count Analysis

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import numpy as np
import matplotlib.pyplot as plt
import string

from collections import Counter
from scipy.optimize import minimize_scalar
from Database import data_config
from initiateScore import dataBaseSelectScore, dataBaseUpdateScore, dataBaseWordCount
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from score_config import word_count_score

dbname = data_config.databaseHost()[0]
host = data_config.databaseHost()[1]
port = data_config.databaseHost()[2]
userID = data_config.databaseHost()[3]
pwd = data_config.databaseHost()[4]

reviewData = dataBaseWordCount(dbname, host, port, userID, pwd)
authorScore = dataBaseSelectScore(dbname, host, port, userID, pwd)[0]
stop_words = set(stopwords.words('english'))

tableName = word_count_score()[0]
scoreColumn = word_count_score()[1]

def wordCountStart():
    print('Starting Word Count Analysis')
    word_count_reviews()
    print('Finished Word Count Analysis')
    
def reviewAnalyze():
    
    '''
    @purpose: Calculating percentage of individual reviews and the 
    filtered reviews (removing the stop words) percentage (filtered count / total count) 
    
    @inputs: indiv_review [list of words], filtered_reviews [list of words]
    @outputs: indiv_percentage [float]
    
    '''
    
    countDict = {}
    filtered_all_reviews = []
    all_reviews = []
    
    for reviews in reviewData:
        
        review_id = reviews[0]
        author_id = int(reviews[1])
        
        ## count = len(re.findall(r'\w+', indiv_reviews))
        ## Removes punctuations
        user_reviews = reviews[3].translate(None, string.punctuation)
        word_tokens = word_tokenize(user_reviews.lower())
        indiv_reviews = word_tokens
        
        ## Filter unnecessary words from the sentence
        #filtered_reviews = [w for w in word_tokens if not w in stop_words] 
        filtered_reviews = [] 
  
        for w in word_tokens: 
            if w not in stop_words: 
                filtered_reviews.append(w.lower())
        
        ## Tokenize the words into list of words
        all_reviews.extend(indiv_reviews)
        filtered_all_reviews.extend(filtered_reviews)
        
        ## Percentage Individual Count
        indiv_percentage = calculate(indiv_reviews, filtered_reviews)
        
        countDict[review_id] = [author_id, indiv_percentage]
    
    arc = float(len(all_reviews))
    farc = float(len(filtered_all_reviews))
    countTotal = calculateTotal(arc, farc)
    return countTotal, countDict, filtered_all_reviews, all_reviews
    ''' 
    Remove all punctuations and "most frequent used words?" in English dictionary.
    Then, count how many words each review is given. 
    '''

def calculate(indiv_reviews, filtered_reviews):
    
    '''
    @purpose: Calculating percentage of individual reviews and the 
    filtered reviews (removing the stop words) percentage (filtered count / total count) 
    
    @inputs: indiv_review [list of words], filtered_reviews [list of words]
    @outputs: indiv_percentage [float]
    
    '''
    
    indiv_count = float(len(indiv_reviews))
    filtered_indiv_count = float(len(filtered_reviews))
    indiv_percentage = filtered_indiv_count/indiv_count
        
    return indiv_percentage


def calculateTotal(arc, farc):
    
    '''
    @purpose: Calculating percentage of all reviews and all the 
    filtered reviews (removing the stop words) percentage (filtered count / total count) 
    
    @inputs: arc [list of words], farc [list of words]
    @outputs: total_percentage [float]
    
    '''
    
    total_percentage = farc/arc
    return total_percentage

def plot(freq_of_word_counts, word_counts):
    
    '''
    @purpose: Testing purposes. Plots the neg_zipf_likelihood distribution
    
    '''
    plt.scatter(np.log(word_counts), np.log(freq_of_word_counts))
    plt.xlabel('Log of word frequency')
    plt.ylabel('Log of number of such words')
    plt.title('Power law for word frequencies')
    plt.show()

def neg_zipf_likelihood(s):
    
    ''' The distribution of word frequencies is often characterized by Zipf's law, 
    which states that it has Pareto distribution p(k) ~ k^-s, so-called power law.
    This power law can be well seen as a straight line on the log-log plot of word counts:   

    If you are still not sure whether you need Zipf's distribution or any other distribution, 
    you can compare log likelihood of your data under different distribution, or choose one 
    using Kolmogorov-Smirnov test.

    '''
    
    all_reviews = reviewAnalyze()[3]
    all_words = Counter(all_reviews)
    all_words_count = Counter(all_words.values())
    word_counts = np.array(list(all_words_count.keys()))
    freq_of_word_counts = np.array(list(all_words_count.values()))
    
    n = sum(freq_of_word_counts)
    #plot(freq_of_word_counts, word_counts)
    # for each word count, find the probability that a random word has such word count
    probas = word_counts ** (-s) / np.sum(np.arange(1, n+1) **(-s))
    log_likelihood = sum(np.log(probas) * word_counts)
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

def word_count_reviews():
    best_percentage = min_scalar()

    countTotal = reviewAnalyze()[0]
    countList = reviewAnalyze()[1]
    
    for rev_id, id_value  in countList.items():
        rev_id
        author_id = id_value[0]
        scoreValue = id_value[1]
        breaker = (scoreValue * best_percentage + countTotal) * best_percentage
        
        deduct = abs(best_percentage - breaker)
        
        '''authors is author_id
        score is the authorScore '''
        for mainAuthorid, value in authorScore.items():
            score = 0
            score = value
            newScore = score - (score * deduct**2)
            if breaker < best_percentage and author_id == mainAuthorid:
                authorScore[mainAuthorid] = newScore
            elif breaker > 1 and author_id == mainAuthorid:
                authorScore[mainAuthorid] = newScore        
                
    dataBaseUpdateScore(authorScore, tableName, scoreColumn)