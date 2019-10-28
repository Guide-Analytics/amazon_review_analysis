'''
#################################################
@product: Gide Product Analysis
@filename: Data Configurations

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from SeleniumAnalysis import review_config

keywords = "keywords"
review_sent = "review_sentence"
avgKeywordScore = "avgkeyword_confidence_score"

product = "product"
product_url = "product_url"
author = "author"
words_found = "words_found"
author_id = "author_id"
review_text = "review_text"

user_score = "user_score"
sentence_score = "sentence_confidence_score"

def databaseHost():
    
    '''
    @purpose: Database host protocols 
    
    @outputs: dbname [string], host [int], port [int], 
    userID [string], pwd = "" [string]
    '''
    
    dbname = 'postgres'
    host = 'localhost'
    port = '5432'
    userID = 'postgres'
    pwd = ''
    
    return dbname, host, port, userID, pwd

def tableSite():
    
    '''
    @purpose: Column Values (headers) for the database where tables are created
    using these column values (author_table, product_table, review_table)
    
    @outputs: tableReview [big string], tableProfile [big string], 
    tableProduct [big string]
    '''
    tableReview = review_config.tableHeader()[0]
    tableProfile = review_config.tableHeader()[1]
    tableProduct = review_config.tableHeader()[2]
    
    return tableReview, tableProfile, tableProduct

def tableExtraction():
    
    '''
    @purpose: Column Values (headers) for the database where tables are created
    using these column values (wordslabelling, sentencelabelling)
    
    @outputs: tableWords [string], tableSentences [string]
    '''
    
    tableWords = '''('''+product+ ''' text NULL, 
    '''+product_url+''' text NULL, 
    '''+author_id+''' BIGINT NOT NULL,
    '''+author+''' VARCHAR(255) NULL, 
    '''+words_found+''' text NULL, 
    '''+review_text+''' text NULL,
    FOREIGN KEY (author_id) REFERENCES author_table (author_id)); '''
    
    tableSentences = '''('''+keywords+ ''' VARCHAR(255) NULL, 
    '''+avgKeywordScore+''' text NULL, 
    '''+review_sent+''' text NULL); '''
    return tableWords, tableSentences

def tableScore():
    
    '''
    @purpose: Column Values (headers) for the database where tables are created
    using these column values (user_score)
    
    @outputs: authorScore [string]
    '''
    
    authorScore = '''('''+author_id+ ''' BIGINT PRIMARY KEY NOT NULL, 
    ''' +author+ ''' VARCHAR(255) NULL, 
    '''+user_score+''' NUMERIC NULL); '''
    return authorScore

def tableKeyWords():
    
    '''
    @purpose: Column Values (headers) for the database where tables are created
    using these column values (OLD Sentencing Labelling)
    
    @outputs: tableKey [string]
    '''
    
    tableKey = '''('''+keywords+ ''' VARCHAR(255) NULL,
    '''+avgKeywordScore+ '''VARCHAR(255) NULL,
    '''+review_sent+ ''' VARCHAR(255) NULL,
    '''+author+ ''' VARCHAR(255) NULL,
    '''+author_id+''' BIGINT NOT NULL,
    '''+sentence_score+''' VARCHAR(255) NULL; '''
    
    return tableKey