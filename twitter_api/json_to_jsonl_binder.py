import os, json
import pandas as pd

############################################################
# Define Output Location
############################################################

current_path = os.getcwd()

directory = os.path.join(current_path,"json") #Specify your json directory path here

############################################################
# Changing File format to Json (NOT NECCESSARY IN THE DATA SAMPLING VERSIONS ABOVE 06/03/2020)
############################################################

#for file in os.listdir(directory): # This can rename your file in case they do NOT already end in .json
#    dst =  directory + "\\" +file + ".json"
#    src =  directory + "\\" +file
#    os.rename(src, dst)

############################################################
# Reading in all Jsons to one Python object
############################################################

json_list = []  # Initiate a new blank list for storing json data in list format
for dirpath, subdirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(dirpath, file)) as json_file:
                data = json.load(json_file)
                json_list.append(data)

############################################################
# Saving Python Object to JsonL
############################################################

with open('output.jsonl', 'w') as outfile: #Now, output the list of json data into a single jsonl file
    for entry in json_list:
        json.dump(entry, outfile)
        outfile.write('\n')

############################################################
# Test if you can access tweets independently
############################################################

tweets = []
for line in open('output.jsonl', 'r'):
    tweets.append(json.loads(line))

print(tweets[1])

