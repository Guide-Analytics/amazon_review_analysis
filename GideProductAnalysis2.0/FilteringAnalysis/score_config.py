'''
#################################################
@product: Gide Product Analysis
@filename: Score Config File

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from SeleniumAnalysis import review_config

'''
@purpose: Table Configuration Values
'''

authorTableName = review_config.tableNames()[2]
reviewTableName = review_config.tableNames()[0]

def userScore():
    
    '''
    @purpose: user score column column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'user_score'
    columnNameValue = 'user_score = 1000'
    
    return authorTableName, columnName, columnNameValue
    
def word_count_score():
    
    '''
    @purpose: word count score column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'word_count_score'
    columnNameValue = 'word_count_score = 0'
    
    return authorTableName, columnName, columnNameValue
    
def quality_word_score():
    
    '''
    @purpose: quality word score column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''

    columnName = 'quality_word_score'
    columnNameValue = 'quality_word_score = 0'
    
    return authorTableName, columnName, columnNameValue
    
def review_sentiment_score():
    
    '''
    @purpose: review sentiment score column values
    
    @outputs: reviewTableName [string], columnName [string], columnNameValue [string], authorTableName [string]
    '''
    
    columnName = 'review_sentiment_score'
    columnNameValue = 'review_sentiment_score = 0'

    return reviewTableName, columnName, columnNameValue, authorTableName


def review_score():
    
    '''
    IBM Sentiment Polarity Score
    @purpose: review polarity score values (do not get confused with review sentiment score)
    
    @outputs: reviewTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'review_score'
    columnNameValue = 'review_score = 0'
    
    return reviewTableName, columnName, columnNameValue
    
def word_reptition_score():
    
    '''
    @purpose: word repetition score column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'word_reptition_score'
    columnNameValue = 'word_reptition_score = 0'
    
    return authorTableName, columnName, columnNameValue

def word_repetition_percentage():
    
    '''
    @purpose: word repetition percentage column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'word_repetition_percentage'
    columnNameValue = 'word_repetition_percentage = 0'
    
    return authorTableName, columnName, columnNameValue
    
def verified_purchase_score():
    
    '''
    @purpose: verified purchase identifier score column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'verified_purchase_score'
    columnNameValue = 'verified_purchase_score = 0'
    
    return authorTableName, columnName, columnNameValue
    
def low_quality_score():
    
    '''
    @purpose: low quality score column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'low_quality_score'
    columnNameValue = 'low_quality_score = 0'

    return authorTableName, columnName, columnNameValue

def review_text():
    
    '''
    @purpose: review text column
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'review_text'
    columnNameValue = 'review_text = NULL'
    
    return authorTableName, columnName, columnNameValue
    
def category():
    
    '''
    @purpose: category (string) column values
    
    @outputs: authorTableName [string], columnName [string], columnNameValue [string]
    '''
    
    columnName = 'category'
    columnNameValue = "category = NULL"
    
    return authorTableName, columnName, columnNameValue

