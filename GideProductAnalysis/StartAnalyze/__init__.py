'''
#################################################
@product: Gide Product Analysis
@filename: Start (Setup)

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

from reportOutput import start

def setup():
    
    '''
    @purpose: Starting the Gide Product Analysis: Extraction from webpages and database. (Phase 1-3)
    Then, perform filtering analysis of all the reviews scraped. (Phase 4)
    Lastly, conduct and output three reports; two which contains one product URL and the information of 
    the authors given the reviews (product_info, sentiment_info). Then, (author_info) will contain
    all the reviews from all the authors
    
    '''
    #tempProdName = 'Comfort Zone CZST161BTE Pedestal Fan'
    #tempProdURL = 'https://www.amazon.ca/Comfort-Zone-CZST161BTE-Pedestal-Fan/dp/B004IPA774/ref=cm_cr_arp_d_product_top?ie=UTF8'
    
    ext = input('Extraction, Filtering, or do both, or both and Report Output (e/f/b/r): ')
    ext = ext.lower()
    
    if ext == 'e' or ext == 'b' or ext == 'r':
        '''Phase 1-3:'''
        from Extraction import initiateExtraction
        productname, producturl = initiateExtraction.initExtraction()
        
    if ext == 'f' or ext == 'b' or ext == 'r':
        '''Phase 4:'''
        from FilteringAnalysis import initiateAnalysis
        trigger = raw_input('Score columns and values update? If generating new score columns, select \'n\' (y/n): ')
        initiateAnalysis.filteringAnalysis(trigger)
        
    if ext == 'r':
        '''Phase 5:'''
        start(productname, producturl)
    
'''Trigger: If score has been removed by resetting the table for new authors,
filtering analysis must generate a new score table, so 'n' is the trigger. '''

setup()