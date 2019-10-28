'''
class AmazonConfig:
    
    def __init__(self):
        self.null = 0
        
    def productName(self):
        element = "a[data-hook='product-link']"
        return element
    
    def productURL(self):
        element = "a[data-hook='product-link']"
        return element
        
    def author(self):
        element = "span[class='a-profile-name']"
        return element
    
    def authorURL(self):
        element = "a[class='a-profile']"
        return element
          
    def rating(self):
        element = "a[class='a-link-normal']"
        value = 'span.a-icon-alt:last-child'
        return element, value
        
    def avgRating(self, elements):
        element1 = "div[class='a-row averageStarRatingIconAndCount']/div[class='a-fixed-left-grid AverageCustomerReviews']"
        element2 = "div[class='a-row averageStarRatingNumerical']"
        return element1, element2
        
    def title(self):
        element = "a[data-hook='review-title']"
        return element
        
    def text(self):
        element = "span[data-hook='review-body']"
        return element
        
    def date(self):
        element = "span[data-hook='review-date']"
        return element
    
    def verifiedPurchase(self):
        element = "[data-hook='avp-badge']"
        return element
    
    def detect(self):
        detectElement = 'div.a-fixed-right-grid.view-point'
        return detectElement
    
    def reviewsDetect(self):
        reviewsElement = "div[data-hook='review']"
        return reviewsElement 
    
class TripAdvisorConfig:
    
    def productName(self):
        element1 = "h1[class='heading_title']"
        element2 = "h1[class='ui_header h1']"
        return element1, element2
    
    def productURL(self):
        element = "a[data-hook='product-link']"
        return element
        
    def author(self):
        element1 = "div[class='info_text']"
        element2 = "div[class='username mo']"
        return element1, element2
    
    def authorURL(self):
        element = "a[class='a-profile']"
        return element
          
    def rating(self):
        element1 = "div[class='rating reviewItemInline']"
        element2 = ["span[class='ui_bubble_rating bubble_50']", "span[class='ui_bubble_rating bubble_45']", "span[class='ui_bubble_rating bubble_40']", 
                    "span[class='ui_bubble_rating bubble_35']", "span[class='ui_bubble_rating bubble_30']", "span[class='ui_bubble_rating bubble_25']", 
                    "span[class='ui_bubble_rating bubble_20']", "span[class='ui_bubble_rating bubble_15']", "span[class='ui_bubble_rating bubble_10']",
                    "span[class='ui_bubble_rating bubble_05']", "span[class='ui_bubble_rating bubble_00']"]
    
        return element1, element2
        
    def avgRating(self):
        element = "span[class='overallRating']"
        return element
        
    def title(self):
        element = "span[class='noQuotes']"
        return element
        
    def text(self):
        element = "p[class='partial_entry']" #[normalize-space()]/text()"
        return element
        
    def date(self):
        element1 = "span[class='ratingDate relativeDate']"
        element2 = "span[class='ratingDate']"
        return element1, element2
    
    def verifiedPurchase(self):
        element = "NULL"
        return element
    
    def detect(self):
        detectElement = 'div.listContainer'
        return detectElement
    
    def reviewsDetect(self):
        reviewsElement = "div.review-container"
        return reviewsElement 
    
    
class AmazonProfileConfig:
    
    def detect(self):
        element = 'div#customer-profile-timeline.a-section'
        return element
        
    def reviewsDetect(self):
        element = "//div[@class='desktop card profile-at-card profile-at-review-box']"
        return element
        
    def reviewVotes(self):
        element = "//div[@class='dashboard-desktop-stat-value']"
        return element
    
    def rating(self):
        element = 'span.a-icon-alt:last-child'
        return element
    
    def productName(self):
        element = 'div.a-row.a-spacing-medium'
        return element
    
    def avgRating(self):
        element1 = 'div.a-row.profile-at-product-review-stars'
        element2 = 'span.a-icon-alt:last-child'
        return element1, element2
    
    def productURL(self):
        element = "a[class='a-link-normal profile-at-product-box-link a-text-normal']"
        return element
    
    def rank(self):
        element = 'div.desktop.padded.card > div.a-row > div.a-section > div.a-section.a-spacing-top-base > div.a-row.a-spacing-base'
        return element
    
    def verifiedPurchase(self):
        element = 'div.a-row.a-spacing-mini:last-child'
        return element
    
class TripAdvisorProfileConfig:
    
    def detect(self):
        element = 'div.page'
        return element
        
    def reviewsDetect(self):
        element = "//div[@class='social-sections-CardSection__card_section--20Wxe ui_card section']"
        return element
        
    def reviewVotes(self):
        element = "//div[@class='dashboard-desktop-stat-value']"
        return element
    
    def rating(self):
        element1 = "div.social-sections-ReviewSection__review--3zYsC"
        element2 = ["span[class='ui_bubble_rating bubble_50']", "span[class='ui_bubble_rating bubble_45']", "span[class='ui_bubble_rating bubble_40']", 
                    "span[class='ui_bubble_rating bubble_35']", "span[class='ui_bubble_rating bubble_30']", "span[class='ui_bubble_rating bubble_25']", 
                    "span[class='ui_bubble_rating bubble_20']", "span[class='ui_bubble_rating bubble_15']", "span[class='ui_bubble_rating bubble_10']",
                    "span[class='ui_bubble_rating bubble_05']", "span[class='ui_bubble_rating bubble_00']"]
        return element1, element2
    
    def productName(self):
        element = 'div.social-common-POIObject__poi_name--39wh4 ui_link'
        return element
    
    def title(self):
        element = "div.social-sections-ReviewSection__title--HIMCX"
        return element
    
    def text(self):
        element = "div.social-sections-ReviewSection__body_text--5f5aM"
        return element
    
    def avgRating(self):
        element1 = "div.ui_poi_review_rating"
        element2 = ["span[class='ui_bubble_rating bubble_50']", "span[class='ui_bubble_rating bubble_45']", "span[class='ui_bubble_rating bubble_40']", 
                    "span[class='ui_bubble_rating bubble_35']", "span[class='ui_bubble_rating bubble_30']", "span[class='ui_bubble_rating bubble_25']", 
                    "span[class='ui_bubble_rating bubble_20']", "span[class='ui_bubble_rating bubble_15']", "span[class='ui_bubble_rating bubble_10']",
                    "span[class='ui_bubble_rating bubble_05']", "span[class='ui_bubble_rating bubble_00']"]
        return element1, element2
    
    def productURL(self):
        element = "div.social-sections-POICarousel__item--1Sbpp"
        return element
    
    def rank(self):
        element = 'div.desktop.padded.card > div.a-row > div.a-section > div.a-section.a-spacing-top-base > div.a-row.a-spacing-base'
        return element
    
    def verifiedPurchase(self):
        element = 'div.a-row.a-spacing-mini:last-child'
        return element
    
    def date(self):
        element = "div.social-common-MemberEventOnObjectBlock__item--2EMkj"
        return element
'''