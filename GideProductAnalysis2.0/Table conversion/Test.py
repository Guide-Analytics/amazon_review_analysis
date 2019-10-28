'''
#################################################
@product: Gide Product Analysis
@filename: Test field

@author: Minh Doan
@date: February 26th 2019
@ver: 2.0
##################################################
'''


##Imported libraries:
from Tools import extract_csv_to_dict, filter_dict, get_list_of_values
import sys

## MAIN ##
if __name__ == '__main__':
    ## Import CSV file (Sentiment table):
    file = sys.argv[1]
    csv_file = open(file, 'rb')

    #what key you want
    key = 'KEYWORDS'
    # what Value you want to associate with the key
    value = 'Sentiment Score'
    # To export out in a text file or not:
    export = False

    ## Put CSV file into Dictionary format:
    # Ex:
    # Dict[key] = value
    Dict = extract_csv_to_dict(csv_file,key,value,export)

    ## Continue your code underneath if needed:
    Necessary_dict = {}
    retail = ['COST', 'DESIGN', 'CLICK', 'BLOW', 'NOISE', 'STRONG', 'QUIET']
    service = ['RETURNED', 'LOW', 'EFFICIENT']
    retail_filter = {}
    service_filter = {}

    retail_filter = filter_dict(Dict, retail, retail_filter)
    service_filter = filter_dict(Dict, service, service_filter)
    Necessary_dict = filter_dict(Dict, retail, Necessary_dict)
    Necessary_dict = filter_dict(Dict, service, Necessary_dict)

    List = []
    List = get_list_of_values(Necessary_dict, List)

    print(List)
    csv_file.close()
