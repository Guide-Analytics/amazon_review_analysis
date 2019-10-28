'''
#################################################
@product: Gide Product Analysis
@filename: Review Input (Database --> Database WordLabelling)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import psycopg2
import sys
import string

from nltk.tokenize import sent_tokenize

rev_id = 0
rev_text = 1
date = 2
prod_name = 3
prod_url = 4
author = 5
authorid = 6

def dataBase(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting information from database for review analysis. Contains:
    distinct review ID, review Text, review Date, product Name, product URL, author Name,
    author ID from three tables (review_table, product_table, author_table)
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd [string]
    @outputs: reviewData [list of review information]
    '''
    
    conn = None
    reviewData = []
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT DISTINCT R.review_id, R.review_text, R.date, 
            P.product, P.product_url, A.author, A.author_id
            FROM review_table R
            JOIN product_table P ON P.product_id = R.product_id
            JOIN author_table A ON A.author_id = R.author_id ''')

        row = cur.fetchone()
        while row is not None:
            reviewData.append(row)
            row = cur.fetchone()
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()
    
    return reviewData

def inputRev(reviewData):  
    
    '''
    @purpose: Generate a list of reviews containing:
    the author name, sentence tokenized to words, product name, product URL, and 
    author ID
    
    @inputs: reviewData [list of review information] from Database
    @outputs: reviewList [list of review information] to word analysis
    '''
    
    reviewList = []
    
    for r in reviewData:
        
        amazonCustomer = 'Amazon Customer ' + str(r[date]) ## Amazon Customer + date
        productName = r[prod_name] ## product Name
        url = r[prod_url] ## URL of product
        author_id = r[authorid]

        try:
            sentence = r[rev_text].translate(None, string.punctuation).decode('utf-8')
            sentence = sentence.encode('ascii', errors='ignore')
        except AttributeError:
            sentence = ""

        token_sent = sent_tokenize(sentence) ## Review text   

        if r[author] == "Amazon Customer": ## R[2] == AUTHOR
            reviewList.append([amazonCustomer, token_sent, productName, url, author_id])
        else:
            reviewList.append([r[author], token_sent, productName, url, author_id])
            
    return reviewList

def charact():
    
    '''
    @purpose: read corpus file: 1-Characteristics.txt. contains the necessary/important
    words for word analysis
    
    @outputs: lines [list of characteristic words]
    '''
    ## Characteristics file: 1-Characteristics.txt
    text_file = open("1-Characteristics.txt", "r")
    lines = text_file.read().split(', ')
    text_file.close()
    
    return lines    