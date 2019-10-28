'''
#################################################
@product: Gide Product Analysis
@filename: Word Repetition Analysis

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import re
import string
import copy

from initiateScore import dataBaseReviewRepeated, dataBaseSelectScore, dataBaseUpdateScore
from Database import data_config
from collections import Counter

from nltk.tokenize import word_tokenize
from autoCorrect import  probablityWord #correction
from score_config import word_reptition_score, word_repetition_percentage
from itertools import dropwhile

from statistics import median

'''
@purpose: Database Configuration Values
'''

dbname, host, port, userID, pwd = data_config.databaseHost()

'''
@purpose: Database information data/initial user score
'''

repeatedData = dataBaseReviewRepeated(dbname, host, port, userID, pwd)
authorScore = dataBaseSelectScore(dbname, host, port, userID, pwd)[0]

'''
@purpose: Table Configuration Values (Word Repeated Percentage)
'''

percentageScore = copy.deepcopy(authorScore)

'''
@purpose: Table Configuration Values
'''

authorTableName = word_reptition_score()[0]
scoreColumn = word_reptition_score()[1]

percentageColumn = word_repetition_percentage()[1]

def reptitionStart():
    
    '''
    @purpose: Starting repetition score
    '''
    
    print('Starting Word Repetition Analysis')
    reptition_count_review()
    print('Finished Word Repetition Analysis')
    
def corpus_stopwords():
    
    '''
    @purpose: Retrieve all stopwords from corpus_stopwords.txt
    
    @outputs: newStopWords [set]
    '''
    
    text = open('corpus_stopwords.txt').read()
    words = re.findall(r'\w+', text.lower())
    newStopWords = set(words)
    
    return newStopWords

def reptition_count_review():
    
    '''
    @purpose: Analyzing reviews and detect to see if any stopwords in the corpus are
    in the reveiws. Filter them before conducting repeated reviews/words analysis
    
    @outputs: None (database update)
    '''
    
    removePunct = re.compile('[%s]' % re.escape(string.punctuation))
    
    for mainAuthorID, mainReviews in repeatedData.items():
            
        filteredAuthorWords = [] ## All the reviews for the author
        reviewTextList = mainReviews[2]
        #reviewCount = float(mainReviews[0])
        averageScore = []
        
        for mainText in reviewTextList:
            
            wordCommons, wordCount = findRepetition(filteredAuthorWords, mainText, removePunct)
            
        for commonWords, countWords in wordCommons:
            countWords
            wordPercentage = probablityWord(commonWords, wordCount)
            averageScore.append(wordPercentage)
        '''
        Score Value for the Authors 
        '''         
        reviewCount = len(averageScore)
        scoreCalculation(averageScore, reviewCount, mainAuthorID)
            
    dataBaseUpdateScore(authorScore, authorTableName, scoreColumn)
    dataBaseUpdateScore(percentageScore, authorTableName, percentageColumn)
                        
def findRepetition(filteredAuthorWords, mainText, removePunct):
    
    '''
    @purpose: Finding repetition of words in the reviews for one author. Count
    the most frequently used words for one author and grab the top most used words. 
    Then, use the information to calculate scores for each author
    
    @inputs: filteredAuthorWords [list], mainText [list], removePunct [string - expression of punctuations]
    @outputs: wordCommons [Counter], wordCount [dict]
    
    '''
    
    stopWords = corpus_stopwords()
    newText = removePunct.sub('', mainText[0].lower())
    newWords = word_tokenize(newText)
                        
    for words in newWords:
        if words not in stopWords:
            
            #correctedWord = correction(words)
            filteredAuthorWords.append(words)
                
    wordCount = Counter(filteredAuthorWords)
            
    for key, count in \
        dropwhile(lambda key_count: key_count[1] > 1, wordCount.most_common()):
        count
        del wordCount[key]
                
    wordCommons = wordCount.most_common()
    
    return wordCommons, wordCount

def scoreCalculation(averageScore, reviewCount, mainAuthorID):
    
    '''
    @purpose: Finding repetition of words in the reviews for one author. Count
    the most frequently used words for one author and grab the top most used words. 
    Then, use the information to calculate scores for each author. The score
    calculation finds if any authors are repeating their reviews using the same 
    words (excluding the stop words and unnecessary words)
    
    @inputs: averageScore [dict], reviewCount [float], mainAuthorID [int]
    @outputs: None (database update)
    
    '''
    
    '''
    Repeated words count percentage over the # of the reviews
    An approximate analysis of repeated words in each review
    
    '''
    
    try:
        scoreValue = float(sum(averageScore)) / reviewCount
        medianScore = median(averageScore)
    except: 
        scoreValue = 0.0
        medianScore = 0.0
    
    value = authorScore[mainAuthorID]
    
    if scoreValue >= 0.3:
        authorScore[mainAuthorID] = value *  (1 - (1 - scoreValue) * 0.1)
        percentageScore[mainAuthorID] = scoreValue
        
    elif scoreValue < 0.3 and scoreValue >= 0.1 and medianScore >= 0.5:
        authorScore[mainAuthorID] = value *  (1 - (1 - scoreValue) * 0.1)
        percentageScore[mainAuthorID] = scoreValue
        
    elif scoreValue < 0.3 and scoreValue >= 0.1 and medianScore < 0.5:
        authorScore[mainAuthorID] = value * (1 + (scoreValue * 0.1))
        percentageScore[mainAuthorID] = scoreValue
        
    elif scoreValue < 0.1:
        authorScore[mainAuthorID] = value * (1 + (scoreValue * 0.1))
        percentageScore[mainAuthorID] = scoreValue
