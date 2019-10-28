'''
#################################################
@product: Gide Product Analysis
@filename: Selenium Review Scraper (Website Contents --> Database)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import ssl
import time
from dateutil import parser
from random import randint
import csv
import uuid
import os
import review_config
import sys
sys.path.insert(0, 'GideProductAnalysis2.0/Database')

from AmazonConfig import AmazonConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from Database import writeTable
import UserProfileSelenium

class SeleniumReviewScraper:
    
    '''
    @purpose: Selenium Review Scraper (Amazon - for now, Google, TripAdvisor - future)
    To scrape web information from websites using Selenium Toolkit and extract the information
    to database (i.e. author, product, review, rating, etc.)
    
    The objective of scraping is not to get blocked by the sites. Furthermore, understanding
    how the pages dynamically change by the number of reviews the product contains (i.e. pageNumber
    changes, special web page number 
    
    @parameters: Web elements from config files; they are dynamically changed overtime. 
    reviewdata [list], productdata [list], profiledata [list]
    
    @methods:
    
    browser, set_url, set_start_page, build_id, build_prodid, build_author_id, build_rating, build_maxrating,
    build_avgrating, build_author, build_author_url, build_product_url, build_product, build_title, build_text,
    build_date, build_dateToday, build_verifiedpurchase, initiate, scrape, selenium_writeAuthorCSV, 
    selenium_writeRevProdCSV
    
    @classInputs: url [string] (website URL), start_page [int] (start page number of the product review),
    time_upper_limit [int] (give time limit for scraping each page to prevent block from sites, 
    dbname [string], host [int], port [int], userID [string], pwd = "" [string]

    '''
    
    # Ignore SSL certificate errors
    ssl._create_default_https_context = ssl._create_unverified_context
    
    csv_head_product = review_config.csvHeader()[0]
    csv_head_reviews = review_config.csvHeader()[1]
    csv_head_profile = review_config.csvHeader()[2]

    def __init__(self, url, start_page, time_upper_limit, dbname, host, port, userID, pwd):
        self.url = url
        self.set_url()
        self.start_page = int(start_page)
        self.time_upper_limit = time_upper_limit
        self.dbname = dbname
        self.host = host
        self.port = port
        self.userID = userID
        self.pwd = pwd
        self.reviewdata = []
        self.productdata = []
        self.profiledata = []
        self.config_elements = AmazonConfig()

    
    def browser(self, url):
        
        '''
        Firefox WebDriver launches URL inputted by user. If no URL/URL cannot be opened, 
        raise error and exit
    
        @inputs: URL [string]
        @outputs: self.site (URL site) [object]
        '''
        
        options = webdriver.FirefoxOptions()
        options.set_headless(True)
        options.add_argument(" - incognito")

        #re = "\(1 page\)[ \t\xa0\n]+(.+?)[ \t\xa0\n]+Identify"
        self.site = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', firefox_options=options)
        
        try:
            #if self.start == 0:
            self.site.get(url) #navigate to page behind login
        except:
            print('Browser may have lost connection. Please try again later')
            self.site.quit()
            exit()
            
        return self.site
    
    def set_sleep_timer(self):
        
        '''
        Set timer for scraping each web page (recommended around 5 - 10 seconds)
        '''
        
        sleep_time = randint(3, int(self.time_upper_limit))
        print("\nPlease wait for: " + str(sleep_time) + " seconds.")
        time.sleep(sleep_time)
    
    def set_url(self):
        
        '''
        Start URL using special formatted URL (Amazon End Value : +pageNumber=X) so it will scraped
        the pages from pageNumber=1 ... pageNumber=X 
        '''
    
        url = self.url.split("&pageNumber")
        try:
            self.url = url[0]
        except:
            self.url = url
            
    def set_start_page(self, start_page):

        '''
        Set start page to a special formatted URL (Amazon End Value : +pageNumber=X) so it will scraped
        the pages from pageNumber=1 ... pageNumber=X 
        
        @inputs: start_page [int]
        @outputs: url [string]
        '''

        url = self.url + "&pageNumber=" + str(start_page)
        return url
    
    def build_id(self):
        
        '''
        Building Unique ID for the Review
        
        @outputs: uniqueID [string]
        '''
        
        uniqueID =  str(uuid.uuid4().node)
        return uniqueID
    
    def build_prodid(self):
        
        '''
        Building Unique Product ID for the Review-Product
        
        @outputs: prod_id [int]
        '''
        
        prod_id = int(uuid.uuid4().node)
        return prod_id
    
    def build_authorid(self):
        
        '''
        Building Unique Author ID for the Review-Author
        
        @outputs: author_id [int]
        '''
        
        author_id = int(uuid.uuid4().node)
        return author_id
    
    def build_rating(self, elements):
        
        '''
        Building Rating from the Review
        @inputs: elements [web object]
        @outputs: nrating [int]
        '''
        
        ratingElement = self.config_elements.rating()[0]
        ratingValue = self.config_elements.rating()[1]
        
        try:
            prodName = elements.find_element_by_css_selector(ratingElement)
            rating = prodName.find_element_by_css_selector(ratingValue).get_attribute('textContent')
            nrating = int(float(rating.split(" ")[0]))
        except:
            nrating = 0
        return nrating
    
    def build_maxrating(self):
        
        '''
        Max Rating: DEFAULT = 5
        
        @outputs: maxrating [5]
        '''
        
        maxrating = 5
        return maxrating
    
    def build_avgrating(self, elements):
        
        '''
        Building Average Rating from the Review
        
        @inputs: elements [web object]
        @outputs: navgrating [float]
        '''
        
        avgratingElement1 = self.config_elements.avgRating()[0]
        avgratingElement2 = self.config_elements.avgRating()[1]
        
        try:
            avgrating = elements.find_element_by_css_selector(avgratingElement1).get_attribute('textContent')
        except:
            avgrating = elements.find_element_by_css_selector(avgratingElement2).get_attribute('textContent')
            
        # Rating is in "text" format; therefore, we only want the first value (i.e. 3.5 out of 5 => 3.5).
        # Therefore, we remove the space from the text rating and extract the first element
        navgrating = float(avgrating.split(" ")[0])
        return navgrating

    def build_author(self, elements):
        
        '''
        Building Author from the Review
        
        @inputs: elements [web object]
        @outputs: author [string]
        '''
        
        authorElement = self.config_elements.author()
        author = elements.find_element_by_css_selector(authorElement).text.encode('utf-8')
        return author
    
    def build_author_url(self, elements):
        
        '''
        Building Author URL from the Review
        
        @inputs: elements [web object]
        @outputs: author_url [string]
        '''
        
        # Author URL attribute is located in "href"
        authorURLElement = self.config_elements.authorURL()
        author_url = elements.find_element_by_css_selector(authorURLElement).get_attribute('href')
        return author_url
    
    def build_product_url(self, elements):
        
        '''
        Building Product URL from the Review
        
        @inputs: elements [web object]
        @outputs: prodURL [string]
        '''
        
        # Product URL attribute is located in "href"
        productURLElement = self.config_elements.productURL()
        prodURL = elements.find_element_by_css_selector(productURLElement).get_attribute('href')
        return prodURL

    def build_product(self, elements):
        
        '''
        Building Product Name from the Review
        
        @inputs: elements [web object]
        @outputs: prodName [string]
        '''
        
        productNameElement = self.config_elements.productName()
        prodName = elements.find_element_by_css_selector(productNameElement).get_attribute('textContent').encode('utf-8')
        return prodName
    
    def build_title(self, elements):
        
        '''
        Building Review Title from the Review
        
        @inputs: elements [web object]
        @outputs: title [string]
        '''
        
        titleElement = self.config_elements.title()
        try:
            title = elements.find_element_by_css_selector(titleElement).text.encode('utf-8')
        except:
            title = "No review title"
        return title
    
    def build_text(self, elements):
        
        '''
        Building Review Text from the Review
        
        @inputs: elements [web object]
        @outputs: newBodyText [string]
        '''
        
        textElement = self.config_elements.text()
        bodyText = elements.find_element_by_css_selector(textElement).text.encode('utf-8')
        return bodyText

    def build_date(self, elements):
        
        '''
        Building Review Date from the Review
        
        @inputs: elements [web object]
        @outputs: dateWritten [datetime] ==> dateConvert [string]
        '''
        
        dateElement = self.config_elements.date()
        dateWritten = elements.find_element_by_css_selector(dateElement).text
        dateConvert = str(parser.parse(dateWritten)).split(" ")[0]
        return dateConvert
    
    def build_dateToday(self):
        
        '''
        Building Date Today
        Format: DATE, TIMESTAMP 
        
        @outputs: datetime.now() [datetime] ==> dateToday [sting]
        '''
        
        dateToday = str(datetime.now())
        return dateToday

    def build_verified_purchase(self, elements):
        
        '''
        Building Verified Purchase detection from the Review
        
        @outputs: DEFAULT "YES", otherwise "NO"
        '''
        
        # Yes = purchased, No = not purchased
        verifiedPurchaseElement = self.config_elements.verifiedPurchase()
        try: 
            elements.find_element_by_css_selector(verifiedPurchaseElement).text
            return "Yes"
        except:
            return "No"

    def initiate(self, productInfo):
        
        '''
        Start scraping by looping pages from 1 to n (depending on the site's interface)
        
        @outputs: dateWritten [datetime] ==> dateConvert [string]
        '''
        
        start_page = self.start_page
        page_bool = True
        
        self.reviewdata.append(self.csv_head_reviews)
        self.productdata.append(self.csv_head_product)
        self.profiledata.append(self.csv_head_profile)

        while page_bool:
            
            detectElement = self.config_elements.detect()
            try:
                url = self.set_start_page(start_page)
                self.site = self.browser(url)
            except:
                print("URL entered is wrong. Please try again with the right URL.")
                exit()
            
            # Wait for review contents to load (it must guarantee the reviews blocks exist or else something is not right)
            try:
                WebDriverWait(self.site, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, detectElement)))
            except:
                if TimeoutException:
                    print("Timed out waiting for page to load")
                    '''self.site.quit()'''
                    exit()
                    
                else:
                    print("URL entered is wrong. Please try again with the right URL.")
                    self.site.quit()
                    exit()

            # Sleep because Amazon might block your IP if there are too many requests every second
            self.set_sleep_timer()
            
            print("Scraping page " + str(start_page) + ".")
            
            reviewsElement = self.config_elements.reviewsDetect()
            reviews = self.site.find_elements_by_css_selector(reviewsElement)
            
            # Stop scrape when the review blocks are not detected
            if reviews == [] or reviews == None:
                print("No page detected. Stopping scrape")
                self.site.quit()
                break
            
            self.scrape(self.site, reviews)
            prodName = self.build_product(self.site)
            prodURL = self.build_product_url(self.site)
            productInfo.append([prodName, prodURL])

            self.site.quit()
            start_page += 1
            
        return productInfo[0]
        
    def scrape(self, browser, reviews):
        
        '''
        Starting scrape web elements from the review site
        
        @outputs: dateWritten [datetime] ==> dateConvert [string]
        '''
        
        prodName = self.build_product(browser)
        produrl = self.build_product_url(browser)
        avgrating = self.build_avgrating(browser)
        prodID = self.build_prodid()
        
        n_time = self.time_upper_limit
        
        for elements in reviews:
                
            csv_profiledata = []
            csv_review = []
            csv_product = []
                
            authorID = self.build_authorid()
                
            ## Primary Key Product (Product)
            csv_product.append(prodID)
                
            ## Product to Author (Product)
            csv_product.append(authorID)
                
            ## Product Name (Product)
            csv_product.append(prodName)
                
            ## Product URL (Product)
            csv_product.append(produrl)
                
            ## Average Rating (Product)
            csv_product.append(avgrating)
                
            ## Max Rating (Product)
            maxrating = self.build_maxrating()
            csv_product.append(maxrating)
                
            ## Date Scraped (Product)
            dateToday = self.build_dateToday()
            csv_product.append(dateToday)
                
            ## Unique ID (Review)
            uniqueID = self.build_id()
            csv_review.append(uniqueID)
                
            ## Rating (Review)
            rating = self.build_rating(elements)
            csv_review.append(rating)
                
            ## Verified Purchase (Review)
            verifiedPurchase = self.build_verified_purchase(elements)
            csv_review.append(verifiedPurchase)
                
            ## Max Rating (Review)
            csv_review.append(maxrating)
                
            ## Review Title (Review)
            reviewtitle = self.build_title(elements)
            csv_review.append(reviewtitle)
                
            ## Review Text (Review)
            bodytext = self.build_text(elements)
            csv_review.append(bodytext)
                
            ## Date Written (Review)
            dateWritten = self.build_date(elements)
            csv_review.append(dateWritten)
            
            ## Foreign Key Review to Author (Review)
            csv_review.append(authorID)
                
            ## Date Scraped (Review)
            csv_review.append(dateToday)
                
            ## Foreign Key Review to Product (Review)
            csv_review.append(prodID)
                
            author = self.build_author(elements)
            author_url = self.build_author_url(elements)

            self.productdata.append(csv_product)
            self.reviewdata.append(csv_review)
            
            '''UserProfilePage'''
            try:
                profileResponse = UserProfileSelenium.SeleniumUserProfile(csv_profiledata, produrl, prodName, author, author_url, authorID, prodID, n_time)
                user_prods, user_revs, user_prof = profileResponse.selenium_scrapeProfile()
            except:
                print("Profile Web Error")
                pass
                
            #self.set_sleep_timer()
            
            self.productdata.extend(user_prods)
            self.reviewdata.extend(user_revs)
            self.profiledata.extend(user_prof)
                
            
    def selenium_writeAuthorCSV(self, author_name, func, dbname, host, port, userID, pwd):
        
        '''
        @purpose: Writing author information to database (to CSV and then copy CSV to database)
        
        @inputs: author_name [string] (table name), func [string] action to erase information or to keep
        dbname [string], host [int], port [int], userID [string], pwd = "" [string]
        @outputs: None (database update)
        '''
        
        self.author_path = author_name + '.csv'
        author_path = self.author_path
        print("\nWriting to file.\n"+author_path)
        
        with open((author_path), func) as csv_file :
            writer = csv.writer(csv_file)
            writer.writerows(self.profiledata)
        
        print("\nWriting to Table.\n"+author_name)
        writeTable.authorTable(author_path, author_name, dbname, host, port, userID, pwd, func)
        os.remove(author_path)
            
    def selenium_writeRevProdCSV(self, review_name, prod_name, func, dbname, host, port, userID, pwd):
        
        '''
        @purpose: Writing review and product information to database (to CSV and then copy CSV to database)
        
        @inputs: author_name [string] (table name), func [string] action to erase information or to keep
        dbname [string], host [int], port [int], userID [string], pwd = "" [string]
        @outputs: None (database update)
        '''
        
        self.review_path = review_name + '.csv'
        review_path = self.review_path
        print("\nWriting to file.\n"+review_path)
        
        with open((review_path), func) as csv_file :
            writer = csv.writer(csv_file)
            writer.writerows(self.reviewdata)
            
        
        self.product_path = prod_name + '.csv'
        product_path = self.product_path
        print("\nWriting to file.\n"+product_path)
        
        with open((product_path), func) as csv_file :
            writer = csv.writer(csv_file)
            writer.writerows(self.productdata)
            
        print("\nWriting to Table.\n"+prod_name)
        writeTable.productTable(product_path, prod_name, dbname, host, port, userID, pwd, func)
        
        print("\nWriting to Table.\n"+review_name)
        writeTable.reviewTable(review_path, review_name, dbname, host, port, userID, pwd, func)
        
        os.remove(review_path)
        os.remove(product_path)
