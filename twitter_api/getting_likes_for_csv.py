import tweepy as tw
import pandas as pd
import subprocess
import shlex
import os
import io
import numpy as np
from pathlib import Path

#add API personal keys
#These are my personal login keys. If someone else uses this code, he/she has to put in their own credentials

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
current_path = os.getcwd()

original_file_path = os.path.join(current_path,"data","gay_all_originals.csv")

d_full_csv = pd.read_csv(original_file_path, #reading in the original dataset
                         error_bad_lines=False,
                         index_col=False,
                         )

d_full_csv["processed"] = np.nan #this colomn is initially emty, which will be used to keep track of the process of filling in likes and retweets
d_full_csv["likes"] = np.nan #in case the data will be processed in multiple attempts, the if statment prevents the scriped from erasing the progress with NANs
d_full_csv["retweets"] = np.nan

split = len(d_full_csv)/2
d_full_csv = d_full_csv[int(split):]
d_full_csv = d_full_csv.reset_index(drop=True) # Only for the second half of a dataframe that needs to be processed to reset the index, which is neccessary for combining processed and unprocessed information in dataframes

continuing_file_path = os.path.join(current_path,"data","gay_all_originals_2_2.csv")


if Path(continuing_file_path).is_file():
    df_p = pd.read_csv(continuing_file_path, #reading in the original dataset
                         error_bad_lines=False,
                         index_col=False,
                         dtype={"processed": object}) #the colomn 9 ("process") needs to be assigned as object, otherwise it raises a warning,
# because pandas doesnt know what type it is and tries to guess the type which costs working memory. The original dataset does not have the colomn "processed", but
#it seems like this isnt an issue for the scriped and doesnt raise an error


# This part is a bug fix. For some reason, and I think its the size of the file, the dataframe gets cutoff at some point. Thats why the processed file will
# be add to the complete file.
    cutoff_list = df_p["processed"] #this line cuts of th process information into a list
    cutoff_list = cutoff_list.dropna() #this list gets shorten to the ones that have been processed
    cutoff = len(cutoff_list) #this givess the index of the last processed id
    #print(df_p["id"][cutoff-1]) # in case off doub that this is indeed the same person in both df you can print this
    #print(d_full_csv["id"][cutoff-1])
    d_full_csv[0:cutoff-1]= df_p # the processed information goes on top of the original dataframe to fill in the progress without changing the original file

#############################################################################################################################
##################                                                                                         ##################
##################                    Getting likes and Retweets                                           ##################
##################                                                                                         ##################
#############################################################################################################################

# This loop goes through the dataframe checking if a tweet as been processed already. This means that we already retreived the likes and retweets. I implemented this step in case
# someone cannot process all the data in one session or in case of an unexpected error. Every 50 searches this loop safes its progress. The likes and retweets will gathered
# using tweet and user id. In case a user or tweet doesnt exist this loop will print an error and keeps going after.

left_tweets = d_full_csv["processed"].isna().sum() #left_tweets is the variable that tracks how much tweets are left and need to be processed. This value will be used in the
#next step to start the loop on the right position.
#this right position starts at the last case that has a value (either "processed" or "processed with error") in colomn "processed".

n = len(d_full_csv["processed"]) - left_tweets #The full length of cases minus the ones that arent processed is the position of the last processed case. Which is starting point for the loop.
count = 0 #Count is the variable that makes sure that after 50 iterations (tweets) the file will be safed. I had the problem that the scriped got stuck in the past and all the progress was gone.
for i in range(left_tweets): #this loop goes through only the remaining cases (tweets) starting by the last processed one determined by "n"
    if count < 500: #Only neccessary if someone doesnt want to download everything at once. I decided for 50 so that there will be regular safes.
        if pd.isnull(d_full_csv["processed"].iloc[n]) is True: #this double checks if the tweet was not already processed indicated by a NaN in the colomn. If so it skips to the next case.
            o_id = int(d_full_csv["tweet_id"].iloc[n]) #This extracts the tweet id from the case on the last unprocessed case on position n
            try: #in case of an error (which is usually 404), I implemented try and except
                tweets=api.get_status (o_id) #search request for the tweet coresponding to the id
                d_full_csv["likes"].iloc[n] = tweets.favorite_count #LIKES will be assigned to the case. Favourite_count = likes that what people agreed on Stackoverflow. Hope thats true!
                d_full_csv["retweets"].iloc[n] = tweets.retweet_count #Same for retweets
                d_full_csv["processed"].iloc[n] = "processed" #Case will be labeled as processed to track progess


            except Exception as e: #Error exception lines
                print(e) #descriptive text
                print(n) #case that has an error. Also helps keeping track on progress while scriped runs
                d_full_csv["processed"].iloc[n] = "processed_error" #Case will be labeled as processed to track progess. But also with the note that it had an error.

        else:
            n = n + 1 #Corresponds to the second if statment. In case the tweet has been processed already the loop skips to the next case.



        n = n + 1 #after successful process of a tweet this changes the working-case to the next tweet in the dataframe
        count = count + 1  # after running through one case successfuly the count will increase, so that the scriped will be safed after 50 iterations
    else:
        partially_processed_file = d_full_csv.to_csv(continuing_file_path, index=None, header=True, #after 50 iterations dataframe will be safed
                                                 encoding="utf-8")
        count = 0 #iteration counter goes back to 0. to start counting for the next chunk of 50 processed tweets

partially_processed_file = d_full_csv.to_csv(continuing_file_path, index=None, header=True, #after all cases have been processed it again safes the last cases
                                                 encoding="utf-8")

