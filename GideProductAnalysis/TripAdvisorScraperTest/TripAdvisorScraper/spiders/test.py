from scrapy.spiders import Spider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import requests
import re
from scrapy.item import Item, Field

import uuid
import datetime

class TripadvisorscraperItem(Item):
    uniqueID = Field()
    rating = Field()
    verifiedPurchase = Field()
    maxrating = Field()
    reviewtitle = Field()
    reviewtext = Field()
    datewritten = Field()
    authorID = Field()
    datescraped = Field()
    productID = Field()

class MySpider(Spider):
    name = "trip"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.ca/Restaurant_Review-g294212-d886772-Reviews-or10-Hatsune_Japanese_Restaurant_Guanghua_Road-Beijing.html"]
    
    def parse_reviews(self, response):
        
        
        hxs = Selector(response)
        items = []
        titles = hxs.css("div.review-container")
        
        for title in titles:
            authorID = uuid.uuid4
            uniqueID = uuid.uuid4().hex
            productID = uuid.uuid4
            
            item = TripadvisorscraperItem()
            item['uniqueID'] = uniqueID
            item['rating'] = self.reviewBubble(title)
            item['verifiedPurchase'] = 'NULL'
            item['maxrating'] = 5
            item['reviewtitle'] = title.xpath(".//span[@class='noQuotes']/text()").extract()
            item['authorID'] = authorID 
            item['reviewtext'] = title.xpath(".//p[@class='partial_entry'][normalize-space()]/text()").extract()
            item['datewritten'] = title.xpath(".//span[@class='ratingDate relativeDate']/text()").extract()
            item['datescraped'] = datetime.datetime.now()
            item['productID'] = productID
            
            items.append(item)
        
        print(items)  
        return
    
    def reviewBubble(self, hxs):
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