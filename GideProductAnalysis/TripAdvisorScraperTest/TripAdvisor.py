    from bs4 import BeautifulSoup
import requests
import re
import uuid
import datetime
#import webbrowser

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        
    s = requests.Session()
    r = s.get(url, headers=headers)

    #with open('temp.html', 'wb') as f:
    #    f.write(r.content)
    #    webbrowser.open('temp.html')

    if r.status_code != 200:
        print('status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')

def parse(url, response):

    if not response:
        print('no response:', url)
        return
    print(response)
    # get number of reviews
    #num_reviews = response.find('span', class_='reviews_header_count').text
    num_reviews = num_reviews[1:-1] # remove `( )`
    num_reviews = num_reviews.replace(',', '') # remove `,`
    num_reviews = int(num_reviews)
    print('num_reviews:', num_reviews, type(num_reviews))

    # create template for urls to pages with reviews
    url = url.replace('.html', '-or{}.html')
    print('template:', url)

    # load pages with reviews
    for offset in range(0, num_reviews, 5):
        print('url:', url.format(offset))
        url_ = url.format(offset)
        parse_reviews(url_, get_soup(url_))           
        return # for test only - to stop after first page
    

def parse_reviews(url, response):
    
    if not response:
        print('no response:', url)
        return

    item = {}
    titles = response.css("div.review-container")
        
    for title in titles:
        authorID = uuid.uuid4
        uniqueID = uuid.uuid4().hex
        productID = uuid.uuid4
            
        item['uniqueID'] = uniqueID
        item['rating'] = reviewBubble(title)
        item['verifiedPurchase'] = 'NULL'
        item['maxrating'] = 5
        item['reviewtitle'] = title.xpath(".//span[@class='noQuotes']/text()").extract()
        item['authorID'] = authorID 
        item['reviewtext'] = title.xpath(".//p[@class='partial_entry'][normalize-space()]/text()").extract()
        item['datewritten'] = title.xpath(".//span[@class='ratingDate relativeDate']/text()").extract()
        item['datescraped'] = datetime.datetime.now()
        item['productID'] = productID
            
        results.append(item)
         #~ yield item
        for key,val in item.items():
            print(key, ':', val)
        print('----')
        #return # for test only - to stop after first review
        
        print(results)  
        return
    
    def reviewBubble(hxs):
        rev_bub = ''
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_50']"): rev_bub = '5'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_45']"): rev_bub = '4,5'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_40']"): rev_bub = '4'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_35']"): rev_bub = '3,5'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_30']"): rev_bub = '3'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_25']"): rev_bub = '2,5'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_20']"): rev_bub = '2'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_15']"): rev_bub = '1,5'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_10']"): rev_bub = '1'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_05']"): rev_bub = '0,5'
        if hxs.xpath(".//span[@class='ui_bubble_rating bubble_00']"): rev_bub = '0'
        
        return rev_bub
# --- main ---

s = requests.Session()

start_urls = [
    'https://www.tripadvisor.com/Hotel_Review-g562819-d289642-Reviews-Hotel_Caserio-Playa_del_Ingles_Maspalomas_Gran_Canaria_Canary_Islands.html',
    #'https://www.tripadvisor.com/Hotel_Review-g60795-d102542-Reviews-Courtyard_Philadelphia_Airport-Philadelphia_Pennsylvania.html',
    #'https://www.tripadvisor.com/Hotel_Review-g60795-d122332-Reviews-The_Ritz_Carlton_Philadelphia-Philadelphia_Pennsylvania.html',
]

results = [] # <--- global list for items

for url in start_urls:
    parse(url, get_soup(url))

import pandas as pd

df = pd.DataFrame(results) # <--- convert list to DataFrame
df.to_csv('output.csv')    # <--- save in file
