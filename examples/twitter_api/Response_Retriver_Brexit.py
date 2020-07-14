import tweepy as tw
import pandas as pd
import subprocess
import shlex
import os
import io

#add API personal keys
#These are my personal login keys. If someone else uses this code, he/she has to put in their own credentials

consumer_key = ""
consumer_secret = ""
atoken =  ""
asecret =  ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(atoken, asecret)
api = tw.API(auth, wait_on_rate_limit=True)

### creating the Initial (Original) Tweets df. (df1)
## df1 should include all original tweets about a topic (search words). I could also change the way of search to a list of hashtags in an
## external text file, like Amits example. This file is so far more practise and I will have to think about how to search in general.
# in case we want a list of old tweet id like the Hillary one we could use : api.get_status(tweet_text["id"].iloc[0]) to look up old lists and
#create the df1 list this way. Shouldnt be a big deal

search_words = "#brexit" + " -filter:retweets"
date_since = "2018-11-16"
#tweet_list =[]

original_tweets = tw.Cursor(api.search,
q=search_words,
lang="en",
since=date_since).items(50)

# Iterate and print tweets (One Way)
#for tweet in tweets:
#tweet_list.append(tweet.text)

users_locs = [[tweet.user.screen_name, tweet.user.location, tweet.text, tweet.id, tweet.favorite_count] for tweet in original_tweets]

tweet_text = pd.DataFrame(data=users_locs, columns=['user', "location", "text", "id", "likes"])
ldf1 = len(tweet_text["user"])
df1 = tweet_text.drop_duplicates(subset='text', keep="last") #In my documentation I refere to the initial(original) list of tweets as df1.

### extrakting responses to original tweets based on tweetID

retweets_df = pd.DataFrame(columns = ["screen_name", "original_text","response"])

replies = []
full_text = []
user_name = []
response_likes = []


n = 0
for index, row in df1.iterrows():
    name = (tweet_text["user"].iloc[n])
    o_id = (tweet_text["id"].iloc[n]) - 1
    for full_tweets in tw.Cursor(api.user_timeline,screen_name = name, since_id = o_id,timeout=20).items(1):
      for retweet in tw.Cursor(api.search,q='to:'+ name,result_type='recent',timeout=15).items(10):
        if hasattr(retweet, 'in_reply_to_status_id_str'):
            if (retweet.in_reply_to_status_id_str == full_tweets.id_str):
                replies.append(retweet.text)
                full_text.append(full_tweets.text)
                user_name.append(name)
                response_likes.append(retweet.favorite_count)
                print(replies)
            else:
                print("no responses")
        else:
            print("Error")
	n = n + 1

retweets_df = pd.DataFrame(full_text, columns=['original_text'])
retweets_df["response"] = replies
retweets_df["name"] = user_name
retweets_df["response_likes"] = response_likes

df2 = retweets_df.drop_duplicates(subset='response', keep="last")

### creating files that senitstrenght can work with#

d1 = df1[['text']]
d1 = d1.values.tolist()
d2 = df2[["response"]]
d2 = d2.values.tolist()
d_full = d1 + d2

with open('tweets_text.txt', 'w', encoding="utf-8") as f:
    for item in d_full:
        f.write("%s\n" % item)

## Sentistrenght at work

SentiStrengthLocation = 'sentiment_tool/SentiStrength.jar' #The location of SentiStrength on your computer
SentiStrengthLanguageFolder ='sentiment_tool/SentiStrength_Data/' #The location of the unzipped SentiStrength data files on your computer

FileToClassify = "tweets_text.txt"
classifiedSentimentFile = "tweets_rating.txt"

with io.open(FileToClassify, encoding="utf-8") as f:
    for line in f:
        p = subprocess.Popen(shlex.split("java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "'"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = bytes(line.replace(" ","+"), 'utf-8') #Can't send string in Python 3, must send bytes
        stdout_byte, stderr_text = p.communicate(b)
        stdout_text = stdout_byte.decode("utf-8")  #convert from byte
        stdout_text = stdout_text.rstrip().replace(" ","\t") #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1 -5
        with open(classifiedSentimentFile, "a", encoding="utf-8") as myfile:
            myfile.write(stdout_text + "\t" + line)

print("Finished! The results will be in:\n" + classifiedSentimentFile)

###create finished file

# 1. Remove the formating of sentistrenght, so that the spacing is replaced by "[". This is to make sure the CSV file seperates correctly
# 2. The colom seperation is set to "[" in step 1. now also the delimeter has to be set to "["
# 3. seperate files again into original responses (df1) and (df2)
# 4. combine the files with extra information from intitial tweet


with open('tweets_rating.txt', encoding="utf-8", errors="ignore") as infile, open('tweets_rating_raw.csv','w', encoding="utf-8", errors="ignore") as outfile:
    for line in infile:
        outfile.write(line.replace('\t','['))