'''
#################################################
@product: Gide Product Analysis
@filename: Selenium Profile Scraper (Website Contents --> Database)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import csv
import time
import os
import uuid
from selenium import webdriver

from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from dateutil import parser
#from selenium.webdriver.common.keys import Keys

#from Database import pushDataCSV

class SeleniumUserProfile:
    
    '''
    @purpose: Selenium Profile Scraper (Amazon - for now)
    To scrape web information from review sites that contains profile information using Selenium Toolkit 
    and extract the information to database (i.e. author, product, review, rating, etc.). Each review section
    will contain an author that can be directed to the profile information. 
    
    The objective of scraping is not to get blocked by the sites. Furthermore, understanding
    how the pages dynamically change by the number of reviews the product contains (i.e. scrolling the webpage
    until it reaches the bottom of the profile information).
    
    @parameters: Web elements from config files; they are dynamically changed overtime. 
    reviewdata [list], productdata [list], profiledata [list]
    
    @methods:
    
    browser, build_id, build_votes_reviews, build_rating, build_prodName, build_prodid, build_avg_rating, build_max_rating,
    build_title, build_text, build_prodURL, build_rank, build_date, selenium_scrapeProfile, selenium_scrapeRank,
    selenium_writeAuthorCSV, 
    selenium_writeRevProdCSV
    
    @classInputs: csv_data [list] (review data information), prodName [string] (product name of the initial product URL),
    author [string] (author name), url [string] (product URL), authorID [int] (ID of author), productID [int] (ID of product),
    sleep_time [int] 

    '''
    
    def __init__(self, csv_data, prodURL, prod_name, author, url, authorID, productID, sleep_time):
        self.csv_data = csv_data
        self.prodName = prod_name
        self.author = author
        self.authorid = authorID
        self.productid = productID
        self.prodURL = prodURL
        self.url = url
        self.sleep_time = sleep_time
        
    def browser(self, url):
        
        '''
        Firefox WebDriver launches URL inputted by user. If no URL/URL cannot be opened, 
        raise error and exit
    
        @inputs: URL [string]
        @outputs: browser (Selenium object web information) [object]
        '''
        
        options = webdriver.FirefoxOptions()
        options.set_headless(True)
        options.add_argument(" - incognito")

        browser = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', firefox_options=options)
        
        try:
            
            browser.get(url) #navigate to page behind login
            
        except:
            print('Browser may have lost connection. Please try again later')
            browser.quit()
            exit()
            
        return browser
    
    def build_id(self):
        
        '''
        Building Unique ID for the Review
        
        @outputs: uniqueID [string]
        '''
        
        uniqueID =  str(uuid.uuid4().node)
        return uniqueID
        
    def build_votes_reviews(self, browser):
        
        '''
        Building # Votes for the author's reviews
        
        @inputs: browser [Selenium web object]
        @outputs: votes [string]
        '''
        
        # find_elements_by_xpath returns an array of selenium objects.
        votesElements = browser.find_elements_by_xpath("//div[@class='dashboard-desktop-stat-value']")
        votes = [x.text for x in votesElements]
        return votes
    
    def build_rating(self, elements):
        
        '''
        Building review ratings for the author
        
        @inputs: elements [Selenium web object]
        @outputs: newRating [int]
        '''
        
        try:
            rating = elements.find_element_by_css_selector('span.a-icon-alt:last-child').get_attribute('textContent') 
            newRating = int(rating.split(" ")[0])
        except:
            rating = 0
        return newRating

    def build_prodName(self, elements):
        
        '''
        Building product name for the reviews
        
        @inputs: elements [Selenium web object]
        @outputs: prodName [string]
        '''
        
        try:
            prodName = elements.find_element_by_css_selector('div.a-row.a-spacing-medium').text.encode('utf-8')
        except:
            prodName = "NO PRODUCT NAME"
        return prodName
    
    def build_prodid(self):
        
        '''
        Building product IDs 
        
        @outputs: prod_id [int]
        '''
        
        prod_id = int(uuid.uuid4().node)
        return prod_id
    
    def build_avg_rating(self, elements):
        
        '''
        Building average ratings for the reviews
        
        @inputs: elements [Selenium web object]
        @outputs: newAvgRating [float]
        '''
        
        try:
            prodName = elements.find_element_by_css_selector('div.a-row.profile-at-product-review-stars')
            avgRating = prodName.find_element_by_css_selector('span.a-icon-alt:last-child').get_attribute('textContent')
            newAvgRating = float(avgRating.split(" ")[0])
        except:
            newAvgRating = 0
        return newAvgRating
    
    def build_max_rating(self):
        
        '''
        Building max rating for the reviews
        
        @outputs: max_rating [int]
        '''
        
        max_rating = 5
        return max_rating
    
    def build_title(self, elements):
        
        '''
        Building review titles
        
        @inputs: elements [Selenium web object]
        @outputs: title [string]
        '''
        
        try:
            title_element = elements.find_element_by_css_selector('div.a-section.a-spacing-none')
            title = title_element.find_element_by_css_selector("h1[class='a-size-base a-spacing-none a-color-base profile-at-review-title a-text-bold']").text.encode('utf-8')
        except:
            title = "NO TITLE"
        return title
        
    def build_text(self, elements):
        
        '''
        Building review texts
        
        @inputs: elements [Selenium web object]
        @outputs: newText [string]
        '''
        
        try:
            text_element = elements.find_element_by_css_selector('div.a-section.a-spacing-none')
            text = text_element.find_element_by_css_selector("p[class='a-spacing-small a-spacing-top-mini a-color-base profile-at-review-text profile-at-review-text-desktop']").text.encode('utf-8')
            newText = text.replace("\n", " ")
        except:
            newText = "NO TEXT GIVEN"
        return newText
    
    def build_prodURL(self, elements):
        
        '''
        Building product URLs
        
        @inputs: elements [Selenium web object]
        @outputs: prod [string]
        '''
        
        try:
            prod = elements.find_element_by_css_selector("a[class='a-link-normal profile-at-product-box-link a-text-normal']").get_attribute('href')
        except:
            prod = "NO URL DETECTED"
        return prod
    
    def build_rank(self, elements):
        
        '''
        Building ranks for the author
        
        @inputs: elements [Selenium web object]
        @outputs: nrank [int]
        '''
        
        try:
            rank = elements.find_element_by_css_selector('div.desktop.padded.card > div.a-row > div.a-section > div.a-section.a-spacing-top-base > div.a-row.a-spacing-base').get_attribute('textContent').encode('utf-8')
            strrank = rank.split('#')[1]
            nrank = int(strrank.replace(',', ''))
        except:
            nrank = 0
        return nrank
    
    def build_date(self, elements):
        
        '''
        Building review dates
        
        @inputs: elements [Selenium web object]
        @outputs: date [string]
        '''
        
        date_elementp1 = elements.find_element_by_css_selector("span[class='a-profile-descriptor']").text
        date_elementp2 = date_elementp1.split('reviewed a product')[1][3:]
        date = str(parser.parse(date_elementp2)).split(" ")[0]
        return date
    
    def build_verified_purchase(self, elements):
        
        '''
        Building verified purchase 
        
        @inputs: elements [Selenium web object]
        @outputs: "Yes" purchased, "No" not purchased
        '''
        
        # Yes = purchased, No = not purchased
        try: 
            elements.find_element_by_css_selector('div.a-row.a-spacing-mini:last-child').get_attribute('textContent')
            return "Yes"
        except:
            return "No"
    
    def selenium_scrapeProfile(self):
        
        '''
        Starting profile scraping. Retrieve profile information such as rank, ratings, all reviews and titles
        
        @outputs: product [list] (product information), review [list] (review information), self.csv_data [list] (profile information)
        '''
    
        author = self.author
        author_id = self.authorid
        product_id = self.productid
        author_url = self.url
        dateToday = str(datetime.now())
        max_rating = self.build_max_rating()
        
        product = []
        review = []
        
        browser = self.browser(author_url)
                
        # Wait for review contents to load (it must guarantee the reviews blocks exist or else something is not right)
        try:
            WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#customer-profile-timeline.a-section')))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            #self.timesleep
        
        self.votes = self.build_votes_reviews(browser)
        profiles = browser.find_elements_by_xpath("//div[@class='desktop card profile-at-card profile-at-review-box']")
        numofreviews = len(profiles)
        
        
        # User may be private or not reached when the review sections are not detected by Selenium 
        if profiles == []:
            print('User profile is private')
            
            profilelst = []
        
            ## Primary Key from Reviews
            profilelst.append(author_id)
            
            profilelst.append(product_id)
            
            ## Author URL
            profilelst.append(author_url)
            
            ## Author (For another case in Review)
            #author = self.author 
            profilelst.append(author)
            
            ## Rank
            rank = self.build_rank(browser)
            profilelst.append(rank)
            
            ## Number of reviews
            profilelst.append(numofreviews)
            
            # Date scraped
            profilelst.append(dateToday)
           
            self.csv_data.append(profilelst)
            
            browser.quit()
            return product, review, self.csv_data
        else:
            
            print('Retrieving Author')
            
            profilelst = []
            ## Primary Key from Reviews
            profilelst.append(author_id)
            
            profilelst.append(product_id)
            
            ## Author URL
            profilelst.append(author_url)
            
            ## Author (For another case in Review)
            #author = self.author 
            profilelst.append(author)
            
            ## Rank
            rank = self.build_rank(browser)
            profilelst.append(rank)
            
            ## Number of reviews
            profilelst.append(numofreviews)
            
            # Date scraped
            profilelst.append(dateToday)
            
            self.csv_data.append(profilelst)
            
            for elements in profiles:
                
                csv_product = []
                csv_review = []
                
                ## Primary Key Product (Product) (if condition)
                newprodName = self.build_prodName(elements)
                produrl = self.build_prodURL(elements)
                
                if produrl not in self.prodURL:
                    productID = self.build_prodid()
                    csv_product.append(productID)
                    
                    ## Product to Author (Product)
                    csv_product.append(author_id)
                    
                    ## Product Name (Product)
                    csv_product.append(newprodName)
                
                    ## Product URL (Product)
                    csv_product.append(produrl)
                
                    ## Average Rating (Product)
                    avgrating = self.build_avg_rating(elements)
                    csv_product.append(avgrating)
                
                    ## Max Rating (Product)
                    maxrating = self.build_max_rating()
                    csv_product.append(maxrating)
                
                    ## Date Scraped (Product)
                    csv_product.append(dateToday)
                
                    ## Unique ID (Review) (if condition)
                    uniqueID = self.build_id()
                    csv_review.append(uniqueID)
                
                    ## Rating (Review)
                    rating = self.build_rating(elements)
                    csv_review.append(rating)
                
                    ## Verified Purchase (Review)
                    verifiedPurchase = self.build_verified_purchase(elements)
                    csv_review.append(verifiedPurchase)
                
                    ## Max Rating (Review)
                    csv_review.append(max_rating)
                
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
                    csv_review.append(author_id)
                
                    ## Date Scraped (Review)
                    csv_review.append(dateToday)
                
                    ## Foreign Key Review to Product (Review)
                    csv_review.append(productID)
                
                    product.append(csv_product)
                    review.append(csv_review)
                
            browser.quit()
            return product, review, self.csv_data
        
    def selenium_scraperank(self):
    
        '''
        Rank scrape from author's profile page (Amazon only). Determine to see the author's rank based on
        how many reviews the author has conducted and how positive or negative their reviews are.
        
        @outputs: rank [string]
        
        '''
        self.timesleep = time.sleep(self.sleep_time)
        
        url = self.url
        browser = self.browser(url)
                
        try:
            WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#profile-at-card-container.a-section')))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
            
        self.timesleep
        
        self.rank = self.build_rank(browser)
        browser.quit()
        return(self.rank)