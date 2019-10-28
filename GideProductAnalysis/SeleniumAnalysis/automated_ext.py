'''
#################################################
@product: Gide Product Analysis
@filename: Automated Extraction (Website Contents)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import review_config
from Database import data_config
from SeleniumReviewScraper import SeleniumReviewScraper

'''
@purpose: Database Configuration Values
'''
dbname = data_config.databaseHost()[0]
host = data_config.databaseHost()[1]
port = data_config.databaseHost()[2]
userID = data_config.databaseHost()[3]
pwd = data_config.databaseHost()[4]

review_name = review_config.tableNames()[0]
product_name = review_config.tableNames()[1]
author_name = review_config.tableNames()[2]


def scrape():
    
    '''
    @purpose: Initial Stage: Product URL input and time limit for each page (so the sites
    won't block the user)
    
    @inputs: None
    @outputs: productName [string], productURL [string]
    
    Override Note: If you have already scraped the sites and ran the filtering analysis 
    phase, selecting 'y' for YES is mandatory as it removes the score values and 
    reset the database - except for web-scraped contents! If you have scraped the sites,
    but haven't ran filtering analysis phase, selecting 'n' is mandatory as it produces 
    new columns for scores during filtering analysis phase. 
    '''
    
    producturl = input("Enter multiple URLs (space between): ")

    lstofurl = producturl.split(", ")

    time_upper_limit = input("Enter upper limit of time range (5-10): ")
    override = input('''Have you already scraped from sites? If you haven't run 
                    filtering analysis, please select \'n\' (y/n): ''')
    
    '''
    @purpose: Page start values are different for the URLs
    '''
    
    for link in lstofurl:
        
        if "amazon" in link:
            start_page = 1
        elif "tripadvisor" in link:
            start_page = 0
        
        '''
        @purpose: Product Name Extraction from Website URLs
        '''
            
        productname = None
        try:
            productname = link.split("https://")[0]
            productname = productname.split("/")[1]
        except:
            productname = "No product name"
            
        '''
        @purpose: Call Selenium Review Scraper class to start scraping
        
        @inputs: link (url-link) [string], start_page [int], time_upper_limit [int]
        dbname [string], host [string], port[int], userID [string], pwd [string] = ""
        @outputs: None (productInfo [list] is outputted from scraper.initiate()
        '''
            
        productInfo = []
        scraper = SeleniumReviewScraper(link, start_page, time_upper_limit, dbname, 
                                        host, port, userID, pwd)
        productInfo = scraper.initiate(productInfo)
        
        '''
        @purpose: Write Author, Product, Review Table to Database
        Note that 'w' means write on top; 'a' means append/update the table
        
        @inputs: override [string] = 'w' OR 'a', scraper [SeleniumReviewScraper Class Method]
        @outputs: None (Creates three tables for author, product, and review information)
        '''
        
        if override.lower() == 'y':
            scraperTool('w', scraper)
        else:
            scraperTool('a', scraper)    
        override = 'n'

        productName = productInfo[0]
        productURL  = productInfo[1]
        
    return productName, productURL


def scraperTool(func, scraper):
    
    '''
    @purpose: Write Author, Product, and Review Information to Database
    
    @inputs: author_name/review_name (tableName) [string], N/A / product_name [string], func (override function) [string], 
    dbname [string], host [string], port [int], userID [string], pwd [string] = ""
    @outpos: No outputs; just the three tables in database. 
    
    '''
    
    scraper.selenium_writeAuthorCSV(author_name, func, dbname, host, port, userID, pwd)
    scraper.selenium_writeRevProdCSV(review_name, product_name, func, dbname, host, 
                                     port, userID, pwd)  