'''
#################################################
@product: Gide Product Analysis
@filename: Amazon Config File (Website Contents)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

class AmazonConfig:
    
    '''
    @purpose: Config string values for scraping web contents 

    '''    

    def __init__(self):
        
        '''
        @purpose: None
        '''
        
        self.null = 0
        
    def productName(self):
        
        '''
        @purpose: Product Name Extraction
        '''
        
        element = "a[data-hook='product-link']"
        return element
    
    def productURL(self):
        
        '''
        @purpose: Product URL Extraction
        '''
        
        element = "a[data-hook='product-link']"
        return element
        
    def author(self):
        
        '''
        @purpose: Author Name Extraction
        '''
        
        element = "span[class='a-profile-name']"
        return element
    
    def authorURL(self):
        
        '''
        @purpose: Author URL Extraction
        '''
        
        element = "a[class='a-profile']"
        return element
          
    def rating(self):
        
        '''
        @purpose: Review Rating Extraction
        Rating contains two steps: extraction of the rating configuration (element).
        The rating configuration contains the value (value) of the rating: (1 - 5 stars)
        '''
        
        element = "a[class='a-link-normal']"
        value = 'span.a-icon-alt:last-child'
        return element, value
        
    def avgRating(self):
        
        '''
        @purpose: Average Rating Extraction
        Rating contains two steps: extraction of the rating configuration (element1).
        The rating configuration contains the second configuration in text value (element2)
        (element2) of the rating: (1 - 5 stars)
        '''
        
        element1 = "div[class='a-row averageStarRatingIconAndCount']/div[class='a-fixed-left-grid AverageCustomerReviews']"
        element2 = "div[class='a-row averageStarRatingNumerical']"
        return element1, element2
        
    def title(self):
        
        '''
        @purpose: Review Title Extraction

        '''
        
        element = "a[data-hook='review-title']"
        return element
        
    def text(self):
        
        '''
        @purpose: Review Text Extraction

        '''
        
        element = "span[data-hook='review-body']"
        return element
        
    def date(self):
        
        '''
        @purpose: Review Date Extraction

        '''
        
        element = "span[data-hook='review-date']"
        return element
    
    def verifiedPurchase(self):
        
        '''
        @purpose: Review Verified Purchase Extraction

        '''
        
        element = "[data-hook='avp-badge']"
        return element
    
    def detect(self):
         
        '''
        @purpose: Site Body Detection
        This checks to see if the site contents are available and loaded
        '''
        
        detectElement = 'div.a-fixed-right-grid.view-point'
        return detectElement
    
    def reviewsDetect(self):
        
        '''
        @purpose: Review Body Detection
        This checks to see if the review contents are available and loaded
        '''
        
        reviewsElement = "div[data-hook='review']"
        return reviewsElement 