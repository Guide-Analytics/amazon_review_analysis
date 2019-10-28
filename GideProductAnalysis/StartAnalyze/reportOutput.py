import psycopg2
import ast
import csv
import sys
import string

from Database import data_config
from SeleniumAnalysis import review_config
#from collections import Counter
from nltk import word_tokenize
from Database.data_config import author

dbname, host, port, userID, pwd = data_config.databaseHost()

authorTableName = review_config.tableNames()[2]
#authorTableName = 'author_table'

tempProdName = '16" Oscillating Stand Fan'
tempProdURL = 'https://www.amazon.ca/OPOLAR-Oscillating-Rechargeable-Batteries-Regulation/dp/B07DDFBG85/ref=cm_cr_arp_d_product_top?ie=UTF8'

'''
Report must contain the following information:

Product Name, Product URL, Date Scraped

KeyWordsReport:
-Keyword_Name (Average_Keyword_Sentences_Sentiment_Score, Confidence):
    -Sentence_1, Author_ID (Sentence_Sentiment_Score, Confidence)
 
SentimentReport:
-Review_Text, Author, Author_ID:
    -Sentiment: (Review_Sentiment_Score, Confidence)
    -Category: (Category_Number, Confidence).
    
'''

def wordQuality():
    
    ## Characteristics file: 1-Characteristics.txt
    lqFile = open("corpus_slang.txt", "r")
    lowQualityWords = lqFile.read().split(', ')
    lqFile.close()
    
    hqFile = open("1-Characteristics.txt", "r")
    highQualityWords = hqFile.read().split(', ')
    hqFile.close()
    
    return lowQualityWords, highQualityWords   

def start(productName, productURL):
    generateReport(productName, productURL)

def generateReport(productName, productURL):
    
    ratingData = {}
    
    keyWordData = []
    authorData = []
    sentimentData = []
    
    lowQualityWords, highQualityWords = wordQuality()
    conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
    cur = conn.cursor()
    
    try:
        cur.execute('''
            SELECT DISTINCT  R.author_id, R.rating, P.average_rating
            FROM review_table R
            JOIN product_table P ON P.product_id = R.product_id
            WHERE P.product_url = \''''+productURL+'''\'''')
        
        rating = cur.fetchone()
        while rating is not None:
            ratingData[rating[0]] = [int(rating[1]), float(rating[2])]
            rating = cur.fetchone()
            
        cur.execute('''
            SELECT S.keywords, S.avgkeyword_confidence_score, S.review_sentence
            FROM sentencelabelling S
        ''')
        
        keywordRow = cur.fetchone()
        while keywordRow is not None:
        
            keyWordData = keyWordReport(keywordRow, keyWordData, productURL, ratingData)
            #filteredSentences = lstOfSentencesData(lstofsentences)
            keywordRow = cur.fetchone()
            
        cur.execute('''
            SELECT DISTINCT R.rating, P.average_rating, P.product_url, A.author, 
            R.review_text, R.verified_purchase, R.review_score, R.date,  R.review_id, A.author_id
            FROM review_table R
            JOIN product_table P ON P.product_id = R.product_id
            JOIN author_table A ON A.author_id = R.author_id
        ''')
        
        sentimentRow = cur.fetchone()
        while sentimentRow is not None:
            
            sentimentData = sentimentReport(sentimentRow, sentimentData, productURL, 
                                            lowQualityWords, highQualityWords)
            sentimentRow= cur.fetchone()

        cur.execute('''
           SELECT DISTINCT A.author, A.num_of_reviews, P.product_url, R.rating, P.average_rating, 
           R.review_text, R.date, R.review_score, R.verified_purchase, A.word_repetition_percentage, R.date_scraped, 
           R.review_id, A.author_id
           FROM review_table R
           JOIN product_table P ON P.product_id = R.product_id
           JOIN author_table A ON A.author_id = R.author_id
        ''')
        
        dateScraped = []
        authorInfoRow = cur.fetchone()
        dateScraped.append(authorInfoRow[10])
        
        while authorInfoRow is not None:
            authorData = authorInfoReport(authorInfoRow, authorData, lowQualityWords)
            authorInfoRow = cur.fetchone()  
            
        if len(dateScraped) > 1:
            dateScraped = dateScraped[0]
        else:
            dateScraped = dateScraped
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Select Score Error")
        print(error)
        conn.close()
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()

    outputToCSV(keyWordData, sentimentData, authorData, productName, productURL, dateScraped)   
    
    
def authorInfoReport(authorInfoRow, authorData, lowQualityWords):
    
    author = authorInfoRow[0]
    numOfReviews = int(authorInfoRow[1])
    productURL = authorInfoRow[2]
    rating = int(authorInfoRow[3])
    averageRating = float(authorInfoRow[4])
    text = authorInfoRow[5]
    date = authorInfoRow[6]
    sentimentScore = authorInfoRow[7]
    verifiedPurchase = authorInfoRow[8]
    wordPercentage = authorInfoRow[9]

    newText = text.translate(None, string.punctuation).decode('ascii', errors = 'ignore')
    lstofsentence = word_tokenize(newText.encode('utf-8'))
 
    lowQualityWordCount = len([w for w in lowQualityWords if w in lstofsentence])
    wordCount = len(lstofsentence)

    authorData.append([author, numOfReviews, productURL, rating, averageRating, 
                       text, date, sentimentScore, wordCount, lowQualityWordCount, 
                       verifiedPurchase, wordPercentage])
    
    return authorData

