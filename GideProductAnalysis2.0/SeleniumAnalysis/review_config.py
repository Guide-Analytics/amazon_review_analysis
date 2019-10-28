'''
#################################################
@product: Gide Product Analysis
@filename: Review Config (Website Contents --> Database)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

review_id = "review_id"
rating = "rating"
verified_purchase = "verified_purchase"
max_rating = 'max_rating'
review_title = "review_title"
review_text = "review_text"
date = "date"
author_id = "author_id"
date_scraped = "date_scraped"
product_id = "product_id"
    
author_url = "author_url"
author = "author"
num_of_reviews = "num_of_reviews"
rank = "rank"
    
product = "product"
product_url = "product_url"
average_rating = "product_rating"
    
def tableNames():
    
    '''
    @purpose: Table Names
    
    @outputs: review_name [string], product_name [string], author_name [string]
    '''
    
    review_name = "review_table"
    product_name = "product_table"
    author_name = "author_table"
    
    return review_name, product_name, author_name

def csvHeader():
    
    '''
    @purpose: Header Values (Names)
    
    @outputs: csv_head_product [list of header values],  csv_head_reviews [list of header values], 
    csv_head_profile [list of header values], 
    '''
    
    csv_head_product = [product_id, author_id, product, product_url, average_rating, max_rating, date_scraped]
    csv_head_reviews = [review_id, rating, verified_purchase, max_rating, review_title, review_text, date, 
                        author_id, date_scraped, product_id]
    csv_head_profile = [author_id, product_id, author_url, author, rank, num_of_reviews, date_scraped]

    return csv_head_product, csv_head_reviews, csv_head_profile
    
def tableHeader():
    
    '''
    @purpose: Header Values (Names) --> Database
    
    @outputs: tableReview [big string], tableProfile [big string], 
    tableProduct [big string], 
    '''
    
    product_name = tableNames()[1]
    author_name = tableNames()[2]
    
    ## Database Header (Final Phase)
    tableReview = '''('''+review_id+ ''' text PRIMARY KEY NOT NULL, '''+rating+''' INT NULL, '''+verified_purchase+''' VARCHAR(10) NULL, 
        '''+max_rating+''' INT NOT NULL, '''+review_title+''' VARCHAR(255) NULL, '''+review_text+''' text NULL, '''+date+''' date NULL, 
        '''+author_id+''' BIGINT NOT NULL, '''+date_scraped+''' timestamp(6) NOT NULL, '''+product_id+''' BIGINT NOT NULL, 
        FOREIGN KEY ('''+product_id+''', '''+author_id+''') REFERENCES '''+product_name+ '''('''+product_id+''', '''+author_id+'''), 
        FOREIGN KEY ('''+author_id+''') REFERENCES '''+author_name+ '''('''+author_id+''')); '''
    
    tableProfile = '''('''+author_id+''' BIGINT PRIMARY KEY NOT NULL, '''+product_id+''' BIGINT NOT NULL, '''+author_url+''' VARCHAR(255) NULL, 
    '''+author+''' VARCHAR(255) NULL, '''+rank+''' INT NULL, '''+num_of_reviews+''' INT NULL, '''+date_scraped+''' timestamp(6) NOT NULL); '''
    
    tableProduct = '''('''+product_id+''' BIGINT NOT NULL, '''+author_id+''' BIGINT NOT NULL, '''+product+''' VARCHAR(255) NULL, 
    '''+product_url+''' VARCHAR(255) NULL, '''+average_rating+''' REAL NULL, '''+max_rating+''' INT NOT NULL, '''+date_scraped+''' timestamp(6) NOT NULL, 
    PRIMARY KEY ('''+product_id+''', '''+author_id+'''), 
    FOREIGN KEY ('''+author_id+''') REFERENCES '''+author_name+ '''('''+author_id+''')); '''
    
    return tableReview, tableProfile, tableProduct