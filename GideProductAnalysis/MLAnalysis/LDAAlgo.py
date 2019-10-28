import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sklearn.preprocessing import LabelEncoder

#from xgboost import XGBRegressor
#from sklearn.linear_model import BayesianRidge
#from sklearn.ensemble import GradientBoostingRegressor
#from sklearn.neural_network import MLPRegressor

from sklearn.neighbors import KNeighborsRegressor
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#from sklearn.metrics import mean_squared_error # might use this
from sklearn.model_selection import cross_val_score
from MLPseudoLabeller import PseudoLabeller

def MLStart():
    MLAnalysis()
    
def MLTrain(train, test):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    '''Retrieving data values for a matrix'''

    col = ['word_count_score', 'quality_word_score', 'word_reptition_score','review_sentiment_score','low_quality_score','verified_purchase_score']
    #test['category'] = 0
    combi = train.append(test)
    number = LabelEncoder()
    for i in col:
        combi[i] = number.fit_transform(combi[i].astype('float'))  ## scores
        combi[i] = combi[i].astype('int') ##  cateogry 
        train = combi[:train.shape[0]]
        test = combi[train.shape[0]:]
        test.drop('category',axis=1,inplace=True)

        '''Removing unnecessary values before matrix construction'''

    training = train.drop(['author_url','product_id', 'author', 'rank', 'num_of_reviews', 'date_scraped'],axis=1)
    testing = test.drop(['author_url','product_id', 'author', 'rank', 'num_of_reviews', 'date_scraped'],axis=1)
    
    y_train = training['category']
    training.drop('category',axis=1,inplace=True)

    features = training.columns
    target = 'category'

    X_train, X_test = training, testing

#RandomForestRegressor(),
#XGBRegressor(nthread=1),
#MLPRegressor(),
#Ridge(),
#BayesianRidge(),
#ExtraTreesRegressor(),
#ElasticNet(),
#GradientBoostingRegressor()

    model = KNeighborsRegressor()

    model.seed = 42
    num_folds = 3

    scores = cross_val_score(model, X_train, y_train, cv=num_folds, scoring='neg_mean_squared_error')
    score_description = " %0.2f (+/- %0.2f)" % (np.sqrt(scores.mean()*-1), scores.std() * 2)
    print(score_description)
    
    return features, target, X_train, X_test, y_train
    

def MLAnalysis():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    train = pd.read_csv('dataset_train.csv')
    test = pd.read_csv('dataset_test2.csv')
    
    features, target, X_train, X_test, y_train = MLTrain(train, test)
    
    model = PseudoLabeller(
    KNeighborsRegressor(), ##LinearDiscriminantAnalysis()
    test,
    features,
    target,
    sample_rate = 0.3
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    
    

    '''Output to CSV'''
    sub = pd.DataFrame(data = pred, columns=['category'])

    sub['author_id'] = test['author_id']
    sub['product_id'] = test['product_id']
    sub['author_url'] = test['author_url']
    sub['author'] = test['author']
    sub['rank'] = test['rank']
    sub['num_of_reviews'] = test['num_of_reviews']
    
    sub.to_csv('dataset_test_output.csv', index='False')

    '''Probably not necessary'''
    #result = cross_val_score(model, X_train, y_train, cv=num_folds, scoring='neg_mean_squared_error', n_jobs=8)