def sentimentReport(sentimentRow, sentimentData, productURL, lowQualityWords, highQualityWords):
    
    produrlscraped = sentimentRow[2]
    if productURL == produrlscraped:
        
        rating = int(sentimentRow[0])
        averageRating = float(sentimentRow[1])
        
        try:   
            author = sentimentRow[3] 
            reviewText = sentimentRow[4]
            newText = reviewText.translate(None, string.punctuation).decode('ascii', errors = 'ignore')
            lstofsentence = word_tokenize(newText.encode('utf-8'))
            
            lowQualityWordCount = len([w for w in lowQualityWords if w in lstofsentence])
            highQualityWordCount = len([w for w in highQualityWords if w in lstofsentence])
            wordCount = len(lstofsentence)
        except:
            pass
        
        verifiedPurc = sentimentRow[5]
        review_date = sentimentRow[7]
        sentimentScore = sentimentRow[6]
        
        sentimentData.append([rating, averageRating, author, reviewText, review_date, 
                             verifiedPurc, highQualityWordCount, wordCount, lowQualityWordCount, sentimentScore])
    
    return sentimentData

def keyWordReport(keywordRow, keyWordData, productURL, ratingData):
    
    lstofsentences = ast.literal_eval(keywordRow[2])
    keyWordScoreLst = ast.literal_eval(keywordRow[1])
    newKeyWordData = []
            
    for sentences in lstofsentences:
        producturlscraped = sentences[4]
        
        if productURL == producturlscraped:
        
            authorID = sentences[1]
            rating = ratingData[authorID]
            author = sentences[2]
            splitScores = sentences[3].split(', ')
            text = sentences[0].encode('utf-8')
            sentimentScore = splitScores[0].strip("(")
            confidenceScore = splitScores[1].strip(")") 
            keyWordData.append([keywordRow[0].upper(), keyWordScoreLst[0], keyWordScoreLst[1], 
                            text, sentimentScore, confidenceScore, author, rating[0], rating[1], "NULL"])

    for filtered in keyWordData:
        
        if filtered not in newKeyWordData:
            newKeyWordData.append(filtered)
    
    return newKeyWordData

def lstOfSentencesData(lstofsentences):
    
    filteredSentences = []
    for dataInfo in lstofsentences:
        if dataInfo != []:
            filteredSentences.append(dataInfo)
    
    return filteredSentences


def outputToCSV(keyWordData, sentimentData, authorData, productName, productURL, dateScraped):

    productInfo = "product_info.csv"
    sentimentInfo = "sentiment_info.csv"
    authorInfo = "author_info.csv"
    
    productname = "Product Name: "+ productName
    producturl = "Product URL: "+ productURL
    datescraped = "Date Scraped: " + str(dateScraped)
    try:
        with open(productInfo, 'wb') as csvfile:
           
            sentwriter = csv.writer(csvfile)
            sentwriter.writerow(["Product Info", productname+" || "+datescraped, "", producturl])
            sentwriter.writerow(["KEYWORDS", "Keywords Sentiments Score", "Keywords Confidence Score", "Sentence", 
                                 "Sentiment Score", "Confidence Score", "Author", "Rating", "Average Rating", "Category"])
            sentwriter.writerows(keyWordData)
    except:
        print('Product Info Table Issue')
        sys.exit(5)
            
    try:
        with open(sentimentInfo, 'wb') as csvfile:
            
            sentwriter = csv.writer(csvfile)
            sentwriter.writerow(["Sentiment Info", productname+" || "+datescraped, "", producturl])   
            sentwriter.writerow(["Rating", "Average Rating", "Author", "Review Text", "Review Date", "Verified Purchase", 
                                 "# HQ Words", "Word Count", "# LQ Words", "Sentiment Score"])
            sentwriter.writerows(sentimentData)
    except:
        print("Sentiment Info Table Issue")
        sys.exit(6)
        
    with open(authorInfo, 'wb') as csvfile:
            
        sentwriter = csv.writer(csvfile)
        sentwriter.writerow(["Author Info"])
        sentwriter.writerow(["Author", "# Of Reviews", "Product URL", "Rating", "Average Rating", "Review Text", "Review Date", 
                             "Sentiment Score", "Word Count", "# LQ Words", "Verified Purchase", "Repeatability Percentage"])
        sentwriter.writerows(authorData)

    print("Report Completed. Please check " +productInfo+ " "+sentimentInfo+ " "+authorInfo)
    
    
#start("", "https://www.amazon.ca/Comfort-Zone-CZST161BTE-Pedestal-Fan/dp/B004IPA774/ref=cm_cr_arp_d_product_top?ie=UTF8")