import os, json
import pandas as pd
from datetime import datetime

# Sometimes if we have too many jsons in a folder it is hard to delete them via cmd or windows tasks, thats why we have this code

############################################################
# Define Output Location
############################################################

current_path = os.getcwd()

directory = os.path.join(current_path,"json") #Specify your json directory path here

############################################################
# Remove all json files form directory
############################################################

for file in os.listdir(directory): # This can rename your file in case they do NOT already end in .json
    if file.endswith(".json"):
        file_to_delete = os.path.join(directory,file)
        os.remove(file_to_delete)