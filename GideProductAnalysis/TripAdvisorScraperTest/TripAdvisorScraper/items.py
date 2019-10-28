# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

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
