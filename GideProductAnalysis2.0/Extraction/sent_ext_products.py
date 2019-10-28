import review_input
#import main

features = review_input.charact()
'''
def sentProd(reviewData):   
    revLst = review_input.inputRev()[1]
    #features = rev_input.charact()
    ## Dictionary containing 
    char_sent = {}
    newsentence = []
    
    fileNum = 1
    
    characterDict(char_sent)  
    for item in revLst:
        key = item[0]
        if key == 'author':
            char_sent = dict( [(k,v) for k,v in char_sent.items() if len(v)>0])
            main.productFound(char_sent, fileNum)
            fileNum += 1
            char_sent = {}
            characterDict(char_sent)  
            continue
        sent = item[1]
        for bodyrev in sent:
            sentence = "".join(bodyrev).encode('utf-8')
            for feat in features:
                if feat in sentence.lower():
                    newsentence.append(sentence + ' (reviewerID: ' + key +')')
                    char_sent[feat].extend(newsentence)
                    newsentence = []
                           
    char_sent = dict( [(k,v) for k,v in char_sent.items() if len(v)>0])         
    main.productFound(char_sent, fileNum)
    
def characterDict(char_sent):
    
    for feat in features:
        char_sent[feat] = []
    return char_sent
    
'''