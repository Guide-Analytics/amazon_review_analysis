'''
#################################################
@product: Gide Product Analysis
@filename: Initiate Extraction (Website Scraped --> Database)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import csv
import review_input
import words_ext
import os

from Database import data_config
from Database import writeTable
from SeleniumAnalysis.automated_ext import scrape

'''
@purpose: Database Configuration Values
'''

dbname = data_config.databaseHost()[0]
host = data_config.databaseHost()[1]
port = data_config.databaseHost()[2]
userID = data_config.databaseHost()[3]
pwd = data_config.databaseHost()[4]

def initExtraction():
    
    '''
    @purpose: Start Website Scraping. Then, retrieve 
    Product Name and Product URL. 
    Then, analyze all the reviews and find the words found
    in the reviews; store them in database. 
    
    @outputs: productname [string], producturl [string]
    '''
    
    productname, producturl = scrape()
    wordsFound()
    
    return productname, producturl
    
def wordsFound():
    
    '''
    @purpose: Conduct Word Analysis and store the information in the following format:
    Product Name, Product URL, Author ID, Author Name, Words Found [list], Review Text
    
    @outputs: None (stores information to Database)
    '''
    
    reviewData = review_input.dataBase(dbname, host, port, userID, pwd)
    char_words = words_ext.wordAnalysis(reviewData)
    
    ## Create a .csv file, search the two lists: mergelst and features,
    ## and search features' words in mergelst.
    ## Output: .csv file with review_id and characteristic words found 
    wpath = 'wordsLabelling.csv'
    wname = "wordslabelling"
    #try:
    with open(wpath,'wb') as csvfile:
        sentwriter = csv.writer(csvfile)
        sentwriter.writerow(['Product', 'URL', 'AuthorID', 'Author', 'Words Found', 'Text'])     
        sentwriter.writerows(char_words)
    print("Words Detection Completed. Please check: "+wname)
    writeTable.wordsTable(wpath, wname, dbname, host, port, userID, pwd)
    os.remove(wpath)