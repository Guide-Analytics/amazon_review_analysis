'''
#################################################
@product: Gide Product Analysis
@filename: Review Sentiment Analysis Classifier

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from initiateScore import dataBaseBetaWL
from Database import data_config

import json
import ast
#import re

from watson_developer_cloud import AssistantV1
from collections import Counter

from score_config import review_text

from textblob import TextBlob ## Updated to TextBlob (update on ReadMe)

'''
@purpose: Table Configuration Values
'''

tableName = review_text()[0]
scoreColumn = review_text()[1]

'''
@purpose: Database Configuration Values
'''

dbname, host, port, userID, pwd = data_config.databaseHost()

reviewData = dataBaseBetaWL(dbname, host, port, userID, pwd)

class NaturalLanguageClassifier:
    
    '''
    @purpose: Natural Language Analysis: Classifier (Confidence/Relevance Score)
    
    @parameter: -1 to 1 (-1 negative, 0 neutral, 1 positive)
    
    @methods:
    
    keyWordBuild, positiveWordsIntent, negativeWordsIntent, watsonClassifier, textBlobClassifier.
    textAuthorUpdate
    
    @classInputs: api_init, workspace_id, trigger, authorID, productURL, sentence, score
    API identifier: api_init [string], API workspace ID: workspace_id [string] to start Watson Classifier, information trigger [string]
    to analyze sentence's sentiment/confidence scores, authorID [string] (ID of authors), productURL [string] (product URL),
    sentence [string] (sentences from reviews to analyze from), score [float] (sentiment score)

    '''
    def __init__(self, api_key, workspace_id, trigger, authorID, productURL, sentence, score):
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.trigger = trigger
        self.authorID = authorID
        self.productURL = productURL
        self.sentence = sentence
        self.sentScore = score
        
    def keyWordBuild(self):
        
        '''
        @purpose: Building key words from 1-Characteristics.txt file of all the keywords.
        Count how many keywords are being used in each sentence of the reviews. KeyWordsScoreLst
        are all the scores for the keywords and stored in the list. sentencesScoreLst are all the scores
        for the sentences and stored in the list. newKeyWordCount is a dictionary that counts the meaningful 
        words used in the reviews.
        
        @outputs: keyWordsScoreLst [dict], sentencesScoreLst [dict], newKeyWordCount [dict - Counter]
        '''
        
        keyWordsScoreLst = {}
        sentencesScoreLst = {}
        keyWordLst = []
        keyWordCounter = []
        
        text_file = open("1-Characteristics.txt", "r")
        lines = text_file.read().split(', ')
        text_file.close()
        
        for word in lines:
            keyWordsScoreLst[word] = [0, 0]
            sentencesScoreLst[word] = []
        
        for authorID, lstCharact in reviewData.items():
            authorID
            keywords = lstCharact[1]
            keyWordLst.extend(keywords)
        
        for words in keyWordLst:
            nword = ast.literal_eval(words)
            keyWordCounter.extend(nword)
            
        newKeyWordCounter = dict(Counter(keyWordCounter))
                
        return keyWordsScoreLst, sentencesScoreLst, newKeyWordCounter
        
    def positiveWordsIntent(self):
        
        '''
        @purpose: Extract all the positive words
        
        @outputs: lstOfPositiveWords [list]
        '''
        
        positiveWords = open('positiveWords.txt', 'r')
        lines = positiveWords.read().split('\n')
        
        lstOfPositiveWords = []
        
        for word in lines:
            positiveIntent = {}
            positiveIntent['text'] = word
            lstOfPositiveWords.append(positiveIntent)
        
        return lstOfPositiveWords
    
    def negativeWordsIntent(self):
        
        '''
        @purpose: Extract all the negative words
        
        @outputs: lstOfNegativeWords [list]
        '''
        
        negativeWords = open('negativeWords.txt', 'r')
        lines = negativeWords.read().split('\n')
        
        lstOfNegativeWords = []
        
        for word in lines:
            positiveIntent = {}
            positiveIntent['text'] = word
            lstOfNegativeWords.append(positiveIntent)
        
        return lstOfNegativeWords
    
    def watsonClassifier(self, keyWordsScoreLst, sentencesScoreLst, keyWordCounter):
        
        '''
        @purpose: watsonClassifier currently does not work right now
        
        @outputs: ERROR, ERROR
        '''
        
        lstOfPositiveWords = self.positiveWordsIntent()
        lstOfNegativeWords = self.negativeWordsIntent()
        
        assistant = AssistantV1(
            iam_apikey = self.api_key,
            version='2018-11-10'
        )
        
        try:
            assistant.create_intent(
                workspace_id = self.workspace_id,
                intent = 'positive',
                examples = lstOfPositiveWords
            ).get_result()
        except:
            pass
        
        try:
            assistant.create_intent(
                workspace_id = self.workspace_id,
                intent = 'negative',
                examples = lstOfNegativeWords
            ).get_result()
        except:
            pass
        
        
        newResponse = assistant.message(
            workspace_id = self.workspace_id,
            input = {
                'text' : self.sentence
            }
        ).get_result()
        
        try:
            confidenceResult = json.loads(json.dumps(newResponse, indent=2))['intents'][0]['confidence']
        except:
            confidenceResult = 0

        self.authorTextUpdate(confidenceResult, sentencesScoreLst, keyWordsScoreLst, keyWordCounter)
        
        return sentencesScoreLst, keyWordsScoreLst
    
        
    def textBlobClassifier(self, keyWordsScoreLst, sentencesScoreLst, keyWordCounter):
        
        '''
        @purpose: Since Waston Classifier does not work right now, we are using textBlob Classifier to determine
        if the review has meaning/relevance based on sentence's subjectivity.
        
        @inputs: keyWordsScoreLst [list], sentencesScoreLst [list], keyWordCounter [dict]
        @outputs: sentencesScoreLst [list], keyWordsScoreLst [list]
        '''
        
        sentenceSentiment = TextBlob(self.sentence)
        
        confidenceResult = float(sentenceSentiment.sentiment.subjectivity)
        
        self.authorTextUpdate(confidenceResult, sentencesScoreLst, keyWordsScoreLst, keyWordCounter)
        
        return sentencesScoreLst, keyWordsScoreLst
    
        
    def authorTextUpdate(self, confidenceResult, sentencesScoreLst, keyWordsScoreLst, keyWordCounter):
        
        '''
        @purpose: Building key words from 1-Characteristics.txt file of all the keywords.
        Count how many keywords are being used in each sentence of the reviews. KeyWordsScoreLst
        are all the scores for the keywords and stored in the list. sentencesScoreLst are all the scores
        for the sentences and stored in the list. newKeyWordCount is a dictionary that counts the meaningful 
        words used in the reviews. Then, update the new characteristics and information into sentencesScoreLst to
        match specific keywords dict.
        
        @inputs: confidenceResult [float], sentencesScoreLst [list], keyWordsScoreLst [list], keyWordCounter [dict of counts]
        @outputs: None (sentences)
        
        '''
        
        sentence = self.sentence
        sentScore = self.sentScore
        authorID  = self.authorID
        productURL = self.productURL
        
        lstCharact = reviewData[authorID]
            
        mainKeyWords = []
        author = lstCharact[0]
        keywords = lstCharact[1]
            
        for words in keywords:
                
            nword = ast.literal_eval(words)
            mainKeyWords.extend(nword)
            
        mainSet = set(mainKeyWords)
                
        for word in mainSet:
                        
            if word in sentence: 
                    
                wordCount = keyWordCounter[word]   
                value = keyWordsScoreLst[word]
                
                averageSentiment = value[0]
                weightedConfidence = value[1]
                
                originalSentiment = averageSentiment * wordCount
                originalConfidence = weightedConfidence * wordCount
                
                try:
                    newValue = [float(originalSentiment + sentScore) / wordCount,
                                float(originalConfidence + confidenceResult) / wordCount]
                except:
                    newValue = [float(originalSentiment + sentScore),
                                float(originalConfidence + confidenceResult)]
                
                keyWordsScoreLst[word] = newValue
                    
                valuelst = sentencesScoreLst[word]
                valuelst.append([sentence, authorID, author, '('+str(sentScore)+', '+str(confidenceResult)+')', productURL])
                sentencesScoreLst[word] = valuelst