import csv 
import json 
import os
# assign directory
directory = '../data/archive/'
jsonFilePath = r'../data/larger_science_fiction.json'



def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'a', encoding='utf-8') as jsonf: 
        print(f'{len(jsonArray)}')
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

# csvFilePath = r'../data/archive/sf_.csv'
# csv_to_json(csvFilePath, jsonFilePath)

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        csv_to_json(f'{directory}{filename}', jsonFilePath)