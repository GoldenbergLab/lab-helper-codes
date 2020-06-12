import tweepy as tw
import pandas as pd
from os import listdir
from os.path import isfile, join
import os
import io
import numpy as np
import time
from pathlib import Path
import re

### Read In Location File

current_path = os.getcwd() # current directory

file_location = os.path.join(current_path,"USA_UK_locations.csv") # exact location of basefile

all_p = pd.read_csv(file_location, #reading in the original dataset
                     error_bad_lines=False,
                     index_col=False,
                     )

### Subset list of UK and USA

uk_d = all_p[(all_p.Country == "UK")] # UK Dataframe List

usa_d = all_p[(all_p.Country == "USA")] # USA Dataframe List

uk_l = uk_d["Name"].to_list() # UK List

usa_l = usa_d["Name"].to_list() # USA List

usa_l = [x.lower() for x in usa_l] # lower case names

uk_l = [x.lower() for x in uk_l] # lower case names


### List the files in the directory

file_location = os.path.join(current_path,"dataframe", NAMEOFFILE) # exact location of basefile

test_id = pd.read_csv(file_location, #reading in the original dataset
                     error_bad_lines=False,
                     index_col=False,
                     )

### Remove Users due to exclusion criterion


valid_name = []
screen_names = test_id["screen_names"]
for item in screen_names:
    item = item.lower()
    if item.find("covid") != -1 or item.find("corona") != -1:
        x = "False"
        valid_name.append(x)
    else:
        x = "True"
        valid_name.append(x)

test_id["valid_name"] = valid_name
test_id = test_id[test_id["valid_name"] != "False"]
test_id = test_id.drop_duplicates(subset='user_id', keep="last")

#### Main process of getting location

user_id = []
country = []
location_name = []
twitter_location = test_id["location"]
test_locations = all_p["Name"]

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

for items in twitter_location:
    items = str(items)
    items = items.lower()
    items = re.sub('[^0-9a-zA-Z-#]+', ' ', items)
    location_name_case = "not_defined"
    for item in test_locations:
        item = item.lower()
        if contains_word(items, item) == True:
            location_name_case = item
    location_name.append(location_name_case)

test_id["estimated_location"] = location_name

for elements in location_name:
    country_case = "not_defined"
    if elements in uk_l:
        country_case = "UK"
    if elements in usa_l:
        country_case = "USA"
    country.append(country_case)

test_id["estimated_country"] = country

### Result overview

d = test_id[test_id["estimated_country"] != "not_defined"]
uk = d[(d.estimated_country == "UK")]
usa = d[(d.estimated_country == "USA")]

### Save Finished File

finished_file = os.path.join(current_path,"dataframe", "Social_Sharing_Participants_June.csv") # exact location of finished file

d.to_csv(finished_file, index=None, header=True, #after all cases have been processed it again safes the last cases
                                                 encoding="utf-8")


