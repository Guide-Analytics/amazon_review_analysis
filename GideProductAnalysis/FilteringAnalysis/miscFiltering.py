'''
#################################################
@product: Gide Product Analysis
@filename: Misc. Analysis: Low Word Quality Count, Verified Purchase

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from initiateScore import dataBaseReviewMisc, dataBaseSelectScore, dataBaseUpdateScore
from Database import data_config
from itertools import product
from nltk.tokenize import word_tokenize
from collections import Counter
import string
from score_config import low_quality_score, verified_purchase_score

dbname, host, port, userID, pwd = data_config.databaseHost()
miscData = dataBaseReviewMisc(dbname, host, port, userID, pwd)


lqsTableName = low_quality_score()[0]
lqsScoreColumn = low_quality_score()[1]

vpsTableName = verified_purchase_score()[0]
vpsScoreColumn = verified_purchase_score()[1]

def miscStart():
    
    '''
    @purpose: Starting lowQualityCount and verifiedPurchase Analysis 
    and Score Calculation
    
    '''
    
    print('Starting Low Quality Word Analysis')
    lowQualityCount()
    print('Finished Low Quality Word Analysis')
    
    print('Starting Verified Purchase Count Analysis')
    verifiedPurchase()
    print('Finished Verified Purchase Count Analysis')
    
def numberOfReviews():
    
    '''
    @purpose: Starting number of reviews analysis
    (Currently obselete)
    
    '''
    
    authorScore = dataBaseSelectScore(dbname, host, port, userID, pwd)[0]
    
    for mainAuthorID, data in miscData.items():
        
        reviewCount = data[0]
        value = authorScore[mainAuthorID]
        
        if reviewCount < 5: ## reviews are less than 5
            authorScore[mainAuthorID] = value * (reviewCount * 0.95)
    
def lowQualityCount():
    
    '''
    @purpose: Starting low quality word count analysis and score
    calculation 
    
    @outputs: None (database score update)

    '''
    
    authorScore = dataBaseSelectScore(dbname, host, port, userID, pwd)[0]
    
    text_file = open("corpus_slang.txt", "r")
    slangCorpus = text_file.read().split(', ')
    text_file.close()

    for mainAuthorID, data in miscData.items():
        
        reviewText = data[2]
        value = authorScore[mainAuthorID]

        for slangWord, text in product(slangCorpus, reviewText):
            
            newText = text.translate(None, string.punctuation).decode('ascii', errors = 'ignore')
            newWords = word_tokenize(newText.encode('utf-8'))
            
            if slangWord in newWords:
                
                '''
                If the words in the corpus_slang.txt are in the reviews, start 
                counting the words using Counter. 
                '''
                
                countWords = Counter(newWords)
                N = sum(countWords.values())
                slangPercent = float(countWords[slangWord]) / N
                
                score = (1 - slangPercent)
                authorScore[mainAuthorID] = value * score
    
    dataBaseUpdateScore(authorScore, lqsTableName, lqsScoreColumn)
                
def verifiedPurchase():
    
    '''
    @purpose: Starting verified purchases analysis and score 
    calculation 
    
    @outputs: None (database score update)
    
    '''
    
    authorScore = dataBaseSelectScore(dbname, host, port, userID, pwd)[0]
    
    for mainAuthorID, data in miscData.items():
        
        verifiedPurchaseLst = data[1]
        reviewCount = data[0]
        value = authorScore[mainAuthorID]
        
        positiveCount = verifiedPurchaseLst.count("Yes") ## count the # of Yes (verified purchases)
        positivePercent = float(positiveCount) / reviewCount
        negativePercent = (1 - positivePercent)
        
        if negativePercent < 0.5: ## if there are less than 50% verified purchases, scores deduct
            
            score = (positivePercent - negativePercent)
            authorScore[mainAuthorID] = value * (1 + score)
            
        if negativePercent >= 0.0 and negativePercent > positivePercent:
            
            score = (negativePercent - positivePercent)
            authorScore[mainAuthorID] = value * (1 - score)
            
    dataBaseUpdateScore(authorScore, vpsTableName, vpsScoreColumn)             