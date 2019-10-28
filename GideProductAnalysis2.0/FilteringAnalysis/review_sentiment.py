'''
#################################################
@product: Gide Product Analysis
@filename: Review Sentiment Analysis

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import json
import ast
import numpy as np
import math
import warnings

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, KeywordsOptions #, EmotionOptions

from initiateScore \
    import dataBaseReviewRepeated, dataBaseSelectScore, \
    dataBaseUpdateScore, dataBaseSentenceLabellingUpdate

from Database import data_config
from reviewClassifier import NaturalLanguageClassifier

from nltk.tokenize import sent_tokenize
from scipy import stats
from score_config import review_sentiment_score, review_score, review_text

'''
@purpose: Database Configuration Values
'''

dbname, host, port, userID, pwd = data_config.databaseHost()

reviewData = dataBaseReviewRepeated(dbname, host, port, userID, pwd)
authorScore, sentimentValueScore = dataBaseSelectScore(dbname, host, port, userID, pwd)

'''
@purpose: Table Configuration Values
'''

tableName1 = review_sentiment_score()[0]
scoreColumn1 = review_sentiment_score()[1]
tableName2 = review_sentiment_score()[3]
scoreColumn2 = review_score()[1]

'''Author table tablename for text'''
tableName3 = review_text()[0]
scoreColumn3 = review_text()[1]

class NaturalLanguageToneAnalysis:
    
    '''
    @purpose: Natural Language Analysis: Tone/Polarity Score 
    
    @parameter: -1 to 1 (-1 negative, 0 neutral, 1 positive)
    
    @methods:
    
    apiUsed, watsonDeveloperInit, calculateSentimentScore, updateAuthorText, 
    NLPScoreCalculation, NLPScore
    
    @classInputs: api_init, apikey, classapikey, workspace_id, trigger
    API identifier: api_init [string], API key: classapi_key [string] for determining confidence/relvance
    score, API workspace ID: workspace_id [string] to start Watson Classifier, and the information trigger [string]
    to analyze sentence's sentiment/confidence scores

    '''
    
    allReviewScore = {}
    
    def __init__(self, api_init, apikey, classapikey, workspace_id, trigger):
        self.api_init = api_init
        self.apikey = apikey
        self.classapikey = classapikey
        self.workspace_id = workspace_id
        self.trigger = trigger
        self.apiUsed()
    
    def apiUsed(self):
        
        '''
        @purpose: Picking the right API for Review Sentiment: IBM or Google
        Currently, only IBM work
        '''
        
        if "ibm" in self.api_init.lower():
            self.watsonDeveloperInit()
        elif "google" in self.api_init.lower():
            self.google_developer_init()
            
    def watsonDeveloperInit(self):
        
        '''
        @purpose: Starting Watson Toolkit (Review sentiment Analysis)
        
        @outputs: Score update on database and create new table for sentence labelling featuring
        keywords, keywords sentiment/confidence score, and sentences info (author, product URL, product, etc.) 
        in a new table
        '''
        
        print("Starting Review Sentiment Analysis")
        iam_apikey = self.apikey
        
        naturalLanguageUnderstanding = NaturalLanguageUnderstandingV1(
            version = '2018-09-21',
            iam_apikey = iam_apikey)
        
        '''
        Local declaration: Author Score, Regression Score, Author Text
        '''
        totalAuthorValue = []
        totalRegressionValue = []
        allAuthorText = {}
        
        updatedAllAuthorText = self.updateAuthorText(allAuthorText, reviewData)
        
        '''
        KeyWord Scores, Sentence Scores for the KeyWords, and keyWords Counter
        '''
        sentenceClassif = NaturalLanguageClassifier(None, None, None, None, None, None, None)
        keyWordsScoreLst, sentencesScoreLst, keyWordCounter = sentenceClassif.keyWordBuild()
        
        for mainAuthorID, mainReviews in reviewData.items():
            
            authorValue = []
            regressionValue = []
            reviewTextList = mainReviews[2]

            for mainText in reviewTextList:
                
                text = mainText[0]
                mainReviewID = mainText[1]
                productURL = mainText[2]

                print("Analyzing sentence for: " +str(mainAuthorID))
                sentenceScore = [] ## sentence Sentiment Score
                regressionScore = [] ## regression Score (using relevance/confidence scores)
                sentences = text.encode("ascii", errors = 'ignore')
                newSentences = sentences.replace("\n", " ")
                newText = sent_tokenize(newSentences)
                
                for sentence in newText:
                    
                    newtext = str(sentence).encode('utf-8')
                    
                    '''Sentiment Trigger'''
                    if self.trigger == 'sentiment':
                        
                        emotionScore, regressionLst = self.calculateSentimentScore(newtext, naturalLanguageUnderstanding)
                       
                        emotionScoreDict = ast.literal_eval(emotionScore)
                        sentimentScore = float(emotionScoreDict['score'])
                        
                        '''
                        Watson Classifier to start analyzing confidence/relevance score for each sentence. If the user is talking with confidence
                        or with relevance, the score will be given between 0 to 1, otherwise, -1 to 0
                        '''
                        sentenceClassif = NaturalLanguageClassifier(self.classapikey, self.workspace_id, 
                                                                    self.trigger, mainAuthorID, productURL, sentence, sentimentScore)
                        sentScore, keyScore = sentenceClassif.textBlobClassifier(keyWordsScoreLst, sentencesScoreLst, 
                                                                                 keyWordCounter)
                        sentenceScore.append(sentimentScore)
                        regressionPercent = float(sum(regressionLst)) / len(regressionLst) ## Calculating regression score for all the sentences in one review
                        regressionScore.append(regressionPercent) 
                try:
                    averageScore = float(sum(sentenceScore)) / len(sentenceScore) ## ## Calculating sentiment score for all the sentences in one review
                    averageRegScore = float(sum(regressionScore)) / len(regressionScore) ## ## Calculating regression score for all the sentences in one review
                except: 
                    averageScore = 0.0
                    averageRegScore = 0.0

                '''
                Append all review text for the author
                '''
                textLst = updatedAllAuthorText[mainAuthorID]
                textLst.append(["\'"+text+"\'", str(averageScore)])
                updatedAllAuthorText[mainAuthorID] = textLst
                
                '''
                Sentiment Score for the review
                '''
                sentimentValueScore[mainReviewID] = averageScore
                authorValue.append(averageScore)
                regressionValue.append(averageRegScore)
                
                totalAuthorValue.extend(authorValue)
                totalRegressionValue.extend(regressionValue)    
                    
                print("Retrieving Regression score for: " +str(mainAuthorID))
                score, positivePercent, negativePercent = self.NLPScoreCalculation(mainAuthorID, authorValue, regressionValue)
                self.allReviewScore[mainAuthorID] = [score, positivePercent, negativePercent]
                
          
        print("Retrieving Regression scores for all authors")      
        self.NLPScore(self.allReviewScore, totalAuthorValue, totalRegressionValue)    

        dataBaseUpdateScore(authorScore, tableName1, scoreColumn1) ## Update Review Sentiment Score (Review Table)
        dataBaseUpdateScore(sentimentValueScore, tableName1, scoreColumn2) ## Update Polarity Score (Review Table)
        dataBaseUpdateScore(authorScore, tableName2, scoreColumn1) ## Update Review Sentiment Score (Author Table)

        dataBaseUpdateScore(allAuthorText, tableName3, scoreColumn3) ## Update Review Text (Author Table)
        dataBaseSentenceLabellingUpdate(sentScore, keyScore) ## Construct Sentence Labelling Table and update 
        
    def calculateSentimentScore(self, newtext, naturalLanguageUnderstanding):
        
        '''
        @purpose: Sentiment Score Calculation for the sentence text
        
        @inputs: newtext [string], naturalLanguageUnderstanding [IBM object]
        '''
        
        try:
            regressionLst = []
            responseSentiment = naturalLanguageUnderstanding.analyze(
                text = newtext,
                features = Features(sentiment=SentimentOptions())).get_result()
                            
            outputSentiment = json.loads(json.dumps(responseSentiment, indent = 2))
                            
            responseKeyword = naturalLanguageUnderstanding.analyze(
                text = newtext,
                features = Features(keywords = KeywordsOptions(sentiment = True))).get_result()
            outputKeyword = json.loads(json.dumps(responseKeyword, indent = 2))
                            
            emotionScore = str(outputSentiment['sentiment']).split('\'document\': ')[1]
            emotionScore = emotionScore.strip("}") + '}'
                            
            regressionKeyword = outputKeyword['keywords']
                            
            if regressionKeyword == []:
                regressionLst = [0]
            else:

                for keywords in regressionKeyword:
                    keySentimentScore = keywords['relevance']
                    regressionLst.append(keySentimentScore)          
        except: 
            emotionScore = "{'score': 0, 'label': 'neutral'}"
            regressionLst = [0]
        
        return emotionScore, regressionLst
        
        
    def updateAuthorText(self, allAuthorText, reviewData):
        
        '''
        @purpose: Updating all author ID information into dictionaries
        
        @outputs: allAuthorText [dict]
        '''
    
        for mainAuthorID in reviewData.keys():
            
            allAuthorText[mainAuthorID] = []
            
        return allAuthorText
        
    def NLPScoreCalculation(self, mainAuthorID, authorValue, regressionValue):
        
        '''
        @purpose: Score Calculation using Regression Analysis:
        Determining whether the reviews are diversely between negative and positive for
        one author. 
        
        @inputs: mainAuthorID [string], authorValue [list], regressionValue [list]
        @outputs: None (database update)
        '''
        
        ''' Regression Value '''
        x = np.array(authorValue)
        y = np.array(regressionValue)
        
        warnings.filterwarnings("ignore")
        try:
            r_value = stats.linregress(x, y)[2]
            slope = stats.linregress(x, y)[0]
            if math.isnan(slope):
                slope = 0
        except:
            r_value = 0
            slope = 0
        
        absoluteSlope = abs(float(slope))
        absoluteRValue = abs(float(r_value))
        
        score = abs(absoluteRValue - absoluteSlope)
        value = authorScore[mainAuthorID]
        
        if absoluteRValue >= 0.5:
            score = absoluteRValue
            authorScore[mainAuthorID] = value * (1 + (score * 0.1))
        
        if absoluteRValue < 0.5:
            score = absoluteRValue
            authorScore[mainAuthorID] = value * (1 - (score * 0.1))
                
        ''' Breaker to determine positive and negative reviews'''
        positiveCount = float(sum(n > 0 for n in authorValue))
        numberOfReviews = len(authorValue)
        negativeCount = float(numberOfReviews - positiveCount)
        
        negativePercent = negativeCount / numberOfReviews
        positivePercent = positiveCount / numberOfReviews
            
        return score, positivePercent, negativePercent
            
    def NLPScore(self, allReviewScore, totalAuthorValue, totalRegressionValue):
        
        '''
        @purpose: Score Calculation using Regression Analysis: Determining whether 
        the reviews are diversely between negative and positive for all the authors.
        
        Then, using the regression scores for one author and for all the authors,
        we determine to calculate the score based on the criterias below in comments.
        
        @inputs: allReviewScore [dict], totalAuthorValue [list], totalRegressionValue [list]
        @outputs: None (database update)
        '''
        
        ''' Regression Value '''
        x = np.array(totalAuthorValue)
        y = np.array(totalRegressionValue)
        
        warnings.filterwarnings("ignore")
        try:
            r_value = stats.linregress(x, y)[2]
            slope = stats.linregress(x, y)[0]
            if math.isnan(slope):
                slope = 0
        except:
            r_value = 0
            slope = 0
        
        absoluteSlope = abs(float(slope))
        absoluteRValue = abs(float(r_value))
        
        absoluteScore = abs(absoluteRValue - absoluteSlope)
        
        print('Regression score passed')
        
        for mainAuthorID, mainValues in allReviewScore.items():
            
            score = mainValues[0]
            positivePercent = mainValues[1]
            negativePercent = mainValues[2]
            
            '''Average calculation '''
            '''If the review sentiment score is too positive and 
            if all the reviews are above 90%, then deduct 
            (1 - (1 - percent)) * abs(sentimentScore)
            Old score system  value * ((1 - score) + 1)
            ''' 
            
            value = authorScore[mainAuthorID]
            
            ## Mostly positive, but strong correlation (Add)
            if positivePercent >= 0.9 and absoluteScore >= 0.5:
                score = abs(positivePercent - absoluteRValue)
                authorScore[mainAuthorID] = value * (1 + (score * 0.1))
            
            ## Mostly positive, but diverse correlation (Deduct)
            elif (positivePercent >= 0.9) and (absoluteScore < 0.5): 
                score = abs(positivePercent + absoluteRValue)
                authorScore[mainAuthorID] = value * (1 - (1 - score) * 0.1)
           
            ## Mostly negative, but strong correlation (Add) 
            elif negativePercent >= 0.9 and absoluteScore >= 0.5: 
                score = abs(negativePercent - absoluteRValue)
                authorScore[mainAuthorID] = value * (1 + (score * 0.1))
            
            ## Mostly negative, but diverse correlation (Deduct)  
            elif negativePercent >= 0.9 and absoluteScore < 0.5: 
                score = abs(negativePercent + absoluteRValue)
                authorScore[mainAuthorID] = value * (1 - (1 - score) * 0.1)
            ## Mixed positive and negative (mostly positive), strong correlation (Add)
            if positivePercent > negativePercent and positivePercent < 0.9 and absoluteScore >= 0.5:
                score = abs(positivePercent + absoluteRValue)
                authorScore[mainAuthorID] =  value * (1 + (score * 0.1))
        
            ## Mixed positive and negative (mostly negative), strong correlation (Add)
            if negativePercent > positivePercent and negativePercent < 0.9 and absoluteScore >= 0.5:
                score = abs(negativePercent + absoluteRValue)
                authorScore[mainAuthorID] = value * (1 + (score * 0.1))
        
            ## Mixed positive and negative (mostly positive), weak correlation (Deduct)  
            if positivePercent > negativePercent and positivePercent < 0.9 and absoluteScore < 0.5:
                score = abs(positivePercent - absoluteRValue)
                authorScore[mainAuthorID] = value *  (1 - (1 - score) * 0.1)
            
            if negativePercent > positivePercent and negativePercent < 0.9 and absoluteScore < 0.5:
                score = abs(negativePercent - absoluteRValue)
                authorScore[mainAuthorID] = value *  (1 - (1 - score) * 0.1)
            