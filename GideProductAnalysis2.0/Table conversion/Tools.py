'''
#################################################
@product: Gide Product Analysis
@filename: Tools used in all files

@author: Minh Doan
@date: March 1st 2019
@ver: 1.0
##################################################
'''

##Imported libraries:
import csv, collections


def category_list(reader, category):
    index = 0
    if category == []:
        for row in reader:
            if index == 1:
                category = row
                index = 0
                break
            else:
                index += 1
                continue
    return category


def extract_csv_to_dict(csv_file, key, value, export):
    reader = csv.reader(csv_file)
    Dict = {}
    index_start = 2
    category = []
    index = 0
    category = category_list(reader, category)
    i_key = 0
    i_value = 0

    for key_index in category:
        if key_index == key:
            i_key = index
            break
        else:
            index += 1

    index = 0

    for value_index in category:
        if value_index == value:
            i_value = index
            break
        else:
            index += 1

    for row in reader:
        ## Dictionarize CSV file:
        if row[i_key] in Dict:
            Dict[row[i_key]].append(row[i_value])
        else:
            Dict[row[i_key]] = [row[i_value]]
        index_start += 1

    ## Reorder dictionary by dates, increment:
    Dict = collections.OrderedDict(sorted(Dict.items()))

    if export is True:
        csv_writer(Dict, key, value)
        return Dict
    else:
        return Dict


def csv_writer(Dict, key, value):
    # Writing to CSV:
    print("Writing...")

    with open('Result.txt', mode='w+') as CSV_writer:
        CSV_writer.write(key)
        CSV_writer.write(',')
        CSV_writer.write(value)
        CSV_writer.write('\n')

        for key in Dict:
            CSV_writer.write(key)
            CSV_writer.write(',')

            for value in Dict[key]:
                CSV_writer.write(value)
                CSV_writer.write(';')

            CSV_writer.write('\n')

    print("Writing completed")


def filter_dict(Dict, list, filter_dict):
    for keywords in Dict:
        if keywords in list:
            filter_dict[keywords] = Dict[keywords]

    return filter_dict

def get_list_of_values(Dict, List):
    for keywords in Dict:
        for value in Dict[keywords]:
            List.append(value)
    return List
