#############################################################################################################################
##################                                                                                         ##################
##################                              Overview of the scipt                                      ##################
##################                                                                                         ##################
#############################################################################################################################

# This script is a pilot to the emotion contagion project.
# it continues reading in an existing text file that contains
# !!!!!!!!!!! user_id, text !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# and adds likes, retweets and the dates created to an exosting file
# with minor adjustments it can add all infos contained in a twitter json.file

#############################################################################################################################
##################                                                                                         ##################
##################                              Library and Developer Key                                  ##################
##################                                                                                         ##################
#############################################################################################################################

import tweepy as tw
import pandas as pd
import subprocess
import shlex
import os
import io
import numpy as np
import m3inference
import json
from m3inference import get_lang
from pathlib import Path

#add API personal keys
#These are my personal login keys. If someone else uses this code, he/she has to put in their own credentials

###key nr2
consumer_key = ""
consumer_secret = ""
atoken =  ""
asecret =  ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(atoken, asecret)
api = tw.API(auth, wait_on_rate_limit=True)

#############################################################################################################################
##################                                                                                         ##################
##################                    Reading in Dataframes containing ID´s and Usernames                  ##################
##################                                                                                         ##################
#############################################################################################################################

original_file_path = 'D:\\' #The dataset that you want to add information to

continuing_file_path = 'D:\\' # If you have already started but not finished processing a file


d_full_csv = pd.read_csv(original_file_path, #reading in the original dataset. This dataset will not be changed during process
                         error_bad_lines=False,
                         index_col=False,
                         )

###Change the name of variable containing user_ids

d_full_csv = d_full_csv.rename(columns={"twitter_user_id": "twitter_user_id"})

if Path(continuing_file_path).is_file():
    expression_df = pd.read_csv(continuing_file_path, #reading in the dataset that should be continued
                             error_bad_lines=False,
                             index_col=False,
                             )
    ### Replace the second "user_id" in case the filename has different variable name
    expression_df = expression_df.rename(columns={"user_id": "user_id"})

#############################################################################################################################
##################                                                                                         ##################
##################                    Determin the index to continue                                       ##################
##################                                                                                         ##################
#############################################################################################################################

#### Progress Tracker ####
# only if the it has been processed before and the location  of the processed file is known.
#this finds the user_id of the last user in the processed file to know where to continue (expression_df["user_id"].iloc[-1]]) and transfers the  position into a list (couldnt do it straight into an integer, because of the function doesnt allow that)
if Path(continuing_file_path).is_file():
    n = d_full_csv.twitter_user_id[d_full_csv.twitter_user_id == expression_df["user_id"].iloc[-1]].index.tolist() #this finds the index in the original file that matches the id of the last processed one to continue at the last processed user
    n = (n[0]) #the list only contains one value, so we extract the value and change it into an integer
else:
    n = 0

m = d_full_csv["twitter_user_id"].iloc[-1] #to get the upper boundary, we find the highest index in the original dataset

print(n) #startpoint
print(m) #endpont

#############################################################################################################################
##################                                                                                         ##################
##################                    Continue Retrieving texts from users                                 ##################
##################                                                                                         ##################
#############################################################################################################################
if Path(continuing_file_path).is_file():
    tweet_text = expression_df["text"].tolist()
    tweet_id = expression_df["user_id"].tolist()
    tweet_date = expression_df["date"].tolist()
    tweet_likes = expression_df["likes"].tolist()
    tweet_retweets = expression_df["retweets"].tolist()
    user_followers = expression_df["user_followers"].tolist()
    user_created_date = expression_df["user_date_created"].tolist()

else:
    expression_df = pd.DataFrame(columns=["user_id", "text", "date"])
    tweet_text = []
    tweet_id = []
    tweet_date = []
    tweet_retweets = []
    tweet_likes = []
    user_followers = []
    user_created_date = []

