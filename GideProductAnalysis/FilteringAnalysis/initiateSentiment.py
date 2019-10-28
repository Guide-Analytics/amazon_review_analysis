'''
#################################################
@product: Gide Product Analysis
@filename: Review Sentiment Start

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from review_sentiment import NaturalLanguageToneAnalysis
from reviewClassifier import NaturalLanguageClassifier

from watson_developer_cloud import AssistantV1

import json

def reviewSentiment():
    
    '''
    @purpose: Trigger the review sentiment analysis class: NaturalLanguageToneAnalysis
    where it takes the API identifier: api_init [string], API key: api_key [string],
    API workspace ID: workspace_id [string], and the information trigger [string]
    to analyze sentence's sentiment/confidence scores
    
    '''
    
    class_api_key = "Kv03oFfMKFHEGoiNm_NFvTYeRaei0WXneOB-M1O1rw6u"
    
    assistant = AssistantV1(
            iam_apikey = class_api_key,
            version='2018-11-10'
        )
        
    try:
        response = assistant.create_workspace(
            name = 'Confidence',
            description = 'Confidence Level'
        ).get_result()
        response = assistant.list_workspaces().get_result()
        
        response
    except:
        pass
        
    response = assistant.list_workspaces().get_result()
    result = json.loads(json.dumps(response))['workspaces'][0]['workspace_id']
    
    api_init = "ibm"
    api_key = "dZLqeJp0WHcapgMUwueea_bpKXMJnxFgtG12yWpAkjwn"
    workspace_id = result
    trigger = 'sentiment'
    NaturalLanguageToneAnalysis(api_init, api_key, class_api_key, workspace_id, trigger)
    
def reviewClassifier():
    
    '''
    @purpose: Testing purposes

    '''
    #api_init = "ibm"
    api_key = 'dnTz4UV8EkRWBTx9GOwgoA_h671E7-eSSCAMTRPd3k4M'
    trigger = 'sentiment'
    
    NaturalLanguageClassifier(api_key, trigger, 'author', 'review', 0)
    
