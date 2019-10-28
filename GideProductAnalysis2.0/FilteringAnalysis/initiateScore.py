'''
#################################################
@product: Gide Product Analysis
@filename: Filtering Analysis: Scores Update

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from Database import data_config, writeTable
from score_config import review_sentiment_score
    
import csv
import sys
import psycopg2
import os

'''
@purpose: Database Configuration Values
'''

dbname = data_config.databaseHost()[0]
host = data_config.databaseHost()[1]
port = data_config.databaseHost()[2]
userID = data_config.databaseHost()[3]
pwd = data_config.databaseHost()[4]


'''
@purpose: Table Configuration Values
'''

reviewTableName = review_sentiment_score()[0]
authorTableName = review_sentiment_score()[3]

## Generate Score: Max score 
def generateUserScore(tableName, scoreColumn, scoreColumnValue, reset):
        
    '''
    @purpose: Generate User Score: Word Count Score, Quality Word Usage Score, etc.
    Create scores in tables and create headers for columns, then create initial score values.
    Reset score table whenever new data have been scraped from websites. 
    
    @inputs: tableName (author_table, review_table, product_table) [string], scoreColumn [string],
    scoreColumnValue [string], reset [string]
    @outputs: None (database output)
    '''
    
    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        
        cur.execute('''
        select exists(
        select * from information_schema.columns 
        where table_name = \'''' +tableName+ '''\' AND column_name = \'''' +scoreColumn+ '''\')''')
        
        if (cur.fetchone()[0]):
            if reset.lower() == 'y' or reset.lower() == 'yes':
                print(True)
                cur.execute('''
                UPDATE '''+tableName+ ''' SET ''' 
                +scoreColumnValue+ ''' WHERE '''
                +scoreColumn+''' IS NOT NULL
                ''')
        else:
            cur.execute('''
            ALTER TABLE ''' +tableName+ ''' ADD 
            COLUMN '''+scoreColumn+ ''' DECIMAL
            ''')
            cur.execute('''
            UPDATE '''+tableName+ ''' SET '''
            +scoreColumnValue+ ''' WHERE '''
            +scoreColumn+''' IS NULL
            ''')
        cur.execute("commit;")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Generate Score Error")
        print(error)
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            
def generateCategory(tableName, scoreColumn, scoreColumnValue, reset):
    
    '''
    @purpose: Generate Category Column: Category
    Create category values = NULL in tables and create header called Category. 
    Reset Category values whenever new data have been scraped from sites.
    
    @inputs: tableName (author_table, review_table, product_table) [string], scoreColumn [string],
    scoreColumnValue [string], reset [string]
    @outputs: None (database output)
    '''
        
    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        
        cur.execute('''
        select exists(
        select * from information_schema.columns 
        where table_name = \'''' +tableName+ '''\' AND column_name = \'''' +scoreColumn+ '''\')''')
        
        if (cur.fetchone()[0]):
            if reset.lower() == 'y' or reset.lower() == 'yes':
                cur.execute('''
                UPDATE '''+tableName+ ''' SET ''' 
                +scoreColumnValue+ ''' WHERE '''
                +scoreColumn+''' IS NOT NULL
                ''')
        else:
            cur.execute('''
            ALTER TABLE ''' +tableName+ ''' ADD 
            COLUMN '''+scoreColumn+ ''' TEXT
            ''')
            cur.execute('''
            UPDATE '''+tableName+ ''' SET '''
            +scoreColumnValue+ ''' WHERE '''
            +scoreColumn+''' IS NULL
            ''')
            
        cur.execute("commit;")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Generating Category Error")
        print(error)
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            
## SentenceLabelling Update (will write to CSV for simplicity)
def dataBaseSentenceLabellingUpdate(sentScore, keyScore):
    
    '''
    @purpose: Generate sentences with keywords from reviews to database.
    The column consists of keywords, keywords average/confidence score, and
    sentences containing the keyword characteristics containing the URL, author, sentence
    and the sentence sentiment/confidence scores
   
    @inputs: sentScore [dict], keyScore [dict]
    @outputs: None (database output)
    '''
    
    spath = 'sentenceLabelling.csv'
    sname = "sentencelabelling"
    
    combinedList = []
    for sentKey, sentValue in sentScore.items():
        for wordKey, wordValue in keyScore.items():
            if sentKey == wordKey:
                combinedList.append([sentKey, wordValue, sentValue])
    try:
        with open(spath,'wb') as csvfile:
            sentwriter = csv.writer(csvfile)
            sentwriter.writerow(['Keywords', 'Average/Confidence Score','Sentence Containing Characteristics'])     
            sentwriter.writerows(combinedList)
        print("Sentences Detection Completed. Please check " +sname)
        writeTable.sentenceTable(spath, sname, dbname, host, port, userID, pwd, 'w')
        os.remove(spath)
    except:
        print("File not found")
        sys.exit(2)

## Score Update
def dataBaseUpdateScore(authorScore, tableName, scoreColumn):
    
    '''
    @purpose: Update scores from database column - user_score, by using the
    given rules and updated to authorScore. Then, using authorScore values to update 
    the  scores in author_table table. 
    
    @inputs: authorScore [dict], tableName [string], scoreColumn[string]
    @outputs: None (database output)
    '''
    
    conn = None
    rows = zip(authorScore.keys(), authorScore.values())
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        
        if tableName == reviewTableName and scoreColumn == 'review_score':
            cur.executemany('''
              UPDATE '''+tableName+''' SET '''
              +scoreColumn+ '''= review.'''+scoreColumn+''' FROM 
              (VALUES (%s, %s)) AS review (review_id, '''+scoreColumn+''')
              WHERE '''+tableName+'''.review_id = review.review_id
              ''', rows)
    
        else:
            cur.executemany('''
              UPDATE '''+tableName+''' SET '''
              +scoreColumn+ '''= author.'''+scoreColumn+''' FROM 
              (VALUES (%s, %s)) AS author (author_id, '''+scoreColumn+''')
              WHERE '''+tableName+'''.author_id = author.author_id
              ''', rows)
        cur.execute("commit;")
        cur.close()    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Update Score Error")
        print(error)
        sys.exit(3)
    finally:
        if conn is not None:
            conn.close()
            
