'''
#################################################
@product: Gide Product Analysis
@filename: Write to Database  

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from data_config import tableSite
from data_config import tableExtraction
# from data_config import tablePMI

import pushDataCSV

def authorTable(author_path, author_name, dbname, host, port, userID, pwd, func):
    
    '''
    @purpose: Writing data to author_table Table in Database
    
    @inputs: author_path [string] (file path), author_name [string] (file name for table), dbname [string],
    host [string], port [int], userID [string], pwd = "" [string], func [string] (the function
    denotes whether to reset database or not)
    @outputs: None (database creation and update)
    ''' 
    tableProfile = tableSite()[1]
    pushDataCSV.csv_to_table(tableProfile, author_path, author_name, dbname, host, port, userID, pwd, func)
    
def productTable(product_path, prod_name, dbname, host, port, userID, pwd, func):
    '''
    @purpose: Writing data to product_table Table in Database
    
    @inputs: author_path [string] (file path), author_name [string] (file name for table), dbname [string],
    host [string], port [int], userID [string], pwd = "" [string], func [string] (the function
    denotes whether to reset database or not)
    @outputs: None (database creation and update)
    ''' 
    tableProduct = tableSite()[2]
    pushDataCSV.csv_to_table(tableProduct, product_path, prod_name, dbname, host, port, userID, pwd, func)
    
def reviewTable(review_path, review_name, dbname, host, port, userID, pwd, func):
    '''
    @purpose: Writing data to review_table Table in Database
    
    @inputs: author_path [string] (file path), author_name [string] (file name for table), dbname [string],
    host [string], port [int], userID [string], pwd = "" [string], func [string] (the function
    denotes whether to reset database or not)
    @outputs: None (database creation and update)
    '''  
    tableReviews = tableSite()[0]
    pushDataCSV.csv_to_table(tableReviews, review_path, review_name, dbname, host, port, userID, pwd, func)
    
def sentenceTable(spath, sname, dbname, host, port, userID, pwd, func):
    '''
    @purpose: Writing data to sentencelabelling Table in Database
    
    @inputs: author_path [string] (file path), author_name [string] (file name for table), dbname [string],
    host [string], port [int], userID [string], pwd = "" [string], func [string] (the function
    denotes whether to reset database or not)
    @outputs: None (database creation and update)
    ''' 
    tableSentences = tableExtraction()[1]
    pushDataCSV.csv_to_table(tableSentences, spath, sname, dbname, host, port, userID, pwd, func)
    
def wordsTable(wpath, wname, dbname, host, port, userID, pwd):
    '''
    @purpose: Writing data to wordslabelling Table in Database
    
    @inputs: author_path [string] (file path), author_name [string] (file name for table), dbname [string],
    host [string], port [int], userID [string], pwd = "" [string]
    @outputs: None (database creation and update)
    ''' 
    func = ''
    tableWords = tableExtraction()[0]
    pushDataCSV.csv_to_table(tableWords, wpath, wname, dbname, host, port, userID, pwd, func)