def tweet_finder (id): # This function gets text and dates of an ID that you input into the fucntion
    for tweet in tw.Cursor(api.user_timeline, id=id, tweet_mode='extended').items(10):
        if hasattr(tweet, 'retweeted_status') == False:
            tweet_text.append(tweet.full_text)
            tweet_id.append(tweet.user.id)
            tweet_date.append(tweet.created_at)
            tweet_retweets.append(tweet.retweet_count)
            tweet_likes.append(tweet.favorite_count)
            user_created_date.append(tweet.user.created_at)
            user_followers.append(tweet.user.followers_count)

def crawler(n,m):
   while n < m:
        i = 0
        while i < 10: #while after I finished the first document
            try:
                id = d_full_csv["twitter_user_id"].iloc[n]
                tweet_finder(id)
                print(id)
                expression_df = pd.DataFrame(columns=["user_id", "text", "date"])
                expression_df["user_id"] = tweet_id
                expression_df["text"] = tweet_text
                expression_df["date"] = tweet_date
                expression_df["likes"] = tweet_likes
                expression_df["retweets"] = tweet_retweets
                expression_df["user_followers"] =  user_followers
                expression_df["user_date_created"] = user_created_date
                expression_df["lang"] = get_lang(expression_df["text"])
                expression_df = expression_df.loc[expression_df["lang"] == "en"]
                expression_df.to_csv(r'D:\\DownloadsDesktop\\Desktop\\Oxford\\FYP\\fyp_collective_emotion\\Data\\age_1_2.csv',
                                     index=None, header=True,  # after 10 iterations dataframe will be safed
                                     encoding="utf-8")
                i = i + 1
                n = n + 1
            except Exception as e:  # Error exception lines
                print(e)
                i = i + 1
                n = n + 1
    print("done")


crawler(n,m)

#############################################################################################################################
##################                                                                                         ##################
##################                    Deleting media/links etc.                                            ##################
##################                                                                                         ##################
#############################################################################################################################

expression_df = pd.read_csv('', #reading in the dataset that now contains the tweets for each user in the original datafile
                         error_bad_lines=False,
                         index_col=False,
                         )
i = 0 #iterator for addressing each cell of text indeividually
result = [] #creating a list of whether a text contains a URL plus the position of the URL
for index, row in expression_df.iterrows(): #for loop for the lenght of the file
    word = expression_df["text"][i] #this step had to be done because the function wants to work with a lost rather than a dataframe
    result.append(word.find("https")) #this function actually looks for the URLS in the text cell (that is now a list for this step for the above mentioned reason)
    i = i + 1 #counter

expression_df["URL"]= result #now it result of search goes back into dataframe


# Droppping duplicates. It will also tell you how much are left after and before deletion
print(len(expression_df["text"]))
print("number of rows before dropping duplicates")
expression_df = expression_df.drop_duplicates()
print(len(expression_df["text"]))
print("number of rows before dropping duplicates")

expression_df = expression_df.loc[expression_df["URL"] == -1]

expression_df.to_csv(r'D:\\',
                                     index=None, header=True,  # after 50 iterations dataframe will be safed
                                     encoding="utf-8")




###### To check changes for the search engine
tweet_text = []
tweet_id = []
tweet_date = []
tweet_retweets = []
tweet_likes = []
tweets = []
user_followers = []
user_created_date =[]

for tweet in tw.Cursor(api.user_timeline, screen_name = "JanineGorgonzo1", tweet_mode='extended').items(10):
    if hasattr(tweet, 'retweeted_status') == False:
        tweet_text.append(tweet.full_text)
        tweet_id.append(tweet.user.id)
        tweet_date.append(tweet.created_at)
        tweet_retweets.append(tweet.retweet_count)
        tweet_likes.append(tweet.favorite_count)
        user_created_date.append(tweet.user.created_at)
        user_followers.append(tweet.user.followers_count)
        tweets.append(tweet._json)
        print("nopes")
    else:
        print ("deine Mutter")
        print(tweet._json)


json_formatted_str = json.dumps(tweets, indent=2)

print(json_formatted_str)




print (d_full_csv[d_full_csv['twitter_user_id'].astype(str).str.contains('2814504492')])