## Score Select
def dataBaseSelectScore(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting initial scores from user_score and update them to 
    the two tables: author_table, review_table to calculate new user scores
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd = NULL [string]
    @outputs: userScore [dict], reviewScore [dict]
    '''

    conn = None
    userScore = {}
    reviewScore = {}
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT A.author_id, A.user_score 
            FROM author_table A''')
        row = cur.fetchone()
        while row is not None:
            userScore[int(row[0])] = int(row[1])
            row = cur.fetchone()
            
        cur.execute(''' 
            SELECT R.review_id, R.review_score
            FROM review_table R''')
        row = cur.fetchone()
        while row is not None:
            reviewScore[row[0]] = float(row[1])
            row = cur.fetchone()
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Select Score Error")
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()
    return userScore, reviewScore

## Rule 1: Word Count
def dataBaseWordCount(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting review_id (unique IDs), author_id (IDs for authors), author, review_text
    (texts) from review_table to analyze the word count for each reviews and analyze  them
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd = NULL [string]
    @outputs: reviewData [list]
    '''
    
    conn = None
    reviewData = []
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT R.review_id, R.author_id, A.author, R.review_text
            FROM review_table R
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

## Rule 2: High-quality word usage (product characteristic list)
def dataBaseWordsLabelling(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting author_ID (IDs for authors), author, words_found (list of words found in review), 
    review_text (review texts) from words labelling table to analyze the quality of words use for each author
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd = NULL [string]
    @outputs: wordsData [list]
    '''
    
    
    #generateUserScore(authorScore)
    conn = None
    wordsData = []
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT W.author_id, W.author, W.words_found, W.review_text
            FROM wordslabelling W''')
     
        row = cur.fetchone()
        while row is not None:
            corpus_words = row[2][1:-1].replace("\'", "").split(", ")
            review_lst = list(set(row[3][1:-1].replace("\'", "").split(", ")))[0]
            wordsData.append([int(row[0]), row[1], corpus_words, review_lst])
            
            row = cur.fetchone()
            
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Words Labelling Error")
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()
    return wordsData

## Beta Rule 2: High-quality word usage (product characteristic list)
def dataBaseBetaWL(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting author_ID (IDs for authors), author, words_found (list of words found in review), 
    review_text (review texts) from words labelling table to analyze the quality of words use for each author
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd = NULL [string]
    @outputs: wordsData [list]
    '''
    
    #generateUserScore(authorScore)
    conn = None
    wordsData = {}
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT W.author_id, W.author, array_agg(W.words_found), array_agg(W.review_text)
            FROM wordslabelling W
            GROUP BY W.author_id, W.author''')
     
        row = cur.fetchone()
        while row is not None:
            corpus_words = row[2]
            review_lst = row[3]
            wordsData[int(row[0])] = [row[1], corpus_words, review_lst]
            
            row = cur.fetchone()
            
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Words Labelling Error")
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()
    return wordsData

## Rule 3 and 4: Review Sentiment and Repeated Words
def dataBaseReviewRepeated(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting author_ID (IDs for authors), count # of review_text (total # of reviews), 
    rank (rank of the author), list of review_text, review_id, product_url (a list of list containing the text, unique ID, 
    and the product URL). Then, we use this information to analyze sentiment/confidence and we check
    if any reviews/words are repeated.
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd = NULL [string]
    @outputs: reviewData [list]
    '''
    
    conn = None
    reviewData = {}
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT R.author_id, COUNT(R.review_text), AVG(A.rank), 
            json_agg(json_build_array(R.review_text, R.review_id, P.product_url)) AS reviews 
            FROM review_table R
            JOIN author_table A ON A.author_id = R.author_id
            JOIN product_table P ON P.product_id = R.product_id
            GROUP BY R.author_id
            ORDER BY COUNT desc''')
     
        row = cur.fetchone()
        while row is not None:
            reviewData[int(row[0])] = [float(row[1]), float(row[2]), row[3]]
            row = cur.fetchone()  
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database ReviewSentiment and ReviewRepeated Error")
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()
    return reviewData


## Rule 5-7: Misc Rules for Review Count, Word Quality Check, Verified Purchaser
def dataBaseReviewMisc(dbname, host, port, userID, pwd):
    
    '''
    @purpose: Selecting author_id (ID for authors), count # of review_text (total # of reviews), 
    a list of reviews that are or are not verified purchases, and a list of review_text for
    the one author. Then, we use this information to analyze the number of low quality words used
    and identify if the reviews are or are not verified purchases
    
    @inputs: dbname [string], host [int], port [int], userID [string], pwd = NULL [string]
    @outputs: miscData [list]
    '''
    
    conn = None
    miscData = {}

    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        cur.execute('''
            SELECT R.author_id, COUNT(R.review_text), array_agg(R.verified_purchase), array_agg(R.review_text)
            FROM review_table R
            JOIN author_table A ON A.author_id = R.author_id
            GROUP BY R.author_id
            ORDER BY COUNT desc''')
     
        row = cur.fetchone()
        while row is not None:
            miscData[int(row[0])] = [row[1], row[2], row[3]]
            row = cur.fetchone()  
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Review Misc Error")
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()
    return miscData
