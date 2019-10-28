'''
#################################################
@product: Gide Product Analysis
@filename: Filtering Analysis: Initiate

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from score_config \
    import userScore, word_count_score, quality_word_score, \
    review_sentiment_score, word_reptition_score, \
    low_quality_score, verified_purchase_score, category, \
    review_score, review_text, word_repetition_percentage

from Database import data_config

import psycopg2
import sys

'''
@purpose: Database Configuration Values
'''

dbname = data_config.databaseHost()[0]
host = data_config.databaseHost()[1]
port = data_config.databaseHost()[2]
userID = data_config.databaseHost()[3]

'''
@purpose: Score Configuration Values
'''

userName, userColumn, userValue = userScore() ## Initial Score (base parameter 1000)
wordName, wordColumn, wordValue = word_count_score() ## Word Count Score
qualityName, qualityColumn, qualityValue = quality_word_score() ## Quality Word Usage Score
sentimentName, sentimentColumn, sentimentValue, authorSentName = review_sentiment_score() ## Review Sentiment Score (goes to Author and Review Tables)
repeatedName, repeatedColumn, repeatedValue = word_reptition_score() ## Word Repetition Score
repeatedPercentName, repeatedPercentColumn, repeatedPercentValue = word_repetition_percentage() ## Percentage of Reviews Repeated

reviewName, reviewColumn, reviewValue = review_score() ## Review Sentiment Magnitude/Polarity Score (goes to Review Table)
lqsTableName, lqsScoreColumn, lqsScoreColumnValue = low_quality_score() ## Low Quality Score
vpsTableName, vpsScoreColumn, vpsScoreColumnValue = verified_purchase_score() ## Verified Purchase Detection Score

categoryName, categoryColumn, categoryColumnValue = category() ## Category (for Machine Learning Categorization)
reviewTextName, reviewTextColumn, reviewTextValue = review_text() ## Review Text (goes to Author Table)

def filteringAnalysis(trigger):
    
    '''
    @purpose: Generate new columns for scores, text, and percentage values.
    Then, there are six rules that are conducted in analyzing the reviews:
    Word Count, Quality Words Usage, Review Sentiment, Repeated Reviews, Low Quality Words Usage, and Verified Purchase Detection.
    
    After that, a list of review texts will be generated for each author in the Author Table and a CSV file generated for Machine Learning. 
    
    @inputs: trigger [string] 
    @outputs: None (will generate scores in the database, and output a CSV file for Machine Learning purposes.) 
    '''

    from initiateScore import generateUserScore, generateCategory
    
    generateUserScore(userName, userColumn, userValue, trigger) ## Initial Score (base parameter 1000)
    generateUserScore(wordName, wordColumn, wordValue, trigger) ## Word Count Score
    generateUserScore(qualityName, qualityColumn, qualityValue, trigger) ## Quality Word Usage Score
    
    generateUserScore(reviewName, reviewColumn, reviewValue, trigger) ## Review Sentiment Magnitude/Polarity Score (goes to Review Table)
    generateUserScore(sentimentName, sentimentColumn, sentimentValue, trigger) ## Review Sentiment Score (goes to Review Table)
    generateUserScore(authorSentName, sentimentColumn, sentimentValue, trigger) ## Review Sentiment Score (goes to Author Table)
   
    generateUserScore(repeatedName, repeatedColumn, repeatedValue, trigger) ## Word Repetition Score
    generateUserScore(repeatedPercentName, repeatedPercentColumn, repeatedPercentValue, trigger) ## Percentage of Reviews Repeated
    generateUserScore(lqsTableName, lqsScoreColumn, lqsScoreColumnValue, trigger) ## Low Quality Score
    generateUserScore(vpsTableName, vpsScoreColumn, vpsScoreColumnValue, trigger) ## Verified Purchase Detection Score
    
    generateCategory(reviewTextName, reviewTextColumn, reviewTextValue, trigger) ## Review Text (goes to Author Table)
    
    from word_count import wordCountStart
    from quality_word_usage import qualityWordUsageStart
    from initiateSentiment import reviewSentiment
    from word_reptition import reptitionStart
    from miscFiltering import miscStart
    
    wordCountStart() # Word Count Rule
    qualityWordUsageStart() ## Quality Word Usage Rule
    try:
        reviewSentiment() ## Review Sentiment Rule
    except:
        print("IBM Use Limit Reached")
        pass
    reptitionStart() ## Word/Review Repetition Rule
    miscStart() ## Low Quality Word Usage and Verified Purchase Rule
    
    generateCategory(categoryName, categoryColumn, categoryColumnValue, trigger)
    CSVOutput()

## CSV Output for ML training:
def CSVOutput():
    
    '''
    @purpose: Automatically generate CSV Report for Machine Learning training 
    
    @inputs: None
    @outputs: None
    '''
    
    conn = None

    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        cur = conn.cursor()
        sql = "COPY (SELECT * FROM author_table) TO STDOUT WITH CSV HEADER DELIMITER ';' "
        with open("dataset_train.csv", "w") as csvfile:
            cur.copy_expert(sql, csvfile)  

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(2)
    finally:
        if conn is not None:
            conn.close()